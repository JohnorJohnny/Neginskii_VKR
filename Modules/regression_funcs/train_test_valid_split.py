import gc
import pandas as pd
from sklearn.model_selection import train_test_split


def train_test_valid_split(df, high_threshold, train_cols, y_col, predict: bool = False):

    if predict:

        df_train = df[df["Период"] < high_threshold]
        df_valid = df[(df["Период"] >= high_threshold - pd.DateOffset(months=2)) & (df["Период"] < high_threshold)]

    else:

        df_train = df[df["Период"] < high_threshold - pd.DateOffset(months=1)]
        df_valid = df[(df["Период"] >= high_threshold - pd.DateOffset(months=1)) & (df["Период"] < high_threshold)]

    print(f"Validation periiod: {df_valid['Период'].min()} - {df_valid['Период'].max()}, include left and right side")

    del df
    gc.collect()
    gc.collect()

    X_train, X_test, y_train, y_test = train_test_split(df_train[train_cols], df_train[y_col], shuffle=True, random_state=0, test_size=0.2)

    del df_train
    gc.collect()
    gc.collect()

    X_valid, y_valid = df_valid[train_cols], df_valid[y_col]

    del df_valid
    gc.collect()
    gc.collect()

    return X_train, X_test, X_valid, y_train, y_test, y_valid
