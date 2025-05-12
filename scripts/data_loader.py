"""
Author : Anthony Morin
Description : Loading and enriching data.
"""

import pandas as pd
import streamlit as st
import unicodedata
from scripts.utils import download_if_not_exists
from config import DATA_URL, COMMUNES_URL, COL_COMMUNE_CODE

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
    elus_path = "data/elus.csv"
    download_if_not_exists(DATA_URL, elus_path)
    try:
        with open(elus_path, "rb") as f:
            df = pd.read_csv(f, sep=";", encoding="utf-8-sig", dtype=str)
        df.columns = [normalize_column(col) for col in df.columns]
        return df
    except Exception as e:
        st.error(f"Erreur de chargement des données des élus : {e}")
        return pd.DataFrame()

@st.cache_data(show_spinner=False)
def merge_coordinates_with_elus(df_elus: pd.DataFrame) -> pd.DataFrame:
    """
    Merge latitude and longitude into the elected officials dataset using INSEE commune codes.

    Parameters
    ----------
    df_elus : pd.DataFrame
        DataFrame containing elected officials with commune codes.

    Returns
    -------
    pd.DataFrame
        Merged DataFrame with 'latitude' and 'longitude' columns added.
    """
    communes_path = "data/communes.csv"
    download_if_not_exists(COMMUNES_URL, communes_path)

    try:
        with open(communes_path, "rb") as f:
            communes_df = pd.read_csv(f, sep=",", encoding="utf-8-sig", dtype=str)
        communes_df.columns = [normalize_column(col) for col in communes_df.columns]
        communes_df = communes_df.rename(columns={"code_commune_insee": COL_COMMUNE_CODE})

        # Work on copies to keep function pure for caching
        df_elus = df_elus.copy()
        communes_df = communes_df.copy()

        df_elus[COL_COMMUNE_CODE] = df_elus[COL_COMMUNE_CODE].astype(str)
        communes_df[COL_COMMUNE_CODE] = communes_df[COL_COMMUNE_CODE].astype(str)

        merged_df = pd.merge(
            df_elus,
            communes_df[[COL_COMMUNE_CODE, "latitude", "longitude"]],
            on=COL_COMMUNE_CODE,
            how="left"
        )
        return merged_df

    except Exception as e:
        st.error(f"Erreur lors de la fusion avec les coordonnées : {e}")
        return df_elus

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
    col_name = col_name.strip().lower().replace(" ", "_")
    col_name = unicodedata.normalize('NFKD', col_name).encode('ASCII', 'ignore').decode('utf-8')
    return col_name
