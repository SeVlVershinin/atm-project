from app.dto_models import AtmData


class Model:

    def predict(self, atm_data_list: list[AtmData]):
        return [0. for _ in atm_data_list]
