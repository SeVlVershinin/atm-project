import pathlib

from dadata import Dadata

from configs import Settings
from data_collection.pipelines import extend_initial_dataset_with_geo_data
from data_collection.services import (
    load_dataset_from_csv,
    save_dataset_to_csv,
)


def main():
    settings = Settings()
    file_path = pathlib.Path(settings.datasets_dir_path) / settings.initial_dataset_name
    initial_dataset = load_dataset_from_csv(file_path)
    dadata_client = Dadata(settings.dadata_api_key,
                           settings.dadata_secret_key)
    dataset_out = extend_initial_dataset_with_geo_data(
        initial_dataset, dadata_client, settings.geo_tree_secret_key
    )
    saving_path = pathlib.Path(settings.datasets_dir_path) / settings.with_geodata_dataset_name
    save_dataset_to_csv(saving_path, dataset_out)


if __name__ == "__main__":
    main()
