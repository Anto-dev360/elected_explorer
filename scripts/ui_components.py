"""
Author : Anthony Morin
Description : Streamlit UI display components.
"""

import streamlit as st
import pandas as pd
from config import COL_DEPARTMENT_CODE, COL_GENDER_CODE, COL_CODE_TERR

def sidebar_filters(df: pd.DataFrame):
    """
    Render sidebar filters in the Streamlit UI and return selected filter values.

    Parameters
    ----------
    df : pd.DataFrame
        The dataset used to populate filter options such as departments and gender.

    Returns
    -------
    tuple
        A 4-element tuple containing:
        - departments (list): List of selected department codes.
        - gender (list): List of selected gender codes.
        - town (str): Text input for filtering town names.
        - name (str): Text input for filtering elected officials by name.
    """
    st.sidebar.title("🔍 Filtres")
    # Combine unique department and collectivity codes
    territory_codes = df[COL_CODE_TERR].dropna().unique()
    territory_codes = sorted(territory_codes)
    departments = st.sidebar.multiselect("🏙️ Département ou Collectivité", territory_codes)  
    gender = st.sidebar.multiselect("👨‍⚖️👩‍⚖️ Genre :", df[COL_GENDER_CODE].dropna().unique())
    town = st.sidebar.text_input("🏘️ Commune contient :")
    name = st.sidebar.text_input("🧑‍⚖️ Nom de l'élu contient :")
    return departments, gender, town, name

def interactive_table(df: pd.DataFrame):
    """
    Display the filtered results as an interactive data table in Streamlit.

    Parameters
    ----------
    df : pd.DataFrame
        The filtered dataset to display.

    Returns
    -------
    None
        This function directly renders the table in the Streamlit interface.
    """
    if df.empty:
        st.info("Aucun résultat à afficher.")
    else:
        st.dataframe(df, use_container_width=True)
