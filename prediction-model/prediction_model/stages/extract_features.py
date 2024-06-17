import pickle

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer

from config import Files
from ..services.features import one_hot_encode_drop_first


def extract_features(file_cfg: Files) -> None:
    with open(file_cfg.loaded_dataset) as file:
        df = pd.read_csv(file)
    df['atm_group'] = df['atm_group'].replace({
        8083.0: 'Росбанк',
        1022.0: 'АК Барс',
        1942.0: 'Альфабанк',
        3185.5: 'Газпромбанк',
        32.0: 'Райффазен',
        496.5: 'Россельхозбанк',
        5478.0: 'Уралсиб'
    })
    df.drop(["Unnamed: 0", "id", "metro", "city_area", "city_district", "city",
             "address", "address_rus"], axis=1, inplace=True)
    cols = ['education', 'fuel', 'car_service', 'parking_space', 'atm', 'bank', 'bureau_de_change',
            'outpatient_medical_facilities', 'inplace_medical_facilities', 'pharmacy', 'veterinary', 'entertainment',
            'entertainment_for_adults', 'administrative_buildings', 'police', 'fire_station', 'post_office',
            'grave_yard',
            'marketplace', 'monastery', 'place_of_worship', 'public_transport_stop_position']
    df = df[df[cols].notnull().all(axis=1)]
    df = df[df["federal_district"].notnull()]
    df = df[df["locality_area"].notnull()]
    Y = df["target"]
    X = df.drop(columns=["target"])
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=42)
    cols = ['atm_group', 'federal_district', 'region_with_type']
    X_train_enc, X_test_enc, encoder = one_hot_encode_drop_first(X_train, X_test, cols)
    scaler = StandardScaler()
    scaler.fit(X_train_enc)
    X_train_sc = scaler.transform(X_train_enc)
    X_test_sc = scaler.transform(X_test_enc)
    imp = SimpleImputer(strategy='most_frequent')
    imp.fit(X_train_sc)

    with open(file_cfg.encoder_pickle, "wb") as f:
        pickle.dump(encoder, f)
    with open(file_cfg.scaler_pickle, "wb") as f:
        pickle.dump(scaler, f)
    with open(file_cfg.imputer_pickle, "wb") as f:
        pickle.dump(imp, f)

    np.save(file_cfg.x_train_scaled, X_train_sc)
    np.save(file_cfg.y_train, y_train)
    np.save(file_cfg.x_test_scaled, X_test_sc)
    np.save(file_cfg.y_test, y_test)
