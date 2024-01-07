from typing import List
from fastapi import FastAPI

from app.ml_model import Model
from app.dto_models import  AtmData


app = FastAPI()
model = Model()


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
    return model.predict(atm_data_list)



# uvicorn.run(app, host="0.0.0.0", port=80)
