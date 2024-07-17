import streamlit as st
import folium as f
import matplotlib.pyplot as plt
from streamlit_folium import st_folium
import datetime
import requests
import plotly.express as px
import pandas as pd
from fonctionnalite.zone_frequentation import distance_dbscan,make_cluster,find_location,number_in_index,color,generate_and_download_image,generate_and_download_image_heatmap
from fonctionnalite.distance import distance,dist_jour_nuit
from selenium import webdriver
import os
from folium.plugins import HeatMap
import branca
import branca.colormap as cm
from collections import defaultdict
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
        icon=f.CustomIcon("image/elephant_marker.png",icon_size=(20,20))
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
            epsilon=distance_dbscan(df)
            if epsilon!=0.0:
                df_cluster=make_cluster(df,epsilon)
                c=color(df_cluster)
                m=f.Map(location=[df_cluster["Latitude"].mean(),df_cluster["Longitude"].mean()],zoom_start=9)
                for index,row in df_cluster.iterrows():
                    f.CircleMarker(location=[row["Latitude"],row["Longitude"]],
                    raduis=0.3,
                    fill=True,
                    fill_opacity=1,
                    ).add_to(m)
                st_folium(m,width=1000)        
            else:
               df_cluster=make_cluster(df,0.02)
               m=f.Map(location=[df_cluster["Latitude"].mean(),df_cluster["Longitude"].mean()],zoom_start=9)
               for index,row in df_cluster.iterrows():
                    f.CircleMarker(location=[row["Latitude"],row["Longitude"]],
                    raduis=0.3,
                    fill=True,
                    fill_opacity=1,
                    ).add_to(m)
               st_folium(m,width=1000)
               generate_and_download_image()
    elif carte=="Carte de chaleur":
        options=["liste des Points","Carte des chaleurs"]
        carte_selected=st.radio("",options,index=0,horizontal=True)
        if carte_selected=="Carte des chaleurs":
            cart_chaleur_options=["Mode claire","Mode sombre"]
            cart_chaleur_selected=st.radio("",cart_chaleur_options,horizontal=True)
            if cart_chaleur_selected=="Mode claire":
                    epsilon=distance_dbscan(df)
                    if epsilon!=0.0:
                        df_cluster=make_cluster(df,epsilon)
                        heat_map=f.Map(location=[df_cluster["Latitude"].mean(),df_cluster["Longitude"].mean()],zoom_start=9)
                        max_heat=df_cluster["cluster"].max()
                        min_heat=df_cluster["cluster"].min()
                        heatmap_data_max=[
                            [row["Latitude"],row["Longitude"],int(max_heat)] for index,row in df_cluster.iterrows()
                                    ]
                        heatmap_data_min=[
                            [row["Latitude"],row["Longitude"],int(min_heat)] for index,row in df_cluster.iterrows()
                                        ]
                        heatmap_max=HeatMap(heatmap_data_max,name="Eleve")
                        heatmap_min=HeatMap(heatmap_data_min,name="Faible")
                        heatmap_max.add_to(heat_map)
                        heatmap_min.add_to(heat_map)
                        #f.TileLayer('cartodbdark_matter').add_to(heat_map)
                        f.LayerControl().add_to(heat_map)
                        st_folium(heat_map,width=1000)
                        heat_map.save('carte_de_chaleur_claire.html')
                        file_name='carte_de_chaleur_claire.html'
                        nom_elephant=st.session_state['nom_elephant']
                        generate_and_download_image_heatmap(file_name,nom_elephant)
                    else:
                        df_cluster=make_cluster(df,0.02)
                        df_cluster['Latitude']=df_cluster['Latitude'].astype(float)
                        df_cluster['Longitude']=df_cluster['Longitude'].astype(float)
                        df['cluster']=df_cluster['cluster'].astype(int)
                        heat_map=f.Map(location=[df_cluster["Latitude"].mean(),df_cluster["Longitude"].mean()],zoom_start=9)
                        max_heat=df_cluster["cluster"].max().astype(int)
                        min_heat=df_cluster["cluster"].min().astype(int)
                        heatmap_data_max=[
                            [row["Latitude"],row["Longitude"],int(max_heat)] for index,row in df_cluster.iterrows()
                        ]
                        heatmap_data_min=[
                            [row["Latitude"],row["Longitude"],int(min_heat)] for index,row in df_cluster.iterrows()
                        ]
                        gradient_map=defaultdict(dict)
                        heatmap_max=HeatMap(heatmap_data_max,name="Eleve")
                        heatmap_min=HeatMap(heatmap_data_min,name="Faible")
                        heatmap_max.add_to(heat_map)
                        heatmap_min.add_to(heat_map)
                        f.LayerControl().add_to(heat_map)
                        st_folium(heat_map,width=1000)
                        heat_map.save('carte_de_chaleur_claire.html')
                        file_name='carte_de_chaleur_claire.html'
                        nom_elephant=st.session_state['nom_elephant']
                        generate_and_download_image_heatmap(file_name,nom_elephant)
            elif cart_chaleur_selected=="Mode sombre":
                    epsilon=distance_dbscan(df)
                    if epsilon!=0.0:
                        df_cluster=make_cluster(df,epsilon)
                        heat_map=f.Map(location=[df_cluster["Latitude"].mean(),df_cluster["Longitude"].mean()],tiles='cartodbdark_matter',zoom_start=9)
                        max_heat=df_cluster["cluster"].max()
                        min_heat=df_cluster["cluster"].min()
                        heatmap_data_max=[
                            [row["Latitude"],row["Longitude"],int(max_heat)] for index,row in df_cluster.iterrows()
                                    ]
                        heatmap_data_min=[
                            [row["Latitude"],row["Longitude"],int(min_heat)] for index,row in df_cluster.iterrows()
                                        ]
                        heatmap_max=HeatMap(heatmap_data_max,name="Eleve")
                        heatmap_min=HeatMap(heatmap_data_min,name="Faible")
                        heatmap_max.add_to(heat_map)
                        heatmap_min.add_to(heat_map)
                        f.LayerControl().add_to(heat_map)
                        st_folium(heat_map,width=1000)
                        heat_map.save('carte_de_chaleur_sombre.html')
                        file_name='carte_de_chaleur_sombre.html'
                        nom_elephant=st.session_state['nom_elephant']
                        generate_and_download_image_heatmap(file_name,nom_elephant)
                    else:
                        df_cluster=make_cluster(df,0.02)
                        df_cluster['Latitude']=df_cluster['Latitude'].astype(float)
                        df_cluster['Longitude']=df_cluster['Longitude'].astype(float)
                        df['cluster']=df_cluster['cluster'].astype(int)
                        heat_map=f.Map(location=[df_cluster["Latitude"].mean(),df_cluster["Longitude"].mean()],tiles='cartodbdark_matter',zoom_start=9)
                        max_heat=df_cluster["cluster"].max().astype(int)
                        min_heat=df_cluster["cluster"].min().astype(int)
                        heatmap_data_max=[
                            [row["Latitude"],row["Longitude"],int(max_heat)] for index,row in df_cluster.iterrows()
                        ]
                        heatmap_data_min=[
                            [row["Latitude"],row["Longitude"],int(min_heat)] for index,row in df_cluster.iterrows()
                        ]
                        gradient_map=defaultdict(dict)
                        heatmap_max=HeatMap(heatmap_data_max,name="Eleve")
                        heatmap_min=HeatMap(heatmap_data_min,name="Faible")
                        heatmap_max.add_to(heat_map)
                        heatmap_min.add_to(heat_map)
                        f.LayerControl().add_to(heat_map)
                        st_folium(heat_map,width=1000)
                        heat_map.save('carte_de_chaleur_sombre.html')
                        file_name='carte_de_chaleur_sombre.html'
                        nom_elephant=st.session_state['nom_elephant']
                        generate_and_download_image_heatmap(file_name,nom_elephant)
        elif carte_selected=="liste des Points":
            data_display=df[["Longitude","Latitude","Date_Enregistrement","Heure_Enregistrement","temps"]]
            st.subheader("Données cartographiques")
            st.text(f"Nom Elephant:{st.session_state["nom_elephant"]}")
            st.text(f"Nombre de données {len(df)}")
            st.text(f"Date debut: {df.head(1)["Date_Enregistrement"].values[0]}")
            st.text(f"Date Fin: {df.tail(1)["Date_Enregistrement"].values[0]}")
            st.dataframe(data_display)
            col1,col2=st.columns(2)
               
            with col1:
                st.write("Distance Totale en Km")
                distance=distance(df)
                df_distance=pd.DataFrame({"Distance_total":[f"{distance} Km"]})
                st.dataframe(df_distance)
            with col2:
                st.write("Distance de Nuit et Jour en Km")
                data=dist_jour_nuit(df)
                data1=data.unstack(level="temps",fill_value=0)
                dist_nuit=data1["Nuit"].sum()
                dist_jour=data1["Jour"].sum()
                data_n_j=pd.DataFrame({"Distance Nuit":[f"{dist_nuit} Km"],"Distance Jour":[f"{dist_jour} Km"]})
                st.dataframe(data_n_j)
            st.text("")
            st.text("")
            map=f.Map(location=[df["Latitude"].astype(float).mean(),df["Longitude"].astype(float).mean()],zoom_start=9)
            st_folium(map,width=1000)
            
           


        
                       
                        




            
                


