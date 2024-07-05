import streamlit as st
import folium as f
import matplotlib.pyplot as plt
from streamlit_folium import st_folium
import datetime
import requests
import plotly.express as px
import pandas as pd
from fonctionnalite.zone_frequentation import distance_dbscan,make_cluster,find_location
if "df" not in st.session_state:
    st.write("Veuillez Charger un fichier avant de continuer")
else:
    df=st.session_state["df"]
    with st.sidebar:
        carte=st.selectbox("Carte",["","Zone les plus fréquentés","Carte de chaleur"],index=0,placeholder="Choisir une action")
    if carte=="":
        first_record=df.head(1)
        first_lat=first_record['Latitude'].values[0]
        first_long=fird=first_record["Longitude"].values[0]
        first_date=first_record["Date_Enregistrement"].values[0]
        first_hour=first_record["Heure_Enregistrement"].values[0]
        html=f"""
            <h5>Date: {first_date}</h5>
            <p>Longitude: {first_long}</p>
            <p>Latitude: {first_lat}</p>
            <p>Heure: {first_hour}</p>
        """ 
        iframe=f.IFrame(html,width=200,height=200)
        popup=f.Popup(iframe,max_width=300)
        map=f.Map(location=(first_lat,first_long),zoom_start=10)
        icon=f.CustomIcon("image/elephant_marker.png",icon_size=(12,12))
        f.Marker([first_lat,first_long],popup=popup,icon=icon).add_to(map)
        st_folium(map,width=1000)
    if carte=="Zone les plus fréquentés":
        options=["Gaphe des Zones","Visulaisation des Zones de Forte Frequentations"]
        zone_frequenter=st.radio("",options,index=0,horizontal=True)
        if zone_frequenter=="Gaphe des Zones":
            col4,col5=st.columns(2)
            latitudes=[]
            longitudes=[]
            dates_times=[]
            datimes=[]
            col1,col2=st.columns(2)
             #reserver à l'affichage sur matplolib
            if "nom_elephant" in st.session_state:
                nom_elephant=st.session_state["nom_elephant"]
            df_for_trajet=df[["Date_Enregistrement","Heure_Enregistrement","Latitude","Longitude"]]
            for index,rows in df_for_trajet.iterrows():
                latitudes.append(float(rows["Latitude"]))
                longitudes.append(float((rows["Longitude"])))
                dates_times.append(datetime.datetime.combine(rows["Date_Enregistrement"],rows["Heure_Enregistrement"]))
            for date_time in dates_times:
                datimes.append(str(date_time))
            dataframes_from_trajet=pd.DataFrame({"Latitude":latitudes,"Longitude":longitudes,"date":datimes})
            #Afficher les differentes date de debut et de Fin
            date_debut=dataframes_from_trajet.tail(1)["date"].values[0]
            date_fin=dataframes_from_trajet.head(1)["date"].values[0]
            #afficher les longitude et latitudes
            date_debut=date_debut.split(" ")[0]
            date_fin=date_fin.split(" ")[0]
            fig=px.scatter(dataframes_from_trajet,x="Longitude",y="Latitude",hover_data={"date":True,"Longitude":True,"Latitude":True},title=f"Position {nom_elephant} du {date_debut} au {date_fin}")
            fig.update_layout({"width":900,"height":300})
            st.plotly_chart(fig)
            st.write("")
            #determine the different cluster
            epsilon=distance_dbscan(df)
            if epsilon!=0.0:
                df_cluster=make_cluster(df,epsilon)
               #zones proches des endroits de concentrations
                df_lieux_proche=find_location(df_cluster)
                st.write("Lieux Proches des Zones de fortes concentration")
                st.dataframe(df_lieux_proche)            
                fig=px.scatter(df_cluster,x="Longitude",y="Latitude",title=f"Zone de Forte Fréquentation {nom_elephant} du {date_debut} au {date_fin}",color="cluster",labels={"cluster":"niveau de Frequentation"})
                st.plotly_chart(fig)
            else:
                df_cluster=make_cluster(df,0.03)
                #zones proches des endroits de concentrations
                df_lieux_proche=find_location(df_cluster)
                st.write("Lieux Proches des Zones de fortes concentration")
                st.dataframe(df_lieux_proche)
                fig=px.scatter(df_cluster,x="Longitude",y="Latitude",title=f"Zone de Forte Fréquentation {nom_elephant} du {date_debut} au {date_fin}",color="cluster")
                st.plotly_chart(fig)
        elif zone_frequenter=="Visulaisation des Zones de Forte Frequentations":
            st.write("Bonjour")
            epsilon=distance_dbscan(df)
            if epsilon!=0.0:
                df_cluster=make_cluster(df,epsilon)
                st.dataframe(df_cluster)
            else:
               df_cluster=make_cluster(df,0.02)
               st.dataframe(df_cluster)
    elif carte=="Carte de chaleur":
        options=["liste des Points","Carte des chaleurs"]
        carte_selected=st.radio("",options,index=0,horizontal=True)
        st.write(carte_selected)
