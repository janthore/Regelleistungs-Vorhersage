import numpy as np
import matplotlib.pyplot as plt
import xgboost as xgb
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
import pandas as pd
import matplotlib.pyplot as plt


class BaseModel:
    def __init__(self,name, x, y, x_test=None, y_test=None, train_test_split=False, test_size=0.2,random_state_split=42 , val=False):
        print(f"{name} wurde ausgeführt mit {x.shape[0]} an Einträgen, für {x.shape[1]} verschiedene Variablen")
        self.x = x
        self.y = y
        self.x_test = None
        self.y_test = None
        self.x_val = None
        self.y_val = None

        self.model = None
        self.y_pred = None

        if train_test_split:
            self.split(test_size=test_size, random_state=random_state_split, val=val)

    def fit(self):
        if self.model is None:
            raise NotImplementedError("Modellobjekt muss in Subklasse gesetzt werden.")
        self.model.fit(self.x, self.y)

    def predict(self, x_test=None, y_test=None):
        self.x_test = self.x if x_test is None else x_test
        self.y_test = self.y if y_test is None else y_test
        self.y_pred = self.model.predict(self.x_test)
        return self.y_pred

    def split(self, test_size=0.2, random_state=42, val=False):
        if val:
            x_trainval, self.x_test, y_trainval, self.y_test = train_test_split(self.x, self.y, test_size=test_size, random_state=random_state)
            self.x, self.x_val, self.y, self.y_val = train_test_split(x_trainval, y_trainval, test_size=test_size, random_state=random_state)

        else:
            self.x, self.x_test, self.y, self.y_test = train_test_split(self.x, self.y, test_size=test_size,random_state=random_state )

    @property
    def mse(self):
        if self.y_pred is None: self.predict()
        return np.mean((self.y_test - self.y_pred) ** 2)

    @property
    def r2(self):
        if self.y_pred is None: self.predict()
        return 1 - (np.sum((self.y_test - self.y_pred) ** 2) / np.sum((self.y_test - np.mean(self.y_test)) ** 2))

    @property
    def rmse(self):
        if self.y_pred is None: self.predict()
        return np.sqrt(self.mse)

    def regelleistung_performance(self):
        df = pd.DataFrame()
        df["y_test"] = self.y_test
        df["y_pred"] = self.y_pred
        df["error"] = df["y_test"] - df["y_pred"]

        anzahl = df["y_pred"].shape[0]

        print(f"Mean y_true: {np.mean(df['y_test'])}")
        print(f"Mean y_pred: {np.mean(df['y_pred'])}")
        print(f"Mean error: {np.mean(df['error'])}")
        print(f"Zu wenig Regeleistung: {df[df['error'] > 0].shape[0]}")
        print(f"Das ist: {df[df['error'] > 0].shape[0]/anzahl}")


class LinearRegression(BaseModel):
    def __init__(self, x, y, x_test=None, y_test=None):
        super().__init__("Lineare Regression",x,y, x_test, y_test)
        self.X = sm.add_constant(self.x)
        self.model = sm.OLS(self.y, self.X).fit()

    def predict(self, x_test=None, y_test=None):
        def bestätigung():
            antwort = input("Möchtest du fortfahren? (j/n): ")
            if antwort.lower() in ["j", "ja"]:
                print("Fortfahren...")
                return True
            else:
                print("Abgebrochen.")
                return False

        # ❗ Fehlerhafte Bedingung: x_test or y_test is None prüft nur y_test
        if x_test is None or y_test is None:
            print("Achtung: x_test oder y_test ist nicht übergeben worden.")
            if not bestätigung():
                print("Vorhersage abgebrochen.")
                return  # ⛔ Abbruch der Funktion

        self.x_test = sm.add_constant(x_test)
        self.y_test = y_test
        self.y_pred = self.model.predict(self.x_test)
        return self.y_pred

    def fit(self):
        pass

    def summary(self):
        return self.model.summary()




class XGBoostRegression(BaseModel):
    def __init__(
        self, x, y, x_test=None, y_test=None,
        n_estimators=100,         # Anzahl der Bäume (mehr = bessere Genauigkeit, höhere Rechenzeit)
        learning_rate=0.1,        # Lernrate (wie stark jeder Baum zur Vorhersage beiträgt)
        max_depth=3,              # Maximale Tiefe der Bäume (Komplexität / Overfitting)
        subsample=1.0,            # Anteil der Daten, die für jeden Baum verwendet werden (für Varianzreduktion)
        colsample_bytree=1.0,     # Anteil der Merkmale, die pro Baum verwendet werden
        gamma=0,                  # Mindestverbesserung, damit ein Knoten gesplittet wird (Regularisierung)
        reg_alpha=0,              # L1-Regularisierung (Sparsamkeit/Funktionseinschränkung)
        reg_lambda=1,             # L2-Regularisierung (Stabilität, Vermeidung von Overfitting)
        random_state=None,         # Zufallsstartwert für Reproduzierbarkeit

        train_test_split =False,
        test_size=0.2,
        random_state_split=42,
        val=True
    ):
        super().__init__("XGBoost",x, y, x_test, y_test, train_test_split, test_size, random_state_split, val)

        self.model = xgb.XGBRegressor(
            n_estimators=n_estimators,
            learning_rate=learning_rate,
            max_depth=max_depth,
            subsample=subsample,
            colsample_bytree=colsample_bytree,
            gamma=gamma,
            reg_alpha=reg_alpha,
            reg_lambda=reg_lambda,
            random_state=random_state,
            verbosity=0,
            eval_metric='rmse',
            early_stopping_rounds=50
        )
        print(self.x.shape)
        print(self.y.shape)
        print(self.x_test.shape)
        print(self.y_test.shape)
        print(self.x_val.shape)
        print(self.y_val.shape)
        print("Model wird trainiert")
        # 🔁 Nur wenn val-Daten vorhanden sind, verwenden wir sie!
        if self.x_val is not None and self.y_val is not None:
            self.model.fit(
                self.x, self.y,
                eval_set=[(self.x_val, self.y_val)],
                verbose=100
            )
        else:
            self.model.fit(self.x, self.y)

        self.predict(self.x_test, self.y_test)
    def get_feature_importance(self, importance_type="weight", visualation=True):
        def plot_importance_type(booster, importance_type):
            plt.title(f"Feature Importance - {importance_type}")

            xgb.plot_importance(booster, importance_type=importance_type)
            plt.tight_layout()
            plt.show()
        booster = self.model.get_booster()
        if importance_type == "all":
            importance = []
            for itype in ["weight", "gain", "cover", "total_gain", "total_cover"]:
                scores = booster.get_score(importance_type=itype)
                importance.append((itype, scores))
                if visualation:
                    plot_importance_type(booster=booster,importance_type=itype)
            return importance
        else:
            scores = booster.get_score(importance_type=importance_type)
            if visualation:
                plot_importance_type(booster=booster,importance_type=importance_type)
            return scores

    def get_performance_bins(self):
        print(self.y_test)
        print(self.y_pred)
        print("Formel: y_true - y_pred")
        df = pd.DataFrame()
        df["y_test"] = self.y_test
        df["y_pred"] = self.y_pred
        df["error"] = df["y_test"].abs() - df["y_pred"].abs()
        df["y_test_bins"] = pd.cut(df["y_test"], bins=10, labels=False)
        error_stats = df.groupby("y_test_bins")["error"].agg(["count", "mean", "std", "min", "max"])
        return error_stats


if __name__ == '__main__':
    df = pd.read_csv(r"/Nodebooks/Parameter/ForecastError/50HZ_forecast_error_data.csv", index_col=0, parse_dates=True, dayfirst=True)
    x = df.drop(columns=["DE_50HZ"])
    y = df["DE_50HZ"]
    print("Start")
    model = XGBoostRegression(x, y,n_estimators=10000, max_depth=10, train_test_split=True, val=True)
    print("MSE:", model.mse)
    print("R²:", model.r2)
    print("rmse:", model.rmse)

    print(model.get_performance_bins())