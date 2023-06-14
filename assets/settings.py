"""
Constants.
"""


PRED_WEEK = "2022-01-01"
KEY_COLS = ["Артикул", "КлиентКод"]
CAT_COLS = [
    "Канал",
    "Код клиента1 С",
    "Регион",
    "КлиентКод",
    "Сегмент",
    "ФО",
    "ТипЦен",
    "Артикул",
    'ВидЦены'
]
N_COUNTS_FOR_PRED = 4
PREDICTION_LEN = 7
PREV_COLS_LEN = 360

MARK = "half-year" if PREV_COLS_LEN >= 180 else "year" if PREV_COLS_LEN >= 360 else None

PREV_COLS = ["prev_" + str(i) for i in range(1, PREV_COLS_LEN + 1)][::-1]
PREV_COLS_DAYS = ["prev_" + str(i) + "_day" for i in range(1, 31)][::-1]


SKU_FILE = "Data/entry_data/SKU.xlsx"
ADDRESSES_FILE = "Data/entry_data/contragents.xlsx"
PATNERS_FILE = "Data/entry_data/clients.xlsx"
OLD_DATA_FILE = "Data/entry_data/Fact/old_fact.txt"
NEW_DATA_FILE = "Data/entry_data/Fact/append_fact.txt"
DATA_FILE = "Data/entry_data/Fact/final_fact.txt"
CATEGORY_ENCODEDERS_FOLDER = 'Data/models/encoders/'

ALPH = {
    "ь": "",
    "ъ": "",
    "а": "a",
    "б": "b",
    "в": "v",
    "г": "g",
    "д": "d",
    "е": "e",
    "ё": "yo",
    "ж": "zh",
    "з": "z",
    "и": "i",
    "й": "y",
    "к": "k",
    "л": "l",
    "м": "m",
    "н": "n",
    "о": "o",
    "п": "p",
    "р": "r",
    "с": "s",
    "т": "t",
    "у": "u",
    "ф": "f",
    "х": "h",
    "ц": "ts",
    "ч": "ch",
    "ш": "sh",
    "щ": "sch",
    "ы": "yi",
    "э": "e",
    "ю": "yu",
    "я": "ya",
}
