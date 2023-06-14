import base64
import gc
import hashlib
import os
import pickle
import sys
import time
import warnings

import lightgbm as lgb
# import dvc.api
import neptune
import pandas as pd
import yaml
from neptune.integrations.lightgbm import (NeptuneCallback,
                                           create_booster_summary)

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))  # noqa: E402
from assets.settings import (N_COUNTS_FOR_PRED,  # noqa: E402
                             PRED_WEEK, PREDICTION_LEN)
from Modules import regression_funcs as regf  # noqa: E402
from Modules.preprocessing_funcs.get_category_cols import \
    get_category_cols  # noqa: E402

warnings.filterwarnings('ignore')


with open("assets/params.yaml", "r") as stream:

    try:

        params = yaml.safe_load(stream)

    except yaml.YAMLError as exc:

        print(exc)
        raise

lgbm_params = params['regression']['params']
num_boost_round = params['regression']['num_boost_round']
verbose_eval = params['regression']['verbose_eval']


models = {}

run_type = 'hfwc_model_'
hasher = hashlib.sha1(str(time.time()).encode("UTF-8"))
run_type += base64.urlsafe_b64encode(hasher.digest()[:10]).decode("utf-8").rstrip('=')

for week in range(1, N_COUNTS_FOR_PRED + 1):

    df = pd.read_parquet('Data/prepared/train/main_data.gzip')

    train_cols = regf.get_train_columns(df)
    y_col = f'BaseLine_{week}_week'

    high_threshold_for_each_model = pd.Timestamp(PRED_WEEK) - pd.Timedelta(days=PREDICTION_LEN * week)

    print(high_threshold_for_each_model)

    X_train, X_test, X_valid, y_train, y_test, y_valid = regf.train_test_valid_split(df, high_threshold_for_each_model, train_cols, y_col, predict=True)

    del df

    gc.collect()
    gc.collect()

    X_train = regf.rename_columns(X_train)
    X_test = regf.rename_columns(X_test)
    X_valid = regf.rename_columns(X_valid)

    category_cols = get_category_cols(X_train)

    train_data = lgb.Dataset(X_train, y_train, free_raw_data=False)
    test_data = lgb.Dataset(X_test, y_test, free_raw_data=False)

    run = neptune.init_run(
        api_token='eyJhcGlfYWRkcmVzcyI6Imh0dHBzOi8vYXBwLm5lcHR1bmUuYWkiLCJhcGlfdXJsIjoiaHR0cHM6Ly9hcHAubmVwdHVuZS5haSIsImFwaV9rZXkiOiI5NTJlYjRkNS04NWVmLTRlNzAtOThjOC1jNjA1ZDc0YzQ2ZGMifQ==',
        project='johnorjohnny/Practice',
    )

    run["sys/tags"].add("High frequency weekly customers model")

    neptune_callback = NeptuneCallback(run=run)

    run['run_type'] = run_type
    run['model_type'] = 'regression'

    lgbm_reg = lgb.train(
        lgbm_params,
        train_set=train_data,
        valid_sets=[train_data, test_data],
        num_boost_round=num_boost_round,
        verbose_eval=verbose_eval,
        callbacks=[neptune_callback],
        categorical_feature=category_cols,
    )

    print('\nObjective: ', lgbm_params['objective'])

    metrics = regf.calculate_metrics(lgbm_reg, X_train, X_valid, y_train, y_valid)

    models[f'{week}_model'] = lgbm_reg

    try:

        run["lgbm_summary"] = create_booster_summary(
            booster=lgbm_reg,
            log_trees=True,
            tree_figsize=60,
            list_trees=[0, 1, 2, 3, 4],
        )

    except Exception:

        pass

    try:

        run['valid_rmse'].append(metrics['valid']['RMSE'])
        run['valid_r2'].append(metrics['valid']['R2'])
        run['valid_wape'].append(metrics['valid']['wape'])
        run['train_r2'].append(metrics['train']['R2'])
        run['train_wape'].append(metrics['train']['wape'])

    except Exception:
        pass

    run.stop()

    del X_train, X_test, X_valid, y_train, y_test, y_valid, train_data, test_data

    gc.collect()
    gc.collect()

    time.sleep(15)

    gc.collect()
    gc.collect()

pickle.dump(models, open('Data/models/final_models/main_model.pkl', 'wb'))
