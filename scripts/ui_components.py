"""
Author : Anthony Morin
Description : Streamlit UI display components.
"""

import pandas as pd
import streamlit as st

from config.settings import (
    APP_ICON,
    APP_INITIAL_SIDEBAR_STATE,
    APP_LAYOUT,
    COL_CODE_TERR,
    COL_GENDER_CODE,
)


def setup_page():
    """
    Configure the main settings of the Streamlit application page.

    This function sets the Streamlit page configuration, including the page title,
    icon, layout, and sidebar state, using predefined constants. It also displays
    the main title of the application at the top of the page.

    Returns
    -------
    None
        This function does not return any value but modifies the Streamlit page configuration.
    """
    st.set_page_config(
        page_title="Explorateur des Élus",
        page_icon=APP_ICON,
        layout=APP_LAYOUT,
        initial_sidebar_state=APP_INITIAL_SIDEBAR_STATE,
    )
    st.title("📊 Explorateur du Répertoire National des Élus")


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
    departments = st.sidebar.multiselect(
        "🏙️ Département ou Collectivité", territory_codes
    )
    gender = st.sidebar.multiselect(
        "👨‍⚖️👩‍⚖️ Genre :", df[COL_GENDER_CODE].dropna().unique()
    )
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
        st.write("Colonnes disponibles dans le jeu de données:")
        st.write(df.columns.tolist())
        st.dataframe(df, use_container_width=True)


def download_button(df: pd.DataFrame):
    """
    Display a download button to export the filtered dataset as a CSV file.

    Parameters
    ----------
    df : pd.DataFrame
        The filtered dataset containing information about elected officials.

    Returns
    -------
    None
        This function does not return anything. It renders a download button in the Streamlit interface.
    """
    csv = df.to_csv(index=False)
    st.download_button(
        label="Télécharger les données complètes (CSV)",
        data=csv,
        file_name="repertoire_des_elus_filtré.csv",
        mime="text/csv",
    )


def about():
    """
    Display an 'About' section in the Streamlit application.

    Returns
    -------
    None
        This function does not return any value. It outputs static content to the Streamlit interface.
    """
    st.markdown(
        """
                ### 🏛️ Source des données:
                <small>Les données proviennent du site [data.gouv.fr](https://www.data.gouv.fr/fr/datasets/repertoire-national-des-elus-1/),
                qui est la plateforme de données ouvertes du gouvernement français.</small>
                ---
                ### 🛠️ Application réalisée avec:
                - [Streamlit](https://streamlit.io) - Framework pour applications de données
                - [Pandas](https://pandas.pydata.org/) - Manipulation de données
                - [Plotly](https://plotly.com/) - Visualisations interactives
                - [PyDeck](https://deckgl.readthedocs.io/) - Cartographie interactive
        """,
        unsafe_allow_html=True
    )
