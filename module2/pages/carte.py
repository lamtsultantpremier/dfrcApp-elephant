import streamlit as st
import folium as f
from streamlit_folium import st_folium
if "df" not in st.session_state:
    st.write("df is not defined")
else:
    with st.sidebar:
        carte=st.selectbox("Carte",["Zone les plus fréquentés","Carte de chaleur"],index=None,placeholder="choisissez une action")
    df=st.session_state["df"]
    first_record=df.head(1)
    first_lat=first_record['Latitude'].values[0]
    first_long=fird=first_record["Longitude"].values[0]
    first_date=first_record["Date_Enregistrement"].values[0]
    first_hour=first_record["Heure_Enregistrement"].values[0]
    st.write("Carte de représentation")
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
    