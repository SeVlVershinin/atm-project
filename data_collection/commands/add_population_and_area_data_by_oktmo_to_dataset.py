import argparse
import csv
import os
import pathlib
import requests
from datetime import datetime

from dadata import Dadata
from dotenv import load_dotenv
from tqdm import tqdm
from ratelimiter import RateLimiter


@RateLimiter(max_calls=10, period=1)
def _execute_search_by_oktmo_api_request(
        oktmo: str,
        api_key: str,
) -> list[dict]:
    payload = {
        "key": api_key,
        "oktmo_list": oktmo,
    }
    response = requests.get("https://api.geotree.ru/search.php", params=payload)
    response.raise_for_status()
    return response.json()


def _get_population_and_areas_by_fias(
        localities_fias: set | list,
        dadata_client: Dadata,
        geotree_api_key: str,
) -> dict:
    out = {}
    for fias_code in tqdm(localities_fias):
        dadata_response = dadata_client.find_by_id("address", fias_code)
        if not dadata_response or (geo_data := dadata_response[0].get("data")) is None:
            continue
        geotree_response = _execute_search_by_oktmo_api_request(
            geo_data["oktmo"],
            geotree_api_key,
        )
        if geotree_response and (response_item := geotree_response[0]):
            out[fias_code] = {
                "area": response_item["area"],
                "population": response_item["population"],
            }
    return out


if __name__ == "__main__":
    load_dotenv()
    GEO_TREE_SECRET_KEY = os.getenv("GEO_TREE_SECRET_KEY")
    DADATA_API_KEY = os.getenv("DADATA_API_KEY")
    DADATA_SECRET_KEY = os.getenv("DADATA_SECRET_KEY")

    arg_parser = argparse.ArgumentParser(
        description=(
            "The script receives fias codes of cities and settlements specified "
            "in the csv file. Using the dadata service the script receives "
            "oktmo codes, then using the geotree.ru service the script receives "
            "data on the population of cities and settlements and returns "
            "a new dataset with the filled columns `locality_population`, "
            "`locality_area`"
        )
    )
    arg_parser.add_argument("dataset_filename", type=str,
                            help="location of dataset csv file")
    dataset_path = pathlib.Path(arg_parser.parse_args().dataset_filename)
    dataset = []
    cities_fias = set()
    settlements_fias = set()
    with open(dataset_path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            dataset.append(row)
            if row.get("locality_population"):
                continue
            if row["city_fias_id"]:
                cities_fias.add(row["city_fias_id"])
            if row["settlement_fias_id"]:
                settlements_fias.add(row["settlement_fias_id"])

    dadata_client = Dadata(DADATA_API_KEY, DADATA_SECRET_KEY)
    search_out_by_cities_fias = _get_population_and_areas_by_fias(
        cities_fias,
        dadata_client,
        GEO_TREE_SECRET_KEY,
    )
    search_out_by_settlements_fias = _get_population_and_areas_by_fias(
        settlements_fias,
        dadata_client,
        GEO_TREE_SECRET_KEY,
    )

    for entry in dataset:
        if entry.get("locality_population"):
            continue
        if entry["city_fias_id"]:
            population_and_area = search_out_by_cities_fias.get(
                entry["city_fias_id"]
            )
        elif entry["settlement_fias_id"]:
            population_and_area = search_out_by_settlements_fias.get(
                entry["settlement_fias_id"]
            )
        else:
            continue
        if population_and_area is None:
            continue
        entry["locality_area"] = population_and_area["area"]
        entry["locality_population"] = population_and_area["population"]

    today = datetime.today().strftime("%d_%m_%y")
    out_filename = f"with_population_{today}_{dataset_path.name}"
    with open(out_filename, "w") as csvfile:
        field_names_to_write = tuple(dataset[0].keys())
        writer = csv.DictWriter(csvfile, fieldnames=field_names_to_write)
        writer.writeheader()
        for entry in dataset:
            writer.writerow(entry)
