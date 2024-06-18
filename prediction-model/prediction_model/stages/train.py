import pickle

import numpy as np
import mlflow
import mlflow.sklearn
from catboost import CatBoostRegressor
from sklearn.ensemble import StackingRegressor
from sklearn.linear_model import Lasso
from sklearn.metrics import r2_score, mean_squared_error as mse

from config import MainConfig


def train_model(cfg: MainConfig):
    models = [
        ("lasso", Lasso(alpha=cfg.params.lasso.alpha)),
        ("catboost", CatBoostRegressor(
            iterations=cfg.params.catboost.iterations,
            verbose=False
        ))
    ]
    ensemble = StackingRegressor(
        estimators=models,
        verbose=True,
    )
    X_train_sc = np.load(cfg.files.x_train_scaled)
    y_train = np.load(cfg.files.y_train)
    X_test_sc = np.load(cfg.files.x_test_scaled)
    y_test = np.load(cfg.files.y_test)

    with mlflow.start_run():
        ensemble.fit(X_train_sc, y_train)

        mlflow.log_param("model_type", "ensemble")
        mlflow.log_param("models", str(models))

        y_pred = ensemble.predict(X_test_sc)
        rmse = mse(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        mlflow.log_metric("RMSE", rmse)
        mlflow.log_metric("R2", r2)

        mlflow.sklearn.log_model(ensemble, "model")

    with open(cfg.files.model_pickle, "wb") as f:
        pickle.dump(ensemble, f)
