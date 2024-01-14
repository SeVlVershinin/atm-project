import pathlib
from pprint import pprint

from dadata import Dadata
import pandas as pd

from ..exceptions import (
    NotFoundCoreException,
    ValidationCoreException,
    InvalidParametersCoreException,
)
from ..schemas import (
    DatasetObjectWithGeoData,
    FilteredGeoData,
    OriginalGeoData,
    OriginalDatasetObject,
    OSM_TAG_CATEGORIES,
)
from ..services import (
    convert_poi_tag_counts_to_category_counts,
    get_extended_geo_data_from_dadata,
    get_population_stats_by_oktmo_list,
    get_poi_counts_near_geolocation,
    load_osm_pbf_to_dataframe,
    merge_original_atm_dataset_with_geo_data,
)
from ...dto_models import AtmData


def extend_original_atm_dataset(dataset: list[AtmData],
                                dadata_api_key: str,
                                dadata_secret: str,
                                geo_tree_api_key: str) -> pd.DataFrame:
    # TODO: add docstring
    dadata_client = Dadata(token=dadata_api_key, secret=dadata_secret)
    dataset_out = {}
    geocoding_warnings = []
    oktmo_set = set()
    for index, dataset_item in enumerate(dataset):
        geo_object = OriginalGeoData.model_validate({
            "lat": dataset_item.lat,
            "long": dataset_item.lon,
        })
        try:
            geocoding_out = get_extended_geo_data_from_dadata(
                geo_object,
                dadata_client
            )
        except (NotFoundCoreException,
                InvalidParametersCoreException,
                ValidationCoreException) as exc:
            geocoding_warnings.append({
                "id": index,
                "geocoding_warnings": [str(exc)]
            })
            continue
        if geocoding_out.warnings:
            geocoding_warnings.append({
                "id": index,
                "geocoding_warnings": geocoding_out.warnings,
            })
        dataset_out[index] = DatasetObjectWithGeoData.model_validate({
            **geo_object.model_dump(),
            "atm_group": dataset_item.atm_group,
            **geocoding_out.geolocation.model_dump(),
        })
        if geocoding_out.geolocation.oktmo is not None:
            oktmo_set.add(geocoding_out.geolocation.oktmo)

    population_out = get_population_stats_by_oktmo_list(
        oktmo_list=list(oktmo_set),
        api_key=geo_tree_api_key
    )

    out = []
    # TODO: replace prints with logging
    print("===========Geocoding warnings============")
    pprint(geocoding_warnings)
    print("========Population stats warnings========")
    pprint(population_out.exceptions)
    for index, dataset_item in enumerate(dataset):
        dataset_obj = OriginalDatasetObject.model_validate({
            "atm_group": dataset_item.atm_group,
            "lat": dataset_item.lat,
            "long": dataset_item.lon,
        })
        geolocation = dataset_out.get(index)
        oktmo = geolocation.oktmo if geolocation else None
        filtered_geolocation = FilteredGeoData.model_validate(geolocation.model_dump()) \
            if geolocation else None
        population_status = population_out.population_stats.get(oktmo)
        out.append(
            merge_original_atm_dataset_with_geo_data(
                initial_dataset_obj=dataset_obj,
                geolocation=filtered_geolocation,
                population_stats=population_status,
            )
        )
        # TODO: add pois collecting logic from extend_dataset_with_pois_data func

    return out


def extend_dataset_with_pois_data(dataset: list[dict],
                                  searching_radius: int,
                                  osm_cache_file_path: pathlib.Path) -> list[dict]:
    osm_df = load_osm_pbf_to_dataframe(osm_cache_file_path)
    dataset_out = []
    for dataset_obj in dataset:
        try:
            poi_counts = get_poi_counts_near_geolocation(
                gdf=osm_df,
                lat=float(dataset_obj["lat"]),
                long=float(dataset_obj["long"]),
                searching_radius=searching_radius,
            )
            poi_category_counts = convert_poi_tag_counts_to_category_counts(
                pois_in=poi_counts
            )
        except Exception as exc:
            # TODO: refactor exceptions handling and add logging
            print(f"Error was occurred during pois searching for id {dataset_obj['id']}, "
                  f"err_msg: {exc}")
            poi_category_counts = {}

        if not poi_category_counts:
            obj_out = {category: None for category in OSM_TAG_CATEGORIES}
        else:
            obj_out = {category: 0 for category in OSM_TAG_CATEGORIES}

        obj_out = {
            **dataset_obj,
            **obj_out,
            **poi_category_counts,
        }
        dataset_out.append(obj_out)

    return dataset_out
