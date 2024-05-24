import pandas as pd
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu
from io import StringIO

if "csv_content" not in st.session_state:
    st.session_state["csv_content"]=None

st.set_page_config(page_title="EarthRangers",page_icon="🐘",layout="wide")
#Header
st.subheader("🐘 Description Analytics")

#Sidebar
st.sidebar.image("image/elephant.png")
#style css
st.markdown(
    """
    <style>
    </style>
    """,
    unsafe_allow_html=True
)
if "nom_fichier" in st.session_state: 
    df=pd.read_csv(f"./Excel/{st.session_state["nom_fichier"]}")
    st.dataframe(df)
