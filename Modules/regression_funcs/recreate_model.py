import pickle


def recreate_model(models: list = []):
    """
    Recreate regression for hfc data

    Args:
        models (list, optional): List of regressions in descsending order. Defaults to [].
    """

    models.reverse()

    regressions = {}

    for idx, model in enumerate(models):

        reg = pickle.load(open(f'./Data/models/neptune_models/regressions/{model}.pkl', 'rb'))

        regressions[f'{idx + 1}_hfc_regression'] = reg

    pickle.dump(regressions, open('./Data/models/regressions/hfc_regressions.pkl', 'wb'))

    return regressions
