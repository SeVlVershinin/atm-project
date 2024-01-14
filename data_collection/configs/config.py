from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    dadata_api_key: str
    dadata_secret_key: str
    geo_tree_secret_key: str

    datasets_dir_path: str = "datasets"
    initial_dataset_name: str = "train_initial.csv"
    fixed_dataset_name: str = "train_initial_fixed.csv"
    with_geodata_dataset_name: str = "train_with_geo_data.csv"
    extended_with_pois_dataset_name: str = "train_with_pois.csv"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
