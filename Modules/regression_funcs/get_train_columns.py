from assets.settings import CAT_COLS, KEY_COLS, N_COUNTS_FOR_PRED

DELS = [
    "zeros_masses",
    "last_zeros_len",
    "zeros_mass_mean",
    "zeros_mass_median",
    "zeros_mass_std",
    "zeros_mass_cnt",
    "zeros_mass_max",
]


def get_train_columns(df):

    train_cols = df.columns.difference(
        KEY_COLS
        + CAT_COLS
        + DELS
        + ["Период", "ПериодМесяц", "BaseLine", "НаименованиеПродукта1С",
            "Код клиента1 С", "КодПродукта1С", "Наименование логического клиента",
            'max_preiod_article_client', 'min_preiod_article_client', 'Объем',
            'count_of_base_purchases', 'count_of_promo_purchases', 'count_of_purchases',
            'Promo']
        + [f"BaseLine_{j}_week" for j in range(1, N_COUNTS_FOR_PRED + 1)]
    )

    return train_cols
