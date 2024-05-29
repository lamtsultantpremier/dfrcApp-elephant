import streamlit as st
import pandas as pd
from io import StringIO
import os
from pathlib import Path
with st.sidebar:
    st.header('Navigation')
    st.image("image/elephant.png")
uploaded_file=st.file_uploader(label="Charger un fichier .CSV",type=["csv"])
rep_par_defaut="Excel"
    #creation d'une session pour le stockage du fichier
st.markdown(
        """
        <style>
            .st-emotion-cache-1jgv1qq
            {
            background-color:rgb(213, 218, 229);
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    #recuperer le fichier csv puis l'enregistrer dans un dossier séparé
if uploaded_file is not None:
        rep_par_defaut=Path(rep_par_defaut).glob("*")
        for fichier in rep_par_defaut:
            fichier.unlink()
        rep_par_defaut="Excel"
        nom_fichier=uploaded_file.name
        type_fichier=uploaded_file.type
        taille_fichier=uploaded_file.size
        st.session_state["nom_fichier"]=nom_fichier
        st.session_state["type_fichier"]=type_fichier
        st.session_state["taille_fichier"]=taille_fichier
        chemin_fichier=Path(rep_par_defaut,nom_fichier)
        st.session_state['chemin_fichier']=chemin_fichier
        with open(chemin_fichier,mode="wb") as f:
            f.write(uploaded_file.getbuffer())
if "nom_fichier" in st.session_state and "type_fichier" in st.session_state and "taille_fichier" in st.session_state:
        st.write(f"Nom du Fichier : {st.session_state["nom_fichier"]}")
        st.write(f"Type de fichier : {st.session_state["type_fichier"]}")
        st.write(f" Taille du fichier : {st.session_state["taille_fichier"]}")
        st.text("Extrait du contenu du fichier")
        df=pd.read_csv(f"./Excel/{st.session_state["nom_fichier"]}")
        st.dataframe(df.head(2))