"""
Author : Anthony Morin
Description : Main file of the Streamlit application.
"""

import streamlit as st
from scripts.data_loader import download_and_load_data, merge_coordinates_with_elus
from scripts.filters import apply_filters
from scripts.ui_components import sidebar_filters, interactive_table
from scripts.visualizations import gender_distribution_chart, department_mayor_count_chart, mayors_map

st.set_page_config(page_title="Explorateur des Élus", layout="wide")
st.title("📊 Explorateur du Répertoire National des Élus")

# Loading and processing data
with st.spinner("Chargement des données..."):
    df = download_and_load_data()
    df = merge_coordinates_with_elus(df)

# Filter
departments, gender, commune, name = sidebar_filters(df)
filtered_df = apply_filters(df, departments, gender, commune, name)

# Visualisations
st.subheader("1. Répartition hommes / femmes")
gender_distribution_chart(filtered_df)

st.subheader("2. Nombre de maires par département")
department_mayor_count_chart(filtered_df)

st.subheader("3. Carte des maires (under construction)")
# mayors_map(filtered_df)

st.subheader("4. Résultats filtrés")
interactive_table(filtered_df)
