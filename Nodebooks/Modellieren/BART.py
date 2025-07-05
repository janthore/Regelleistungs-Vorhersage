import pandas as pd
import pymc as pm
import numpy as np
import sys
import pickle
import pytensor
sys.path.append(r"C:\Users\janth\OneDrive\Desktop\Studium\Bachelorarbeit\Regelleistungs Vorhersage\pymc-bart-main\pymc-bart-main")
from pymc_bart.bart import BART
from pymc_bart.utils import _sample_posterior
from sklearn.model_selection import train_test_split


def run_bart_model(X, Y, x_test, y_test):
    # Trainingsdaten
    np.random.seed(42)

    print("Modell wird aufgebaut")

    with pm.Model() as model:
        μ = BART("mu", X=X, Y=Y, m=500, alpha=0.985, beta=0.5)
        σ = pm.HalfNormal("σ", 1)
        y_obs = pm.Normal("y_obs", mu=μ, sigma=σ, observed=Y)

        trace = pm.sample(1000, chains=4, cores=4, tune=1000, target_accept=0.9)
        real_trees = [list(chain) for chain in model["mu"].owner.op.all_trees]
        with open("final_bart_trees.pkl", "wb") as f:
            pickle.dump(real_trees, f)


    trees = model['mu'].owner.op.all_trees
    rng = np.random.default_rng()
    preds = _sample_posterior(trees, x_test, rng=rng, shape=1000)
    print("Shape:", preds.shape)  # Sollte (1, 10, 1000) sein

    # Unsicherheit pro Beobachtung
    pred_mean = preds.mean(axis=-1).squeeze()  # (10,)
    pred_std = preds.std(axis=-1).squeeze()  # (10,)

    # Quantile aus der Verteilung, nicht aus der std!
    quantiles = np.quantile(preds, q=[0.025, 0.5, 0.975], axis=-1).squeeze()  # (3, 10)
    q_lower, q_median, q_upper = quantiles

    return pred_mean, pred_std, q_lower, q_median, q_upper


if __name__ == "__main__":
    df = pd.read_csv(r"C:\Users\janth\OneDrive\Desktop\Studium\Bachelorarbeit\Regelleistungs_Vorhersage\Nodebooks\Ergebnisse\Modellierungen\V05\Modellierung_05.csv", index_col=0, parse_dates=True)
    df_sampled = df.sample(n=15000, random_state=42)
    X = df.drop(columns=["Deutschland (Positiv)", "Deutschland (Negativ)"])
    y_pos = df["Deutschland (Positiv)"]
    X_train, X_test, y_train, y_test = train_test_split(X, y_pos, test_size=0.2, random_state=42)
    pred_mean, pred_std, q_low, q_med, q_up = run_bart_model(X_train, y_train, X_test, y_test)
    print("Mittelwerte:", pred_mean)
    print("95%-CI unten:", q_low)
    print("Median:", q_med)
    print("95%-CI oben:", q_up)

    df_ergebnisse = pd.DataFrame()
    df_ergebnisse["pred_mean"] = pred_mean
    df_ergebnisse["pred_std"] = pred_std
    df_ergebnisse["q_low"] = q_low
    df_ergebnisse["q_med"] = q_med
    df_ergebnisse["q_up"] = q_up
    df_ergebnisse.to_csv("Modell_05_bart_results.csv")


