import pathlib
from pprint import pprint

from dadata import Dadata
from tqdm import tqdm

from ..exceptions import (
    NotFoundCoreException,
    ValidationCoreException,
    InvalidParametersCoreException,
)
from ..schemas import (
    DatasetObjectWithGeoData,
    FilteredGeoData,
    OriginalGeoData,
    InitialDatasetObject,
    OSM_TAG_CATEGORIES,
)
from ..services import (
    convert_poi_tag_counts_to_category_counts,
    get_extended_geo_data_from_dadata,
    get_population_stats_by_oktmo_list,
    get_poi_counts_near_geolocation,
    load_osm_pbf_to_dataframe,
    merge_initial_dataset_object_with_geo_data,
)


def extend_initial_dataset_with_geo_data(dataset: list[dict],
                                         dadata_client: Dadata,
                                         geo_tree_api_key: str) -> list[dict]:
    # TODO: add docstring
    dataset = dataset[5000:]
    dataset_out = {}
    geocoding_warnings = []
    oktmo_set = set()
    for dataset_item in tqdm(dataset):
        dataset_object = InitialDatasetObject.model_validate(dataset_item)
        geo_object = OriginalGeoData.model_validate(dataset_item)
        try:
            geocoding_out = get_extended_geo_data_from_dadata(
                geo_object,
                dadata_client
            )
        except (NotFoundCoreException,
                InvalidParametersCoreException,
                ValidationCoreException) as exc:
            geocoding_warnings.append({
                "id": dataset_object.id,
                "geocoding_warnings": [str(exc)]
            })
            continue
        if geocoding_out.warnings:
            geocoding_warnings.append({
                "id": dataset_object.id,
                "geocoding_warnings": geocoding_out.warnings,
            })
        dataset_out[dataset_item["id"]] = DatasetObjectWithGeoData.model_validate({
            **dataset_object.model_dump(),
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
    for dataset_item in tqdm(dataset):
        geolocation = dataset_out.get(dataset_item["id"])
        oktmo = geolocation.oktmo if geolocation else None
        filtered_geolocation = FilteredGeoData.model_validate(geolocation.model_dump()) \
            if geolocation else None
        population_status = population_out.population_stats.get(oktmo)
        out.append(
            merge_initial_dataset_object_with_geo_data(
                initial_dataset_obj=dataset_item,
                geolocation=filtered_geolocation,
                population_stats=population_status,
            )
        )

    return out


def extend_dataset_with_pois_data(dataset: list[dict],
                                  searching_radius: int,
                                  osm_cache_file_path: pathlib.Path) -> list[dict]:
    osm_df = load_osm_pbf_to_dataframe(osm_cache_file_path)
    dataset_out = []
    for dataset_obj in tqdm(dataset):
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
