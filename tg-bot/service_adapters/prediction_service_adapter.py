import json
from os import getenv

import requests
from pydantic import BaseModel


class AtmData(BaseModel):
    lat: float
    lon: float
    atm_group: float


HEADERS = {'Content-type': 'application/json', 'accept': 'application/json'}
SERVICE_URL = getenv("ATM_PROJECT_PREDICTION_SERVICE_URL")


class PredictionServiceAdapter:

    @staticmethod
    def predict(atm_data):
        return atm_data

    @staticmethod
    def get_atm_groups() -> list[float]:
        response = requests.get(f'{SERVICE_URL}/atm-groups', headers=HEADERS)
        return response.json()

    @staticmethod
    def predict_one(atm_data: AtmData) -> float | None:

        response = requests.post(
            f'{SERVICE_URL}/predict-one',
            data=atm_data.model_dump_json(),
            headers=HEADERS
        )
        if response.status_code == 200:
            return response.json()
        else:
            return None

    @staticmethod
    def predict_many(atm_data_list: list[AtmData]) -> list[float] | None:

        response = requests.post(
            f'{SERVICE_URL}/predict-many',
            data=json.dumps([atm_data.model_dump() for atm_data in atm_data_list]),
            headers=HEADERS
        )
        if response.status_code == 200:
            return response.json()
        else:
            return None
