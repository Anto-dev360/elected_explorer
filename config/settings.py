"""
Author : Anthony Morin
Description : Application constants.
"""

# URL of the dataset
DATA_URL = "https://www.data.gouv.fr/fr/datasets/r/2876a346-d50c-4911-934e-19ee07b0e503"

# URL for the coordinates of French communes
TOWN_URL = "https://www.data.gouv.fr/fr/datasets/r/dbe8a621-a9c4-4bc3-9cae-be1699c5ff25"

# Column name constants (standardized for internal use)
COL_DEPARTMENT_CODE = "code_du_departement"
COL_DEPARTMENT_NAME = "libelle_du_departement"
COL_COLLEC_CODE = "code_de_la_collectivite_a_statut_particulier"
COL_COLLEC_NAME = "libelle_de_la_collectivite_a_statut_particulier"
COL_TOWN_CODE = "code_de_la_commune"
COL_TOWN_NAME = "libelle_de_la_commune"
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
COL_CODE_TERR = "code_territoire"

# Coordinates
COL_LAT = "latitude"
COL_LON = "longitude"

# Map view defaults
MAP_ZOOM = 5
MAP_RADIUS = 300
MAP_RADIUS_MIN_PX = 3
MAP_RADIUS_MAX_PX = 12

# UI constants
APP_ICON = "🗳️"
APP_LAYOUT = "wide"
APP_INITIAL_SIDEBAR_STATE = "expanded"
