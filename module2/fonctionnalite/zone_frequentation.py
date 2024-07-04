from geopy.distance import geodesic
import pandas as pd
from sklearn.cluster import DBSCAN

#fonction to determine the min distance for epsilon of DBSCAN
def distance_dbscan(df):
    data=df.reset_index(drop=True)
    dataframe_list=[{"point1":[],"point2":[],"distance":[],"Date":[]}]
    for i in range(1,len(data)):
        coordonnee1=(data.loc[i-1,"Latitude"],data.loc[i-1,"Longitude"])
        coordonnee2=(data.loc[i,"Latitude"],data.loc[i,"Longitude"])
        distance=geodesic(coordonnee1,coordonnee2).km
        dataframe_list[0]["point1"].append(coordonnee1)
        dataframe_list[0]["point2"].append(coordonnee2)
        dataframe_list[0]["distance"].append(distance)
    dataframe=pd.DataFrame({"point1":dataframe_list[0]["point1"],"point2":dataframe_list[0]["point2"],"distance":dataframe_list[0]["distance"]})
    epsilon=round(dataframe["distance"].min(),5)
    return epsilon

#fonction to create cluster
def make_cluster(df,eps):
    dt=df[["Longitude","Latitude","Date_Enregistrement"]]
    dt.reset_index(drop=True,inplace=True)
    dt["Longitude"]=pd.to_numeric(dt["Longitude"],errors="coerce")
    dt["Latitude"]=pd.to_numeric(dt["Latitude"],errors="coerce")
    coordonnes=dt[["Latitude","Longitude"]].values
    dbscan=DBSCAN(eps=eps,min_samples=10)
    clusters=dbscan.fit(coordonnes)
    clusters_label=dbscan.labels_
    dt["cluster"]=clusters_label
    return dt
