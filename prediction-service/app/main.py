from typing import List
from fastapi import FastAPI

from app.ml_model import Model
from app.dto_models import AtmData
from app.configs import Settings
from app.data_collection import extend_original_atm_dataset


app = FastAPI()
model = Model()

settings = Settings()


@app.get("/atm-groups")
def get_atm_groups() -> List[float]:
    """Возвращает перечень банковских групп"""
    return [12., 43., 54., 32., 456., 32., 5454.]


@app.post("/predict-one")
def predict_one(atm_data: AtmData) -> float:
    """Предсказывает индекс популярности для одного банкомата"""
    return model.predict([atm_data])[0]


@app.post("/predict-many")
def predict_many(atm_data_list: List[AtmData]) -> List[float]:
    """Предсказывает индекс популярности для нескольких банкоматов"""
    out = extend_original_atm_dataset(
        dataset=atm_data_list,
        dadata_api_key=settings.dadata_api_key,
        dadata_secret=settings.dadata_secret_key,
        geo_tree_api_key=settings.geo_tree_secret_key,
    )
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(out)
    # TODO: finalize dataset extending script
    return model.predict(atm_data_list)



# uvicorn.run(app, host="0.0.0.0", port=80)
