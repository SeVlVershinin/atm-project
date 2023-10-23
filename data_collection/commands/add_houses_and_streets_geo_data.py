import argparse
import csv
import os
import pathlib
from datetime import datetime

from dadata import Dadata
from dotenv import load_dotenv
from tqdm import tqdm

from exceptions import BaseGeodataGettingException


def _add_houses_and_streets_geo_data(dataset_in: list[dict]) -> list[dict]:
    dadata_client = Dadata(DADATA_API_KEY, DADATA_SECRET_KEY)
    out = dataset_in[:]
    for dataset_entry in tqdm(out):
        fias_level = dataset_entry["fias_level"]
        try:
            fias_level = int(fias_level)
        except (ValueError, TypeError):
            continue
        if fias_level < 7 or not dataset_entry["fias_id"]:
            continue
        dadata_response = dadata_client.find_by_id("address", dataset_entry["fias_id"])
        if not dadata_response or (geo_data := dadata_response[0].get("data")) is None:
            continue
        if fias_level == 8:
            dataset_entry["house_fias_id"] = dataset_entry["fias_id"]
            dataset_entry["house"] = geo_data["house"]
        dataset_entry["street"] = geo_data["street"]
    return out


if __name__ == "__main__":
    load_dotenv()
    DADATA_API_KEY = os.getenv("DADATA_API_KEY")
    DADATA_SECRET_KEY = os.getenv("DADATA_SECRET_KEY")

    arg_parser = argparse.ArgumentParser(
        description=(
            "The script makes requests to the DaData API. For fias_id fields with"
            "level 8 gets the house number by ID."
        )
    )
    arg_parser.add_argument("dataset_filename", type=str,
                            help="location of dataset csv file")
    dataset_path = pathlib.Path(arg_parser.parse_args().dataset_filename)
    dataset = []
    with open(dataset_path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            dataset.append(row)
    if not dataset:
        raise BaseGeodataGettingException("Failed to get data from csv file")

    dataset_out = _add_houses_and_streets_geo_data(dataset)

    today = datetime.today().strftime("%d_%m_%y")

    out_filename = f"with_houses_{today}_{dataset_path.name}"
    with open(out_filename, "w") as csvfile:
        field_names_to_write = tuple(dataset[0].keys())
        writer = csv.DictWriter(csvfile, fieldnames=field_names_to_write)
        writer.writeheader()
        for entry in dataset:
            writer.writerow(entry)
