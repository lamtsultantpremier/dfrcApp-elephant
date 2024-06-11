import pandas as pd
from geopy.distance import geodesic
import math
from fonctionnalite.distance import distance_par_jour_metre,distance_par_jour_m,distance_par_jour_km
#defini si l'éléphant est en Marche ou à l'arrêt en Km et prend en paramètre le DataFrame Originel et aussi sa vitesse
def Activite_elephant_km(df):
    import datetime
    dataframe=[]
    data=df.copy().reset_index(drop=True)
    data.sort_values(by="Date_Enregistrement",ascending=False,inplace=True)
    for i in range(1,len(data)):
        if(i<100):
            coordonee1=(data.loc[i-1,"Latitude"],data.loc[i-1,"Longitude"])
            coordonee2=(data.loc[i,"Latitude"],data.loc[i,"Longitude"])
            #calculer la distance entre les deux points
            distance=geodesic(coordonee1,coordonee2).km
            #Selectionner l'heure d'arrivé
            time1=data["Heure_Enregistrement"].loc[i]
            #Selectionner l'heure de départ
            time2=data["Heure_Enregistrement"].loc[i-1]
            #Recuperer la date d'aujourdhui
            to_day=datetime.date.today()
            datetime1 = datetime.datetime.combine(to_day, time1)
            datetime2 = datetime.datetime.combine(to_day, time2)
            datetime1_delta=datetime.timedelta(hours=datetime1.hour,minutes=datetime1.minute,seconds=datetime1.second)
            datetime2_delta=datetime.timedelta(hours=datetime2.hour,minutes=datetime2.minute,seconds=datetime2.second)
            date1_delta_seconds=datetime1_delta.total_seconds()
            date2_delta_seconds=datetime2_delta.total_seconds()
            difference_timedelta_seconds=(date2_delta_seconds-date1_delta_seconds)%(24*3600)
            difference_timedelta=datetime.timedelta(seconds=difference_timedelta_seconds)
            #convertir la duree en seconds pour déterminer la vitesse
            difference_timedelta_total_seconds=difference_timedelta.total_seconds()
            difference_timedelta_hour=difference_timedelta_total_seconds/3600
            dataframe.append({"point1": coordonee1,"point2":coordonee2,
                          "distance":distance,
                          "date_dep":data["Date_Enregistrement"].loc[i-1],
                          "date_arr":data["Date_Enregistrement"].loc[i],
                          "heure_d":data["Heure_Enregistrement"].loc[i],
                          "heure_arr":data["Heure_Enregistrement"].loc[i-1],
                          "duree_activite": difference_timedelta,
                          "vitesse":f"{round(distance/difference_timedelta_hour,6)} Km/h"
                            })
    dataframe=pd.DataFrame(dataframe)
    #Definition d'un seuil qui permettra de dire si l'éléphant est en marche ou arrêter entre deux position
    dataframe["status_deplacement"]=dataframe["distance"].apply(lambda x:"Au repos" if x<1 else "En Marche")
    return  dataframe
#fin de la fonction

#defini si l'éléphant est en Marche ou à l'arrêt en Km et prend en paramètre le DataFrame Originel
def Activite_elephant_m(df):
    import datetime
    dataframe=[]
    data=df.copy().reset_index(drop=True)
    data.sort_values(by="Date_Enregistrement",ascending=False,inplace=True)
    for i in range(1,len(data)):
        if(i<100):
            coordonee1=(data.loc[i-1,"Latitude"],data.loc[i-1,"Longitude"])
            coordonee2=(data.loc[i,"Latitude"],data.loc[i,"Longitude"])
            #calculer la distance entre les deux points
            distance=geodesic(coordonee1,coordonee2).m
            #Selectionner l'heure d'arrivé
            time1=data["Heure_Enregistrement"].loc[i]
            #Selectionner l'heure de départ
            time2=data["Heure_Enregistrement"].loc[i-1]
            #Recuperer la date d'aujourdhui
            to_day=datetime.date.today()
            datetime1 = datetime.datetime.combine(to_day, time1)
            datetime2 = datetime.datetime.combine(to_day, time2)
            datetime1_delta=datetime.timedelta(hours=datetime1.hour,minutes=datetime1.minute,seconds=datetime1.second)
            datetime2_delta=datetime.timedelta(hours=datetime2.hour,minutes=datetime2.minute,seconds=datetime2.second)
            date1_delta_seconds=datetime1_delta.total_seconds()
            date2_delta_seconds=datetime2_delta.total_seconds()
            difference_timedelta_seconds=(date2_delta_seconds-date1_delta_seconds)%(24*3600)
            difference_timedelta=datetime.timedelta(seconds=difference_timedelta_seconds)
            #convertir la duree en seconds pour déterminer la vitesse
            difference_timedelta_total_seconds=difference_timedelta.total_seconds()
            dataframe.append({"point1": coordonee1,"point2":coordonee2,
                          "distance":distance,
                          "date_dep":data["Date_Enregistrement"].loc[i-1],
                          "date_arr":data["Date_Enregistrement"].loc[i],
                          "heure_d":data["Heure_Enregistrement"].loc[i],
                          "heure_arr":data["Heure_Enregistrement"].loc[i-1],
                          "duree_activite": difference_timedelta,
                          "vitesse":f"{round(distance/difference_timedelta_total_seconds,6)} Km/h"
                            })
    dataframe=pd.DataFrame(dataframe)
    #Definition d'un seuil qui permettra de dire si l'éléphant est en marche ou arrêter entre deux position
    dataframe["status_deplacement"]=dataframe["distance"].apply(lambda x:"Au repos" if x<1 else "En Marche")
    return  dataframe
#fin de la fonction

#definir la duree de marche et de repos
def duree_marche_repos_km(dataframe):
    import datetime
    duree_activite=Activite_elephant_km(dataframe)
    duree=duree_activite.groupby(by=["date_dep","status_deplacement"]).agg({"distance":"sum","duree_activite":"sum"})
    duree.rename(columns={"duree_activite":"duree"},inplace=True)
    duree.sort_values(by="date_dep",ascending=False)
    return duree
#fin de la fonction
 
 #vitesse par Jour effectuerpar un éléphant
def vitesse_jour_km(df):
    import datetime
    vitesse=0.0
    distance=[]
    distances={"index":[],"heure_depart":[],"heure_arrive":[],"distance_km":[],"duree_heure":[],"duree_sec":[],"vitesse":[]}
    df_change=df.set_index("Date_Enregistrement",drop=True)
    df_change.index=pd.to_datetime(df_change.index)
    df_grouped=df_change.groupby(pd.Grouper(level="Date_Enregistrement",freq="D"))
    for key,group in df_grouped:
        if not group.empty:
            heure_arrive=group.head(1)["Heure_Enregistrement"].reset_index(drop=True)[0]
            heure_depart=group.tail(1)["Heure_Enregistrement"].reset_index(drop=True)[0]
            dist=distance_par_jour_km(group)
            index=key.date()
            time1=heure_depart
            #Selectionner l'heure de départ
            time2=heure_arrive
            #Recuperer la date d'aujourdhui
            to_day=datetime.date.today()
            datetime1 = datetime.datetime.combine(to_day, time1)
            datetime2 = datetime.datetime.combine(to_day, time2)
            datetime1_delta=datetime.timedelta(hours=datetime1.hour,minutes=datetime1.minute,seconds=datetime1.second)
            datetime2_delta=datetime.timedelta(hours=datetime2.hour,minutes=datetime2.minute,seconds=datetime2.second)
            date1_delta_seconds=datetime1_delta.total_seconds()
            date2_delta_seconds=datetime2_delta.total_seconds()
            difference_timedelta_seconds=(date2_delta_seconds-date1_delta_seconds)%(24*3600)
            difference_timedelta=datetime.timedelta(seconds=difference_timedelta_seconds)
            #convertir la duree en seconds pour déterminer la vitesse
            difference_timedelta_total_seconds=difference_timedelta.total_seconds()
            #mettre la duree en chaine de caractere
            heure=int(difference_timedelta_total_seconds//3600)
            minutes=int((difference_timedelta_total_seconds % 3600)//60)
            secondes=int((difference_timedelta_total_seconds%60))
            duree_heure=f"{heure:02d}:{minutes:02d}:{secondes:02d}"
            #fin
            
            temps_heure=difference_timedelta_total_seconds/3600
            #vitesse=dist/difference_timedelta_total_seconds
            if difference_timedelta_total_seconds!=0.0:
                vitesse=dist/temps_heure
            distances["index"].append(index)
            distances["heure_depart"].append(heure_depart)
            distances["heure_arrive"].append(heure_arrive)
            distances["distance_km"].append(dist)
            distances["vitesse"].append(vitesse)
            distances["duree_heure"].append(duree_heure)
            distances["duree_sec"].append(difference_timedelta_total_seconds)
            #distances["vitesse"].append(vitesse)
            df=pd.DataFrame(data=distances,index=distances["index"])
    return  df