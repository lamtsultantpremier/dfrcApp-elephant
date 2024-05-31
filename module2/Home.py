
import pandas as pd
import streamlit as st
import plotly.express as px
from fonctionnalite.traitement import traier_fichier
from streamlit_option_menu import option_menu
from fonctionnalite.distance import distance_par_semaine_km,distance_par_mois_km,distance_jour_km,distance_par_annee_km
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
if "chemin_fichier" in st.session_state:
    chemin=st.session_state["chemin_fichier"]
    df=traier_fichier(chemin)
    df=df.sort_values(by="Date_Enregistrement",ascending=False)
    st.session_state["df"]=df
    st.dataframe(df)
if infos=="Distance parcourue":
    options_distances=["Distance par Jour","Distance par Semaine","Distance par Mois","Distance par Année"]
    option_selected=st.radio("Distance",options_distances,horizontal=True)
    if option_selected=="Distance par Jour":
        st.write(option_selected)
        col1,col2=st.columns(2)
        with col1:
            st.subheader("Distance par Jour")
            distance_jour=distance_jour_km(df)
            st.dataframe(distance_jour)
        with col2.container(border=True):
            fig=px.line(distance_jour,x="Date",y="distance",width=500,height=400,title="Distance par Jour")
            st.plotly_chart(fig,selection_mode="points")
    if option_selected=="Distance par Semaine":
        distance_semaine=distance_par_semaine_km(df)
        col1,col2=st.columns(2)
        with col1:
            st.subheader("Distance par Semaine")
            st.dataframe(distance_semaine)
        with col2.container(border=True):
            fig=px.line(distance_semaine,x="Date",y="distance",width=500,height=500,title="Distance par Semaine")
            st.plotly_chart(fig,selection_mode="points")
    if option_selected=="Distance par Mois":
        distance_mois=distance_par_mois_km(df)
        col1,col2=st.columns(2)
        with col1:
            st.subheader("Distance par Mois")
            st.dataframe(distance_mois)
        with col2.container(border=True):
            first_record=distance_mois.head(1)
            last_record=distance_mois.tail(1)
            date_debut=pd.to_datetime(first_record["Date"]).dt.date[0]
            date_fin=pd.to_datetime(last_record["Date"]).dt.date[len(distance_mois)-1]
            date_debut_aff=date_debut.strftime("%d %b %Y")
            date_fin_aff=date_fin.strftime("%d %b %y")
            st.write((date_debut_aff))
            st.write(date_fin_aff)
            fig=px.bar(distance_mois,x="Date",y="distance",width=500,height=450)
            st.plotly_chart(fig,selection_mode="points")
    if option_selected=="Distance par Année":
        distance_annee=distance_par_annee_km(df)
        col1,col2=st.columns(2)
        with col1:
            st.subheader("Distance par Année")
            st.dataframe(distance_annee)
        with col2.container(border=True):
            fig=px.bar(distance_annee,x="Date",y="distance",width=250,height=400,title="Distance par Année")
            st.plotly_chart(fig)
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