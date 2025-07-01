import pandas as pd
import pymc as pm
import numpy as np
import sys
import pickle
import pytensor
sys.path.append(r"C:\Users\janth\OneDrive\Desktop\Studium\Bachelorarbeit\Regelleistungs Vorhersage\pymc-bart-main\pymc-bart-main")
from pymc_bart.bart import BART

def run_bart_model():
    # Trainingsdaten
    np.random.seed(42)
    X = np.random.randn(100, 2)
    Y = X[:, 0] * 2 + X[:, 1] * -1 + np.random.normal(0, 0.5, 100)
    print("Modell wird aufgebaut")

    with pm.Model() as model:
        μ = BART("μ", X=X, Y=Y, m=50)
        σ = pm.HalfNormal("σ", 1)
        y_obs = pm.Normal("y_obs", mu=μ, sigma=σ, observed=Y)

        trace = pm.sample(1000, chains=2, tune=1000, target_accept=0.9)
        with open("final_bart_trees.pkl", "wb") as f:
            pickle.dump(model.μ.owner.op.all_trees, f)

if __name__ == "__main__":
    run_bart_model()
