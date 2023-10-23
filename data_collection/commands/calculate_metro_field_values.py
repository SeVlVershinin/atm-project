import argparse
import csv
import pathlib
from datetime import datetime

from dotenv import load_dotenv

from exceptions import BaseGeodataGettingException


if __name__ == "__main__":
    load_dotenv()
    arg_parser = argparse.ArgumentParser(
        description=(
            "The script copies non-zero values of field `metro_distance_1` "
            "to field `metro`,"
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

    for entry in dataset:
        if entry["metro_distance_1"]:
            entry["metro"] = entry["metro_distance_1"]

    today = datetime.today().strftime("%d_%m_%y")
    out_filename = f"calculated_metro_{today}_{dataset_path.name}"
    field_names_to_write = list(dataset[0].keys())

    with open(out_filename, "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names_to_write)
        writer.writeheader()
        for entry in dataset:
            writer.writerow(entry)
