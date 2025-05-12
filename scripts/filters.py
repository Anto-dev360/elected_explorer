"""
Author : Anthony Morin
Description : Applying user filters.
"""

import pandas as pd
from config import COL_DEPARTMENT_CODE, COL_GENDER_CODE, COL_COMMUNE_NAME, COL_NAME

def apply_filters(df: pd.DataFrame, departments, gender, commune_name, name) -> pd.DataFrame:
    """
    Filter the elected officials dataset based on user-defined criteria.

    Parameters
    ----------
    df : pd.DataFrame
        The full dataset containing elected officials.
    departments : list or None
        List of selected department codes to filter on.
    gender : list or None
        List of selected gender codes to filter on ('M', 'F').
    commune_name : str
        Partial string to match against the commune name (case-insensitive).
    name : str
        Partial string to match against the official's name (case-insensitive).

    Returns
    -------
    pd.DataFrame
        A filtered DataFrame containing only rows that match the given criteria.
        If an exception occurs, an empty DataFrame is returned.
    """
    try:
        if departments:
            df = df[df[COL_DEPARTMENT_CODE].isin(departments)]
        if gender:
            df = df[df[COL_GENDER_CODE].isin(gender)]
        if commune_name:
            df = df[df[COL_COMMUNE_NAME].str.contains(commune_name, case=False, na=False)]
        if name:
            df = df[df[COL_NAME].str.contains(name, case=False, na=False)]
    except Exception as e:
        print(f"Filter error: {e}")
        return pd.DataFrame()
    return df
