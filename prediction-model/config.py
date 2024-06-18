from dataclasses import dataclass


@dataclass
class Files:
    init_dataset: str
    loaded_dataset: str
    x_train_scaled: str
    y_train: str
    x_test_scaled: str
    y_test: str
    encoder_pickle: str
    imputer_pickle: str
    scaler_pickle: str
    model_pickle: str


@dataclass
class CatBoostParams:
    iterations: int | None
    learning_rate: float | None
    tree_depth: int | None
    verbose: bool


@dataclass
class LassoParams:
    alpha: float


@dataclass
class StackingParams:
    verbose: bool


@dataclass
class Params:
    catboost: CatBoostParams
    lasso: LassoParams
    stacking: StackingParams


@dataclass
class Urls:
    mlflow_url: str = "http://128.0.1.1:8080"


@dataclass
class MainConfig:
    files: Files
    params: Params
    urls: Urls
