from dtypes import unit, unitPopulation
import numpy as np 
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from plots.plot_unit_types import plot_unit_clusters


def est_unit_types(units : unitPopulation, plot = True):
    #collect the features from the units not labeled mua or lua 
    features = []
    unitInds = []
    #loop thru all units
    total = len(units.units_list)
    for i,u in enumerate(units.units_list):
        prog = i / total * 100
        print(f'progress = {prog}')
        u.get_unit_type_features()
        #if unit is not mua or lua --> add features to feature matrix
        if u.type != 'mua' and u.type != 'lua':
            features.append(u.type_features)
            unitInds.append(i)

    #convert fetures to np array
    features = np.asarray(features)
    #normalize the features 
    scaler = StandardScaler()
    scaler.fit_transform(features)
    #run K-means with 2(pyr & inter) / 3 clusters(pyr, wide inter, narrow inter)
    kmeans_fit = KMeans(n_clusters = 2, n_init = 50).fit(features)
    cluster_labels = kmeans_fit.predict(features)
    #interneurons have the higher inst firing rates 
    interneurons_lbl = np.argmax(kmeans_fit.cluster_centers_[:,0])
    for clustID, ind in zip(cluster_labels,unitInds):
        if clustID == interneurons_lbl:
            unitPopulation.units_list[ind].type = 'int'
        else:
            unitPopulation.units_list[ind].type = 'pyr'

    if plot == True: 
        plot_unit_clusters(units)

    
    




    


    

    


    




