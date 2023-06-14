import numpy as np
from sklearn.metrics import mean_squared_error, r2_score


def calculate_metrics(model, X_train, X_valid, y_train, y_valid):

    metrics = {'train': {}, 'valid': {}}

    y_train_pred = np.clip(model.predict(X_train), 2, None)

    metrics['train']['RMSE'] = np.float64(round(np.sqrt(mean_squared_error(y_train_pred, y_train)), 3))
    metrics['train']['R2'] = np.float64(round(r2_score(y_train, y_train_pred), 3))
    metrics['train']['wape'] = np.round(sum(abs(y_train - y_train_pred)) / sum(y_train) * 100, 2)
    metrics['train']['mean'] = np.float64(round(np.mean(y_train[y_train != 0]), 3))
    metrics['train']['median'] = np.float64(round(np.median(y_train[y_train != 0]), 3))

    y_valid_pred = np.clip(model.predict(X_valid), 2, None)

    metrics['valid']['RMSE'] = np.float64(round(np.sqrt(mean_squared_error(y_valid_pred, y_valid)), 3))
    metrics['valid']['R2'] = np.float64(round(r2_score(y_valid, y_valid_pred), 3))
    metrics['valid']['wape'] = np.round(sum(abs(y_valid - y_valid_pred)) / sum(y_valid) * 100, 2)
    metrics['valid']['mean'] = np.float64(round(np.mean(y_valid[y_valid != 0]), 3))
    metrics['valid']['median'] = np.float64(round(np.median(y_valid[y_valid != 0]), 3))

    print(metrics)

    print('\nWA: ', (y_valid_pred.sum() - y_valid.sum()) / y_valid.sum())

    return metrics
