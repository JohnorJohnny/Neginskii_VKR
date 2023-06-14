import re


def get_category_cols(df):

    category_cols = []

    for col in df.columns:

        if re.findall(r"for_cat", col):

            category_cols.append(col)

    return category_cols
