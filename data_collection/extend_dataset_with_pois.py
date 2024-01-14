import pathlib

from configs import Settings
from data_collection.pipelines import (
    extend_dataset_with_pois_data,
)
from data_collection.services import (
    load_dataset_from_csv,
    save_dataset_to_csv,
)


def main():
    settings = Settings()
    file_path = pathlib.Path(settings.datasets_dir_path) / settings.with_geodata_dataset_name
    origin_dataset = load_dataset_from_csv(file_path)
    osm_cache_path = pathlib.Path(settings.data_dir_path) / settings.osm_cache_filename
    dataset_out = extend_dataset_with_pois_data(
        origin_dataset,
        settings.pois_searching_radius,
        osm_cache_path
    )
    saving_path = pathlib.Path(settings.datasets_dir_path) / settings.extended_with_pois_dataset_name
    save_dataset_to_csv(saving_path, dataset_out)


if __name__ == "__main__":
    main()
