import argparse
import csv
import os
import pathlib
import requests
from datetime import datetime

from dotenv import load_dotenv
from tqdm import tqdm
from ratelimiter import RateLimiter


@RateLimiter(max_calls=10, period=1)
def _execute_search_api_request(term: str,
                                api_key: str,
                                lat: str | float | None = None,
                                lon: str | float | None = None) -> list[dict]:
    payload = {
        "key": api_key,
        "term": term,
    }
    if lat and lon:
        payload["lat"] = lat
        payload["lon"] = lon
    response = requests.get("https://api.geotree.ru/search.php", params=payload)
    response.raise_for_status()
    return response.json()


def _get_population_and_areas_by_localities(localities: dict, api_key: str) -> dict:
    out = {}
    blank_responses_count = 0
    geo_inside_false_count = 0
    wrong_level_count = 0
    for locality_key, locality_value in tqdm(localities.items()):
        response_json = _execute_search_api_request(
            term=locality_key,
            api_key=api_key,
            lat=locality_value["lat"],
            lon=locality_value["lon"]
        )
        if not response_json:
            response_json = _execute_search_api_request(
                term=locality_value["locality"],
                api_key=api_key,
                lat=locality_value["lat"],
                lon=locality_value["lon"]
            )
        if not response_json:
            blank_responses_count += 1
            continue
        first_item = response_json[0]
        if not first_item.get("geopoint"):
            geo_inside_false_count += 1
            continue
        if int(first_item["level"]) != 4:
            wrong_level_count += 1
        out[locality_key] = {
            "area": first_item["area"],
            "name_source": first_item["name_source"],
            "description": first_item["description"],
            "level": first_item["level"],
            "population": first_item["population"],
        }
    return out


if __name__ == "__main__":
    load_dotenv()
    GEO_TREE_SECRET_KEY = os.getenv("GEO_TREE_SECRET_KEY")

    arg_parser = argparse.ArgumentParser(
        description=(
            "The script receives the names of cities and settlements specified "
            "in the csv file. Using the geotree.ru service, the script receives "
            "data on the population of cities and settlements and returns "
            "a new dataset with the added columns 'locality_population', "
            "'locality_area'"
        )
    )
    arg_parser.add_argument("dataset_filename", type=str,
                            help="location of dataset csv file")
    dataset_path = pathlib.Path(arg_parser.parse_args().dataset_filename)
    dataset = []
    localities_by_dataset_ids = {}
    localities = {}
    with open(dataset_path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            dataset.append(row)
            locality = ""
            region = ""
            if row["city_with_type"] is not None:
                locality = row["city_with_type"]
            elif row["settlement_with_type"] is not None:
                locality = row["settlement_with_type"]
            else:
                continue

            if row["region_with_type"] is not None:
                region = row["region_with_type"]

            locality_lat, locality_lon = None, None
            if row["city_lat"] and row["city_lon"]:
                locality_lat = row["city_lat"]
                locality_lon = row["city_lon"]
            elif row["settlement_lat"] and row["settlement_lon"]:
                locality_lat = row["settlement_lat"]
                locality_lon = row["settlement_lon"]

            locality_with_region = " ".join((locality, region))
            if ((locality_item := localities.get(locality_with_region)) is None) \
                    or (not locality_item["lat"] and not locality_item["lon"]
                        and locality_lat and locality_lon):
                localities[locality_with_region] = {
                    "lat": locality_lat,
                    "lon": locality_lon,
                    "locality": locality,
                    "region": region,
                }
            localities_by_dataset_ids[row["id"]] = locality_with_region

    search_out_by_localities = _get_population_and_areas_by_localities(
        localities,
        GEO_TREE_SECRET_KEY,
    )

    for entry in dataset:
        entry_id = entry["id"]
        locality_key = localities_by_dataset_ids.get(entry_id)
        if not locality_key:
            entry["locality_area"] = None
            entry["locality_population"] = None
            continue
        locality_data = search_out_by_localities.get(locality_key)
        if not locality_data:
            entry["locality_area"] = None
            entry["locality_population"] = None
            continue
        entry["locality_area"] = locality_data["area"]
        entry["locality_population"] = locality_data["population"]

    today = datetime.today().strftime("%d_%m_%y")
    out_filename = f"with_population_{today}_{dataset_path.name}"
    with open(out_filename, "w") as csvfile:
        field_names_to_write = tuple(dataset[0].keys())
        writer = csv.DictWriter(csvfile, fieldnames=field_names_to_write)
        writer.writeheader()
        for entry in dataset:
            writer.writerow(entry)
