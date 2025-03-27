import streamlit as st
import pandas as pd
from io import BytesIO
from data_processing import load_data, save_data, filter_data, update_values
import base64

# Style CSS moderne
st.markdown("""
<style>
    /* Thème général */
    .stApp {
        background-color: #f4f6f9;
        font-family: 'Inter', 'Roboto', sans-serif;
    }

    /* Titre principal */
    h1 {
        color: #2c3e50;
        text-align: center;
        font-weight: 700;
        margin-bottom: 30px;
    }

    /* Conteneurs de données */
    .stDataFrame, .stForm {
        background-color: white;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        padding: 20px;
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }

    .stDataFrame:hover, .stForm:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
    }

    /* Boutons */
    .stButton>button {
        background-color: #3498db !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }

    .stButton>button:hover {
        background-color: #2980b9 !important;
        transform: scale(1.05) !important;
    }

    /* Sélecteurs et champs de saisie */
    .stSelectbox>div>div>div, 
    .stTextInput>div>div>input {
        border-radius: 8px !important;
        border: 1px solid #e0e0e0 !important;
        padding: 10px !important;
        transition: all 0.3s ease !important;
    }

    .stSelectbox>div>div>div:focus, 
    .stTextInput>div>div>input:focus {
        border-color: #3498db !important;
        box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2) !important;
    }

    /* Sections */
    h3 {
        color: #34495e;
        border-bottom: 2px solid #3498db;
        padding-bottom: 10px;
        margin-top: 30px;
    }
</style>
""", unsafe_allow_html=True)

# Charger les données
df = load_data()

# Titre de l'application
st.title("📊 Gestion des Consommations par Établissement")

# Section de filtrage avec colonnes
col1, col2 = st.columns(2)

with col1:
    # Sélectionner la colonne pour filtrer
    column_to_filter = st.selectbox(
        "Choisir une colonne de filtrage", 
        df.columns, 
        help="Sélectionnez la colonne selon laquelle vous voulez filtrer vos données"
    )

with col2:
    # Obtenir les valeurs uniques de cette colonne
    unique_values = df[column_to_filter].dropna().unique()
    selected_value = st.selectbox(
        f"Filtrer par {column_to_filter}", 
        unique_values,
        help="Sélectionnez la valeur spécifique à filtrer"
    )

# Filtrer les données
filtered_df = filter_data(df, column_to_filter, selected_value)

# Affichage des données filtrées avec un style amélioré
st.markdown("### 📋 Données Filtrées")
st.dataframe(filtered_df, use_container_width=True)

# Gestion des champs vides
cols_with_missing = filtered_df.columns[filtered_df.isnull().any()]
if len(cols_with_missing) > 0:
    st.warning("⚠️ Certains champs sont vides. Veuillez les compléter.")

    with st.form(key="data_form", clear_on_submit=True):
        st.markdown("### ➕ Ajouter des Valeurs Manquantes")
        
        new_data = {}
        for col in cols_with_missing:
            new_data[col] = st.text_input(
                f"Entrez une valeur pour {col}", 
                placeholder=f"Nouvelle valeur pour {col}"
            )

        submit_button = st.form_submit_button("✅ Sauvegarder")

        if submit_button:
            updated_df = update_values(df, new_data, column_to_filter, selected_value)
            save_data(updated_df)
            st.success("✅ Modifications enregistrées avec succès !")
            st.experimental_rerun()

# Modification des données existantes
if len(filtered_df) > 0:
    with st.form(key="edit_form", clear_on_submit=True):
        st.markdown("### ✏️ Modifier les Données Existantes")
        
        edit_data = {}
        for col in filtered_df.columns:
            edit_data[col] = st.text_input(
                f"Modifier {col}", 
                value=str(filtered_df.iloc[0][col]),
                placeholder=f"Nouvelle valeur pour {col}"
            )

        edit_button = st.form_submit_button("🔄 Mettre à Jour")

        if edit_button:
            updated_df = update_values(df, edit_data, column_to_filter, selected_value)
            save_data(updated_df)
            st.success("🔄 Modifications enregistrées avec succès !")
            st.experimental_rerun()

# Téléchargement des données
def get_excel_download_link(dataframe):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        dataframe.to_excel(writer, index=False, sheet_name="Données")
    return output.getvalue()

# Bouton de téléchargement avec style amélioré
st.markdown("### 📥 Exporter les Données")
if st.button("Télécharger en Excel", type="primary"):
    xlsx_data = get_excel_download_link(df)
    st.download_button(
        label="📂 Télécharger le fichier Excel",
        data=xlsx_data,
        file_name="Données_Modifiées.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )