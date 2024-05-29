
import pandas as pd
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu
from io import StringIO
st.set_page_config(page_title="EarthRangers",page_icon="🐘",layout="wide")
with st.sidebar:
    st.header('Navigation')
    st.image("image/elephant.png")
    infos=st.selectbox("Pattern de Mouvement",["Vitesse de déplacement","Distance parcourue"],index=None,placeholder='choisir une action')
    st.title("")#
    #st.selectbox("Dynamique de Mouvement",["Direction Geographique","Trajectoire Dominante"])
    #st.title("")
    #st.selectbox("Temps Passé à différents endroits",["Temps de marche","Temps de repos"])
    #st.button("Rapport Journalier")
if "csv_content" not in st.session_state:
    st.session_state["csv_content"]=None
    #Header
    st.subheader("🐘 Description Analytics")
    #Sidebar
    #style css
    #.st-emotion-cache-ue6h4q:classe des selectBox
    st.markdown(
        """
        <style>
            .st-emotion-cache-ue6h4q{
                color: rgb(255, 255, 255);
            }
        .b{
                text-decoration:None;
                color: rgb(255, 255, 255);
                }
        </style>
        """,
        unsafe_allow_html=True
    )
if infos=="Distance parcourue":
    options_distances=["Distance par Jour","Distance par Semaine","Distance par Mois","Distance par Année"]
    option_selected=st.radio("Distance",options_distances,horizontal=True)
    st.write(option_selected)
if "chemin_fichier" in st.session_state:
    chemin=st.session_state["chemin_fichier"]
    df=pd.read_csv(chemin)
    #st.dataframe(df)
#st-emotion-cache-1d4lk37
#col1, col2,col3,col4,col5= st.columns(5)

#with col1:
    #st.header("Colonne 1")
    #st.write("Contenu de la première colonne")

#with col2:
    #st.header("Colonne 2")
    #st.write("Contenu de la deuxième colonne")
#with col3:
    #st.header("Colonne 2")
    #st.write("Contenu de la deuxième colonne")
#with col4:
    #st.header("Colonne 2")
    #st.write("Contenu de la deuxième colonne")
#with col5:
    #st.header("Colonne 2")
    #st.write("Contenu de la deuxième colonne")

#tab1, tab2= st.tabs(["Tab 1", "Tab 2"])

# Contenu pour le premier onglet
#with tab1:
    #st.header("Contenu du premier onglet")
    #st.write("AAAA")

# Contenu pour le deuxième onglet
#with tab2:
    #st.header("Contenu du deuxième onglet")
    #st.write("AAAAA")
#st.write()