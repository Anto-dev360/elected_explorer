"""
Author : Anthony Morin
Description : Main file of the Streamlit application.
"""

import streamlit as st

from scripts.data_loader import download_and_load_data, merge_coordinates_with_elec
from scripts.filters import apply_filters
from scripts.ui_components import (
    about,
    download_button,
    interactive_table,
    setup_page,
    sidebar_filters,
)
from scripts.visualizations import (
    department_mayor_count_chart,
    gender_distribution_chart,
    mayors_map,
    profession_analysis_chart,
)


def main():
    """
    Main entry point for the Streamlit application. This function orchestrates the various steps involved in setting up
    the application, loading the data, applying filters, and displaying the user interface with different sections and tabs.

    The application allows the user to explore French elected officials data, with features such as:
    - Gender distribution.
    - Map of mayors.
    - Visualizations of mayor statistics by department.
    - A table of filtered results.
    - Information about the data source and the technologies used.

    Parameters
    ----------
    None

    Returns
    -------
    None
        The function renders the entire Streamlit application interface.
    """
    # Configure streamlit layout.
    setup_page()

    # Introduction.
    st.markdown(
        """
        Bienvenue dans l’**Explorateur du Répertoire National des Élus** 🇫🇷.
        Cette application vous permet d'explorer les données publiques des élus français : répartition par genre, cartographie, par département, et plus encore.
        """
    )
    st.markdown("---")

    # Loading and processing data.
    with st.spinner("⏳ Chargement des données..."):
        df = download_and_load_data()
        df = merge_coordinates_with_elec(df)

    # Sidebar filters.
    departments, gender, town, name = sidebar_filters(df)
    filtered_df = apply_filters(df, departments, gender, town, name)

    # Sum up.
    st.subheader("📌 Résumé")
    col1, col2, col3 = st.columns(3)
    col1.metric("Élus affichés", f"{len(filtered_df):,}")
    col2.metric("Départements", filtered_df["code_du_departement"].nunique())
    pct_femmes = filtered_df["code_sexe"].value_counts(normalize=True).get("F", 0) * 100
    col3.metric("Femmes %", f"{pct_femmes:.1f} %")
    st.markdown("---")

    # Creating tabs.
    tab1, tab2, tab3, tab4 = st.tabs(
        ["Carte", "Visualisations", "Tableau de données", "À propos"]
    )

    # Map tab.
    with tab1:
        st.subheader("🗺️ Carte des maires")
        mayors_map(filtered_df)

    # Visualisations tab.
    with tab2:
        st.subheader("👥 Répartition hommes / femmes")
        gender_distribution_chart(filtered_df)
        st.markdown("---")

        st.subheader("🏛️ Nombre de maires par département")
        department_mayor_count_chart(filtered_df)
        st.markdown("---")

        st.subheader("👔 Catégories socio-professionnelles les plus représentées")
        profession_analysis_chart(filtered_df)

    # Result tab.
    with tab3:
        st.subheader("📋 Résultats filtrés")
        with st.expander("🔍 Afficher les élus filtrés (tableau)"):
            interactive_table(filtered_df)

        download_button(filtered_df)

    # About tab.
    with tab4:
        about()


if __name__ == "__main__":
    main()
