
"""
Author : Anthony Morin
Description : Application constants.
"""

# URL of the dataset
DATA_URL = "https://www.data.gouv.fr/fr/datasets/r/2876a346-d50c-4911-934e-19ee07b0e503"

# URL for the coordinates of French communes
COMMUNES_URL = "https://www.data.gouv.fr/fr/datasets/r/dbe8a621-a9c4-4bc3-9cae-be1699c5ff25"

# Column name constants (standardized for internal use)
COL_DEPARTMENT_CODE = "code_du_departement"
COL_DEPARTMENT_NAME = "libelle_du_departement"
COL_COMMUNE_CODE = "code_de_la_commune"
COL_COMMUNE_NAME = "libelle_de_la_commune"
COL_SECTOR = "libelle_du_secteur"
COL_NAME = "nom_de_l_elu"
COL_FIRSTNAME = "prenom_de_l_elu"
COL_GENDER_CODE = "code_sexe"
COL_BIRTHDATE = "date_de_naissance"
COL_BIRTHPLACE = "lieu_de_naissance"
COL_SOCIOPRO_CODE = "code_de_la_categorie_socio_professionnelle"
COL_SOCIOPRO_LABEL = "libelle_de_la_categorie_socio_professionnelle"
COL_MANDATE_START = "date_de_debut_du_mandat"
COL_FUNCTION_LABEL = "libelle_de_la_fonction"
COL_FUNCTION_START = "date_de_debut_de_la_fonction"

# Coordinates
COL_LAT = "latitude"
COL_LON = "longitude"

# Map view defaults
MAP_ZOOM = 5
MAP_COLOR = [200, 30, 0, 160]
MAP_RADIUS = 300