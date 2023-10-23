import argparse
import csv
import os
import pathlib
from datetime import datetime

from dadata import Dadata
from dotenv import load_dotenv
from tqdm import tqdm

from exceptions import BaseGeodataGettingException


def _clarify_geo_data(dataset_in: list[dict]) -> list[dict]:
    field_names_to_update = (
        "area_fias_id",
        "area_with_type",
        "city_with_type",
        "city_fias_id",
        "federal_district",
        "capital_marker",
        "fias_id",
        "fias_level",
        "region_with_type",
        "region_fias_id",
        "settlement_with_type",
        "settlement_fias_id",
        "street_with_type",
        "street_fias_id",
    )
    dadata_client = Dadata(DADATA_API_KEY, DADATA_SECRET_KEY)
    out = dataset_in[:]
    updated_rows_count = 0
    updated_row_ids = []
    for dataset_entry in tqdm(out):
        fias_level = dataset_entry["fias_level"]
        try:
            fias_level = int(fias_level)
        except (ValueError, TypeError):
            continue
        if fias_level < 8 and dataset_entry["address_rus"]:
            dadata_response = dadata_client.clean("address", dataset_entry["address_rus"])
            new_fias_level = dadata_response["fias_level"]
            try:
                new_fias_level = int(new_fias_level)
            except (ValueError, TypeError):
                continue
            if new_fias_level <= fias_level:
                continue
            updated_rows_count += 1
            updated_row_ids.append(dataset_entry["id"])
            dataset_entry["lat"] = dadata_response["geo_lat"]
            dataset_entry["long"] = dadata_response["geo_lon"]
            for key in field_names_to_update:
                dataset_entry[key] = dadata_response[key]
    print(f"updated {updated_rows_count} rows with ids: {updated_row_ids}")
    return out


if __name__ == "__main__":
    load_dotenv()
    DADATA_API_KEY = os.getenv("DADATA_API_KEY")
    DADATA_SECRET_KEY = os.getenv("DADATA_SECRET_KEY")

    arg_parser = argparse.ArgumentParser(
        description=(
            "The script tries to collect updated geodata for rows that have "
            "a fias_id and its level below 8 and have a text address. For such "
            "rows, a request is made to the DaData API with the address string."
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

    dataset_out = _clarify_geo_data(dataset)

    today = datetime.today().strftime("%d_%m_%y")

    out_filename = f"clarified_{today}_{dataset_path.name}"
    with open(out_filename, "w") as csvfile:
        field_names_to_write = tuple(dataset[0].keys())
        writer = csv.DictWriter(csvfile, fieldnames=field_names_to_write)
        writer.writeheader()
        for entry in dataset:
            writer.writerow(entry)
