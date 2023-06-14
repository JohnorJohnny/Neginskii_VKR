from Modules.regression_funcs.translit import translit


def rename_columns(df):

    df = df.rename(
        columns=lambda x: translit(
            x.replace(" ", "_")
            .replace("-", "_")
            .replace(",", "_")
            .replace("(k)", "k")
            .replace("<", "smaller_then")
        )
    )

    return df
