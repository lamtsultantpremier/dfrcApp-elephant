import streamlit as st
import pandas as pd
import numpy as np
st.title("Initialisation à la DataVizualisation")
#Definir l'auteur du document
st.subheader("Auteur : Lamine")
st.markdown("***Un site pour la viz de donnée***")
#dessiner un diagramee à bar
bar_data=pd.DataFrame(
   [1,3,6],["Attieke","Oiseaux","poisson"]
)
st.line_chart(bar_data)
df=pd.read_csv("data.csv").head(100)
df.rename(columns={"lng":"longitude","lat":"latitude"},inplace=True)
st.map(df[["longitude","latitude"]])