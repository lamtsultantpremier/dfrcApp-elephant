
import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
from fonctionnalite.traitement import traier_fichier
from streamlit_option_menu import option_menu
from fonctionnalite.distance import distance_par_semaine_km,distance_par_mois_km,distance_jour_km,distance_par_annee_km,distance_par_nuit_jour_km
from io import StringIO
import locale
#definir la date au format francais
locale.setlocale(locale.LC_TIME,"fr_FR.UTF-8")
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
            fig=px.line(distance_jour,x="Date",y="distance",width=600,height=500,title="Distance par Jour")
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
            date_fin_aff=date_fin.strftime("%d %b %Y")
            fig=px.bar(distance_mois,x="Date",y="distance",width=500,height=500,title=f"Courbe des distances du {date_debut_aff} au {date_fin_aff}",labels={"distance":"Distance par Mois"})
            st.plotly_chart(fig,selection_mode="points")
    if option_selected=="Distance par Année":
        distance_annee=distance_par_annee_km(df)
        col1,col2=st.columns(2)
        with col1:
            st.subheader("Distance par Année")
            st.dataframe(distance_annee)
        with col2.container(border=True): 
            fig=px.bar(distance_annee,x="Date",y="distance",width=200,height=300)
            st.plotly_chart(fig)
    distance_nuit_jour=st.radio("Distance de Jour et de Nuit",["","Distance nuit et Jour"],horizontal=True)
    if distance_nuit_jour!="Distance nuit et Jour":
            distance_nuit_jour=distance_par_nuit_jour_km(df)
            distance_nuit_jour_unstack=distance_nuit_jour.unstack()
            distance_nuit_jour_formated=distance_nuit_jour_unstack["Distance_parcourue_km"]
            dates=[]
            for index,rows in distance_nuit_jour_formated.iterrows():
                print(distance_nuit_jour_formated.loc[[index]])
                dates.append(index)
            with st.expander("Choisir une date"):
                choix=st.selectbox("",dates,index=None,placeholder="Choisir une Date")
            ##on est ICI
            if choix:
                color_sequences=["orange","yellow"]
                df=distance_nuit_jour_formated.loc[[choix]]
                col1,col2,col3=st.columns(3)
                col4,col5,col6=st.columns(3)
                dist_nuit=df["Nuit"].values[0]
                distance_jour=df["Jour"].values[0]
                data_sector={"Distance":[dist_nuit,distance_jour],"Type":["Nuit","Jour"]}
                df_sector=pd.DataFrame(data_sector)
                with col1:
                    st.text("Distance de Jour et de Nuit")
                    st.dataframe(df)
                with col3:
                    st.text("Distance")
                    st.dataframe(df_sector)
                form=px.pie(df_sector,names="Type",values="Distance",title="Distance Parcourue de Jour et de Nuit",width=500,height=500,color_discrete_sequence=["orange","gray"])
                with col5:
                    st.plotly_chart(form)
                options_compare=["Comparaison entre deux Date",""]
                choix1=st.radio("",options_compare,horizontal=True)
                if choix1=="Comparaison entre deux Date":
                    col1,col2,col3=st.columns(3)
                    with col1:
                        with st.expander("Choisi la prémière date"):
                            choix_date1=st.selectbox("Choisir une date",dates,index=None,placeholder="Choisissez la Premiere Date")
                            #selectionner la dataframe resultant de la date1
                            df_date1=distance_nuit_jour.loc[[choix_date1]]
                        st.dataframe(df_date1)
                    with col3:
                        with st.expander("Choisi la deuxieme date"):
                            choix_date2=st.selectbox("Choisir une date",dates,index=None,placeholder="Choisissez la Deuxieme Date")
                            #selectionner la dataframe resultante de la date2
                            df_date2=distance_nuit_jour.loc[[choix_date2]]
                        st.dataframe(df_date2)                     
    else:
        distance_nuit_jour=distance_par_nuit_jour_km(df)
        col1,col2=st.columns(2)
        with col1:
            st.dataframe(distance_nuit_jour)
        with col2.container(border=True):
             distance_nuit_jour_unstack=distance_nuit_jour.unstack(level="temps")
             distance_nuit_jour_formated=distance_nuit_jour_unstack["Distance_parcourue_km"]
             fig,ax=plt.subplots(figsize=(6,11))
             distance_nuit_jour_formated.plot(kind="barh",ax=ax,color={"Jour":"blue","Nuit":"orange"},grid=False)
             ax.set_xlabel('Distance_parcourue_Km')
             ax.set_ylabel('Date')
             st.pyplot(fig)
             
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