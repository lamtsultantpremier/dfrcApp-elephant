import pandas as pd
from geopy.distance import geodesic
"""Permet de definir les differentes distances parcourues par l'éléphant
"""
def distance_par_jour_km(dataframe):
    #conversion du dataframe en numeric
    dist_total=0
    for i in range(1,len(dataframe)):
        prev_long=dataframe["Longitude"].iloc[i-1]
        prev_lati=dataframe["Latitude"].iloc[i-1]
        prev_pos=(prev_lati,prev_long)
        cur_long=dataframe["Longitude"].iloc[i]
        cur_lati=dataframe["Latitude"].iloc[i]
        cur_pos=(cur_lati,cur_long)
        distance=geodesic(prev_pos,cur_pos).km
        #distance total de chaque groupe
        dist_total+=distance
    return dist_total
#Fin de la fonction

def distance_par_jour_metre(dataframe):
    #conversion du dataframe en numeric
    dataframe["Longitude"]=pd.to_numeric(dataframe["Longitude"],errors='coerce')
    dataframe["Latitude"]=pd.to_numeric(dataframe["Latitude"],errors='coerce')
    distances=[]
    for i in range(1,len(dataframe)):
        prev_long=dataframe["Longitude"].iloc[i-1]
        prev_lati=dataframe["Latitude"].iloc[i-1]
        prev_pos=(prev_lati,prev_long)
        cur_long=dataframe["Longitude"].iloc[i]
        cur_lati=dataframe["Latitude"].iloc[i]
        cur_pos=(cur_lati,cur_long)
        distance=geodesic(prev_pos,cur_pos).m
        distances.append(distance)
    #distance total de chaque groupe
    dist_total=sum(distances)
    return dist_total
#Fin de la fonction

#distance par jour et nuit en kilometre retourne un dataframe multi-index
def distance_par_nuit_jour_km(dt):
    dt1=dt.groupby(by=["Date_Enregistrement","temps"]).apply(distance_par_jour_km)
    dt1=pd.DataFrame(dt1)
    dt1.rename(columns={0:"Distance_parcourue_km"},inplace=True)
    return dt1
#fin de la fonction

#distance par jour et nuit en metre
def distance_par_nuit_jour_m(dt):
    dt1=dt.groupby(by=["Date_Enregistrement","temps"]).apply(distance_par_jour_metre)
    dt1=pd.DataFrame(dt1)
    dt1.rename(columns={0:"Distance_parcourue_m"},inplace=True)
    return dt1
#fin de la fonction

#distance par semaine en Km
def distance_par_en_semaine_km(dt):
    dt2=dt.groupby(pd.Grouper(level="Date_Enregistrement",freq="W",sort=True))
    distances=[]
    index=[]
    date_debut_fin=[]
    group_name=[]
    for nom_groupe,groupe in dt2:
        grouped=groupe.groupby(level="Date_Enregistrement")
        #Faire la somme des distances de chaque groupe
        distance=grouped.apply(distance_par_jour_km).sum()
        #convertir la Timestamps en dateTime puis au format dd/mm/yy
        date_debut=groupe.index.min().to_pydatetime().date().strftime("%d-%m-%Y")
        #convertir la Timestamps en dateTime puis au format dd/mm/yy
        date_fin=groupe.index.max().to_pydatetime().date().strftime("%d-%m-%Y")
        date_debut_fin.append(date_debut+"/"+date_fin)
        distances.append(distance)
        #dataframe=pd.DataFrame(dataframe,columns=[nom_groupe],index=[nom_groupe])
        dataframe={"Date":date_debut_fin,"distance_parcourue_Km":distances}
        dataframe=pd.DataFrame(dataframe)
    return dataframe
#fin de la fonction

#distance par semaine en mettre
def distance_par_en_semaine_metre(dt):
    dt2=dt.groupby(pd.Grouper(level="Date_Enregistrement",freq="W",sort=True))
    distances=[]
    index=[]
    date_debut_fin=[]
    group_name=[]
    for nom_groupe,groupe in dt2:
        grouped=groupe.groupby(level="Date_Enregistrement")
        #Faire la somme des distances de chaque groupe
        distance=grouped.apply(distance_par_jour_metre).sum()
        #convertir la Timestamps en dateTime puis au format dd/mm/yy
        date_debut=groupe.index.min().to_pydatetime().date().strftime("%d-%m-%Y")
        #convertir la Timestamps en dateTime puis au format dd/mm/yy
        date_fin=groupe.index.max().to_pydatetime().date().strftime("%d-%m-%Y")
        date_debut_fin.append(date_debut+"/"+date_fin)
        distances.append(distance)
        #dataframe=pd.DataFrame(dataframe,columns=[nom_groupe],index=[nom_groupe])
        dataframe={"Date":date_debut_fin,"distance_parcourue_Metre":distances}
        dataframe=pd.DataFrame(dataframe)
    return dataframe
#fin de la fonction

#distance par mois en metre
def distance_par_en_mois_metre(dt):
    dt2=dt.groupby(pd.Grouper(level="Date_Enregistrement",freq="M",sort=True))
    distances=[]
    index=[]
    date_debut_fin=[]
    group_name=[]
    for nom_groupe,groupe in dt2:
        grouped=groupe.groupby(level="Date_Enregistrement")
        #Faire la somme des distances de chaque groupe
        distance=grouped.apply(distance_par_jour_metre).sum()
        #convertir la Timestamps en dateTime puis au format dd/mm/yy
        date_debut=groupe.index.min().to_pydatetime().date().strftime("%d-%m-%Y")
        #convertir la Timestamps en dateTime puis au format dd/mm/yy
        date_fin=groupe.index.max().to_pydatetime().date().strftime("%d-%m-%Y")
        date_debut_fin.append(date_debut+"/"+date_fin)
        distances.append(distance)
        #dataframe=pd.DataFrame(dataframe,columns=[nom_groupe],index=[nom_groupe])
        dataframe={"Date":date_debut_fin,"distance_parcourue_Metre":distances}
        dataframe=pd.DataFrame(dataframe)
    return dataframe
#fin de la fonction

#distance par mois en km
def distance_par_en_mois_km(dt):
    dt2=dt.groupby(pd.Grouper(level="Date_Enregistrement",freq="M",sort=True))
    distances=[]
    index=[]
    date_debut_fin=[]
    group_name=[]
    for nom_groupe,groupe in dt2:
        grouped=groupe.groupby(level="Date_Enregistrement")
        #Faire la somme des distances de chaque groupe
        distance=grouped.apply(distance_par_jour_km).sum()
        #convertir la Timestamps en dateTime puis au format dd/mm/yy
        date_debut=groupe.index.min().to_pydatetime().date().strftime("%d-%m-%Y")
        #convertir la Timestamps en dateTime puis au format dd/mm/yy
        date_fin=groupe.index.max().to_pydatetime().date().strftime("%d-%m-%Y")
        date_debut_fin.append(date_debut+"/"+date_fin)
        distances.append(distance)
        #dataframe=pd.DataFrame(dataframe,columns=[nom_groupe],index=[nom_groupe])
        dataframe={"Date":date_debut_fin,"distance_parcourue_Km":distances}
        dataframe=pd.DataFrame(dataframe)
    return dataframe
#fin de la fonction

#distance parcourue par Annee en Kilometre
def distance_par_en_annee_km(dt):
    dt2=dt.groupby(pd.Grouper(level="Date_Enregistrement",freq="Y",sort=True))
    distances=[]
    index=[]
    date_debut_fin=[]
    group_name=[]
    for nom_groupe,groupe in dt2:
        grouped=groupe.groupby(level="Date_Enregistrement")
        #Faire la somme des distances de chaque groupe
        distance=grouped.apply(distance_par_jour_km).sum()
        #convertir la Timestamps en dateTime puis au format dd/mm/yy
        date_debut=groupe.index.min().to_pydatetime().date().strftime("%d-%m-%Y")
        #convertir la Timestamps en dateTime puis au format dd/mm/yy
        date_fin=groupe.index.max().to_pydatetime().date().strftime("%d-%m-%Y")
        date_debut_fin.append(date_debut+"/"+date_fin)
        distances.append(distance)
        #dataframe=pd.DataFrame(dataframe,columns=[nom_groupe],index=[nom_groupe])
        dataframe={"Date":date_debut_fin,"distance_parcourue_Km":distances}
        dataframe=pd.DataFrame(dataframe)
    return dataframe
#fin de la fonction

def distance_par_en_annee_metre(dt):
    dt2=dt.groupby(pd.Grouper(level="Date_Enregistrement",freq="Y",sort=True))
    distances=[]
    index=[]
    date_debut_fin=[]
    group_name=[]
    for nom_groupe,groupe in dt2:
        grouped=groupe.groupby(level="Date_Enregistrement")
        #Faire la somme des distances de chaque groupe
        distance=grouped.apply(distance_par_jour_metre).sum()
        #convertir la Timestamps en dateTime puis au format dd/mm/yy
        date_debut=groupe.index.min().to_pydatetime().date().strftime("%d-%m-%Y")
        #convertir la Timestamps en dateTime puis au format dd/mm/yy
        date_fin=groupe.index.max().to_pydatetime().date().strftime("%d-%m-%Y")
        date_debut_fin.append(date_debut+"/"+date_fin)
        distances.append(distance)
        #dataframe=pd.DataFrame(dataframe,columns=[nom_groupe],index=[nom_groupe])
        dataframe={"Date":date_debut_fin,"distance_parcourue_Metre":distances}
        dataframe=pd.DataFrame(dataframe)
    return dataframe
#fin de la fonction

