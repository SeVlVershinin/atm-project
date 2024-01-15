from typing import List

from fastapi import FastAPI

from app.predictor.predictor import Predictor
from app.dto_models import AtmData



app = FastAPI()
predictor = Predictor()




# app.state.osm_gdf = None


# @app.on_event("startup")
# def load_data():
#     print("Start loading osm dataframe")
#     # osm_gdf = load_osm_pbf_to_dataframe()
#     print("Osm dataframe successfully loaded")
#     # app.state.osm_gdf = osm_gdf
#
#
# #
# #
# @app.on_event("shutdown")
# def shutdown_event():
#     print("Osm dataframe successfully unloaded")
#     # app.state.osm_gdf = None


@app.get("/atm-groups")
def get_atm_groups() -> List[str]:
    """Возвращает перечень банковских групп"""
    return ['Rosbank', 'AkBars', 'Alfabank', 'Gazprombank', 'Raiffeisen', 'Rosselkhozbank', 'Uralsib']


@app.post("/predict-one")
def predict_one(atm_data: AtmData) -> float:
    """Предсказывает индекс популярности для одного банкомата"""
    return predictor.predict([atm_data])[0]


@app.post("/predict-many")
def predict_many(atm_data_list: List[AtmData]) -> List[float]:
    """Предсказывает индекс популярности для нескольких банкоматов"""
    return predictor.predict(atm_data_list)


# uvicorn.run(app, host="0.0.0.0", port=80)
