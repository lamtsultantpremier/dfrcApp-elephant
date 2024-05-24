import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import pandas as pd

###Fonctionnement de plotly###
#Plotly permet de faire des diagramme interactif#
st.title("Plotly graphics")
temps=pd.DataFrame({
    "day":['Monday',"Tuesday","Wenesday","Thursday","Friday","Saturday","Sunday"],
    "temperature":[28,27,26,25,35,37,26],
})
#Diagramme à bande interactif
fig=px.bar(data_frame=temps,x="day",y="temperature", title="Temperature Journalière")
st.plotly_chart(fig)

#nuage de point interactif
cars=pd.read_csv("Automobile_data.csv").head(200)
st.dataframe(cars)
numerics_col=cars.select_dtypes(exclude=["object"]).columns.to_list()
categoriel_col=cars.select_dtypes(include=["object"]).columns.to_list()
st.write(numerics_col)
var_x=st.selectbox("Choisi la variable en Abscisse",numerics_col)
var_y=st.selectbox("Choisi la variable en ordonnée",numerics_col)
var_color=st.selectbox("Choisir la valeur caracteriel des abscisse",categoriel_col)

fig1=px.scatter(
    data_frame=cars,
    x=var_x,
    y=var_y,
    color=var_color
)
st.plotly_chart(fig1)

#Exemple de graphe seaborn et matplotlib
#Avec seaborn
airbnb=pd.read_csv("new_york.csv")
st.subheader("Seaborn")
fig_ax,ax_sb=plt.subplots()
ax_sb=sns.histplot(airbnb["availability_365"])
plt.xlabel("Nombre de jour disponible")
st.pyplot(fig_ax)

#Exemple Avec Matplotlib
fig_mt,ax_mat=plt.subplots()
ax_mt=plt.hist(airbnb["availability_365"])
plt.xlabel("Nombre de jour disponible")
plt.ylabel("Y")
st.pyplot(fig_mt)