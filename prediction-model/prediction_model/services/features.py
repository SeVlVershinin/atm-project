import pandas as pd
from sklearn.preprocessing import OneHotEncoder


def one_hot_encode_drop_first(X_train, X_test, cols):
    drop_enc = OneHotEncoder(drop='first', handle_unknown='ignore').fit(X_train[cols])

    X_train_enc = pd.DataFrame(drop_enc.transform(X_train[cols]).toarray(),
                               columns=drop_enc.get_feature_names_out(cols),
                               dtype=int)
    X_test_enc = pd.DataFrame(drop_enc.transform(X_test[cols]).toarray(),
                              columns=drop_enc.get_feature_names_out(cols),
                              dtype=int)

    X_train_enc = X_train_enc.reset_index(drop=True)
    X_test_enc = X_test_enc.reset_index(drop=True)
    X_train = X_train.reset_index(drop=True)
    X_test = X_test.reset_index(drop=True)

    X_train_enc = pd.concat([X_train.drop(columns=cols), X_train_enc], axis=1)
    X_test_enc = pd.concat([X_test.drop(columns=cols), X_test_enc], axis=1)

    return X_train_enc, X_test_enc, drop_enc
