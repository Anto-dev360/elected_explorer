"""
Author : Anthony Morin
Description : Main file of the Streamlit application.
"""

import streamlit as st
from scripts.data_loader import download_and_load_data, merge_coordinates_with_elec
from scripts.filters import apply_filters
from scripts.ui_components import sidebar_filters, interactive_table
from scripts.visualizations import gender_distribution_chart, department_mayor_count_chart, mayors_map

st.set_page_config(page_title="Explorateur des Élus", layout="wide")
st.title("📊 Explorateur du Répertoire National des Élus")

# Introduction
st.markdown("""
Bienvenue dans l’**Explorateur du Répertoire National des Élus** 🇫🇷.  
Cette application vous permet d'explorer les données publiques des élus français : répartition par genre, cartographie, par département, et plus encore.  
*Source : [data.gouv.fr](https://www.data.gouv.fr/fr/datasets/repertoire-national-des-elus/)*  
""")

st.markdown("---")

# Loading and processing data
with st.spinner("⏳ Chargement des données..."):
    df = download_and_load_data()
    df = merge_coordinates_with_elec(df)

# Sidebar filters
departments, gender, town, name = sidebar_filters(df)
filtered_df = apply_filters(df, departments, gender, town, name)

# Sum up
st.subheader("📌 Résumé")
col1, col2, col3 = st.columns(3)
col1.metric("Élus affichés", f"{len(filtered_df):,}")
col2.metric("Départements", filtered_df["code_du_departement"].nunique())
pct_femmes = filtered_df["code_sexe"].value_counts(normalize=True).get("F", 0) * 100
col3.metric("Femmes %", f"{pct_femmes:.1f} %")

st.markdown("---")

# Visualisations
st.subheader("1️⃣ 👥 Répartition hommes / femmes")
gender_distribution_chart(filtered_df)

st.markdown("---")

st.subheader("2️⃣ 🏛️ Nombre de maires par département")
department_mayor_count_chart(filtered_df)

st.markdown("---")

st.subheader("3️⃣ 🗺️ Carte des maires")
mayors_map(filtered_df)

st.markdown("---")

st.subheader("4️⃣ 📋 Résultats filtrés")
with st.expander("🔍 Afficher les élus filtrés (tableau)"):
    interactive_table(filtered_df)

st.markdown("""
---
🛠️ Application réalisée avec [Streamlit](https://streamlit.io)
""")