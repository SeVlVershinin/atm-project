import logging

import hydra
import mlflow
import mlflow.sklearn

from config import MainConfig
from prediction_model.stages.load_data import load_data
from prediction_model.stages.extract_features import extract_features
from prediction_model.stages.train import train_model


logger = logging.getLogger(__name__)


@hydra.main(config_path="config", config_name="main_conf", version_base=None)
def main(cfg: MainConfig) -> None:
    logger.info("Model training pipeline started")
    mlflow.set_tracking_uri(uri=cfg.urls.mlflow_url)
    load_data(init_dataset_path=cfg.files.init_dataset,
              loaded_dataset_path=cfg.files.loaded_dataset)
    extract_features(file_cfg=cfg.files)
    train_model(cfg=cfg)
    logger.info("Model successful trained")


if __name__ == "__main__":
    main()
