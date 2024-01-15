from typing import List
from fastapi import FastAPI

from app.predictor.ml_model import Predictor
from app.dto_models import AtmData
# from app.configs import Settings
# from app.data_collection import extend_original_atm_dataset


app = FastAPI()
model = Predictor()

# settings = Settings()


@app.get("/atm-groups")
def get_atm_groups() -> List[str]:
    """Возвращает перечень банковских групп"""
    return ['Rosbank', 'AkBars', 'Alfabank', 'Gazprombank', 'Raiffeisen', 'Rosselkhozbank', 'Uralsib' ]


@app.post("/predict-one")
def predict_one(atm_data: AtmData) -> float:
    """Предсказывает индекс популярности для одного банкомата"""
    return model.predict([atm_data])[0]


@app.post("/predict-many")
def predict_many(atm_data_list: List[AtmData]) -> List[float]:
    """Предсказывает индекс популярности для нескольких банкоматов"""
    # out = extend_original_atm_dataset(
    #     dataset=atm_data_list,
    #     dadata_api_key=settings.dadata_api_key,
    #     dadata_secret=settings.dadata_secret_key,
    #     geo_tree_api_key=settings.geo_tree_secret_key,
    # )
    # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    # print(out)
    # TODO: finalize dataset extending script
    return model.predict(atm_data_list)



uvicorn.run(app, host="0.0.0.0", port=80)
