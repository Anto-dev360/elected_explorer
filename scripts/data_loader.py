"""
Author : Anthony Morin
Description : Loading and enriching data.
"""

import unicodedata

import pandas as pd
import streamlit as st

from config.settings import (
    COL_CODE_TERR,
    COL_COLLEC_CODE,
    COL_DEPARTMENT_CODE,
    COL_TOWN_CODE,
    DATA_URL,
    TOWN_URL,
)
from scripts.utils import download_if_not_exists


@st.cache_data(show_spinner=False)
def download_and_load_data(url: str = DATA_URL) -> pd.DataFrame:
    """
    Download and load the dataset of elected officials from data.gouv.fr if not already cached.

    Parameters
    ----------
    url : str, optional
        URL to the CSV dataset of elected officials. Defaults to the DATA_URL constant.

    Returns
    -------
    pd.DataFrame
        A cleaned DataFrame with normalized column names, or an empty DataFrame if loading fails.
    """
    elec_path = "data/elus.csv"
    download_if_not_exists(DATA_URL, elec_path)
    try:
        with open(elec_path, "rb") as f:
            df = pd.read_csv(f, sep=";", encoding="utf-8-sig", dtype=str)
        df.columns = [normalize_column(col) for col in df.columns]
        df[COL_CODE_TERR] = df[COL_DEPARTMENT_CODE].fillna(df[COL_COLLEC_CODE])
        return df
    except Exception as e:
        st.error(f"Erreur de chargement des données des élus : {str(e)}")
        return pd.DataFrame()


@st.cache_data(show_spinner=False)
def merge_coordinates_with_elec(df_elec: pd.DataFrame) -> pd.DataFrame:
    """
    Merge latitude and longitude into the elected officials dataset using INSEE town codes.

    Parameters
    ----------
    df_elec : pd.DataFrame
        DataFrame containing elected officials with town codes.

    Returns
    -------
    pd.DataFrame
        Merged DataFrame with 'latitude' and 'longitude' columns added.
    """
    town_path = "data/communes.csv"
    download_if_not_exists(TOWN_URL, town_path)

    try:
        with open(town_path, "rb") as f:
            town_df = pd.read_csv(f, sep=",", encoding="utf-8-sig", dtype=str)
        town_df.columns = [normalize_column(col) for col in town_df.columns]
        town_df = town_df.rename(columns={"code_commune_insee": COL_TOWN_CODE})

        # Work on copies to keep function pure for caching
        df_elec = df_elec.copy()
        town_df = town_df.copy()

        # Ensure proper formatting of INSEE codes
        df_elec[COL_TOWN_CODE] = df_elec[COL_TOWN_CODE].astype(str).str.zfill(5)
        town_df[COL_TOWN_CODE] = town_df[COL_TOWN_CODE].astype(str).str.zfill(5)

        merged_df = pd.merge(
            df_elec,
            town_df[[COL_TOWN_CODE, "latitude", "longitude"]],
            on=COL_TOWN_CODE,
            how="left",
        )
        return merged_df

    except Exception as e:
        st.error(f"Erreur lors de la fusion avec les coordonnées :{str(e)}")
        return df_elec


def normalize_column(col_name):
    """
    Normalize a column name by removing accents, lowercasing, and replacing spaces with underscores.

    Parameters
    ----------
    col_name : str
        Original column name from the dataset.

    Returns
    -------
    str
        A normalized column name ready for consistent internal processing.
    """
    col_name = (
        col_name.strip().lower().replace(" ", "_").replace("'", "_").replace("-", "_")
    )
    col_name = (
        unicodedata.normalize("NFKD", col_name)
        .encode("ASCII", "ignore")
        .decode("utf-8")
    )
    return col_name
