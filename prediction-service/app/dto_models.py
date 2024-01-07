from pydantic import BaseModel


class AtmData(BaseModel):
    """Данные о банкомате, необходимые для прогнозирования индекса популярности"""
    lat: float
    lon: float
    atm_group: float
