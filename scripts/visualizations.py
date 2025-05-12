"""
Author : Anthony Morin
Description : Visualization functions (graphs, map).
"""

import streamlit as st
import plotly.express as px
import pydeck as pdk
import pandas as pd
from config import (
    COL_GENDER_CODE, COL_DEPARTMENT_NAME, COL_LAT, COL_LON, COL_NAME,
    MAP_RADIUS, MAP_ZOOM, COL_COLLEC_NAME
)

def gender_distribution_chart(df: pd.DataFrame) -> None:
    """
    Display a pie chart showing gender distribution among elected officials.

    Parameters
    ----------
    df : pd.DataFrame
        The dataset containing a column with gender codes.

    Returns
    -------
    None
        The chart is rendered directly in the Streamlit interface.
    """
    try:
        gender_counts = df[COL_GENDER_CODE].value_counts().rename(
            index={'F': 'Femmes', 'M': 'Hommes'}
        )
        fig = px.pie(names=gender_counts.index, values=gender_counts.values,
                     title="Répartition par genre",
                     color=gender_counts.index,
                     color_discrete_map={"Femmes": "pink", "Hommes": "lightblue"})
        st.plotly_chart(fig)
    except Exception as e:
        st.error(f"Erreur d'affichage du graphique par genre : {e}")

def department_mayor_count_chart(df: pd.DataFrame) -> None:
    """
    Display a horizontal scrollable bar chart showing the number of mayors per
    department or collectivity.

    Parameters
    ----------
    df : pd.DataFrame
        The dataset containing a column with department or collectivity names.

    Returns
    -------
    None
        The bar chart is rendered in the Streamlit interface.
    """
    try:
        # Create a unified label column combining department or collectivity names
        df = df.copy()
        df["territoire_label"] = df[COL_DEPARTMENT_NAME].fillna(df[COL_COLLEC_NAME])

        # Count mayors by this label
        dept_counts = df["territoire_label"].value_counts().sort_values(ascending=False)

        fig = px.bar(
            x=dept_counts.index, y=dept_counts.values,
            labels={'x': 'Département', 'y': 'Nombre de maires'},
            title="📊 Nombre de maires par département"
        )
        fig.update_layout(width=2000, height=600, xaxis_tickangle=-45)

        st.markdown('<div style="overflow-x: auto">', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=False)
        st.markdown('</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Erreur lors de l'affichage des maires : {e}")

def mayors_map(df: pd.DataFrame) -> None:
    """
    Display a geospatial map showing the location of mayors based on latitude and longitude.

    Parameters
    ----------
    df : pd.DataFrame
        The dataset containing 'latitude' and 'longitude' columns for mapping.

    Returns
    -------
    None
        A Pydeck map is rendered in the Streamlit interface.
    """
    try:
        if "latitude" not in df.columns or "longitude" not in df.columns:
            st.warning("Coordonnées manquantes pour la carte.")
            return
        if df[["latitude", "longitude"]].dropna().empty:
            st.warning("Aucune donnée géographique disponible pour les maires sélectionnés.")
            return
        df = df.dropna(subset=["latitude", "longitude"]).copy()
        df["latitude"] = df["latitude"].astype(float)
        df["longitude"] = df["longitude"].astype(float)

        df["fill_color"] = df["code_sexe"].apply(
            lambda sex: [255, 105, 180] if sex == "F" else [30, 144, 255]
)
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=df,
            get_position='[longitude, latitude]',
            get_fill_color='fill_color',
            get_radius=MAP_RADIUS,
            pickable=True
        )

        view_state = pdk.ViewState(
            latitude=df["latitude"].mean(),
            longitude=df["longitude"].mean(),
            zoom=MAP_ZOOM,
            pitch=0
        )

        st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))
    except Exception as e:
        st.error(f"Erreur lors de l'affichage de la carte : {e}")
