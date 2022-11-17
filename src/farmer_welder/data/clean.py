# Cleaning of datasets
import pandas as pd


def transform_education(dat: pd.DataFrame) -> pd.DataFrame:
    """
    Create variable years_of_education based on categorical variable of
    highest_education in 5467 project.

    Parameters
    ----------
    dat: pd.DataFrame
        Welders dataset.

    Returns
    -------
    dat: pd.DataFrame
        Welders dataset with years_of_education values added for 5467 project
        participants.
    """
    bool_5467 = dat['project_id'] == 5467
    replace_education = {1: 0,
                         2: 1,
                         3: 2,
                         4: 3,
                         5: 4,
                         6: 5,
                         7: 6,
                         8: 7,
                         9: 8,
                         10: 9,
                         11: 10,
                         12: 11,
                         13: 12,
                         14: 12,
                         15: 12,
                         16: 14,
                         17: 14,
                         18: 14,
                         19: 16,
                         20: 18,
                         21: 19,
                         22: 22,
                         23: 24,
                         24: 22,
                         25: -9}
    years_of_education = dat.loc[bool_5467, 'highest_education'].\
        replace(replace_education)
    dat.loc[bool_5467, 'years_of_education'] = years_of_education
    return dat


def transform_to_dummy(dat: pd.DataFrame) -> pd.DataFrame:
    """
    Transform 'sex' and 'project_id' columns to dummy variables.

    Parameters
    ----------
    dat: pd.DataFrame
        Dataset with 'sex' and 'project_id' columns.

    Returns
    -------
    dat: pd.DataFrame
        Dataset with new 'sexd' and 'project_idd' columns.
    """
    dat.loc[dat.loc[:, 'sex'] == 2, 'sexd'] = 0
    dat.loc[dat.loc[:, 'sex'] == 1, 'sexd'] = 1
    dat.loc[dat.loc[:, 'project_id'] == 37016, 'project_idd'] = 0
    dat.loc[dat.loc[:, 'project_id'] == 5467, 'project_idd'] = 1
    return dat
