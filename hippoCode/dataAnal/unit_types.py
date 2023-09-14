from dtypes import unit , unitPopulation
import numpy as np 
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from plots.plot_unit_types import plot_unit_clusters


def est_unit_types(units : unitPopulation, plot = True):
    from sklearn.decomposition import PCA
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
    feature_labels = ['fr','isi','peak_trough_t','tau_decay','tau_rise']
    #normalize the features 
    scaler = StandardScaler()
    norm_features = scaler.fit_transform(features)
    #perform PCA to 
    '''
    pca_unit_features = PCA(n_components=3)
    pca_fitted = pca_unit_features.fit_transform(norm_features)
    '''
    #run K-means with 2(pyr & inter) / 3 clusters(pyr, wide inter, narrow inter)
    kmeans_fit = KMeans(n_clusters = 2, n_init = 50).fit(norm_features)
    cluster_labels = kmeans_fit.predict(norm_features)
    #interneurons have the higher inst firing rates 
    interneurons_lbl = np.argmax(kmeans_fit.cluster_centers_[:,0])
    pyr_lbl = np.argmin(kmeans_fit.cluster_centers_[:,-1])
    for clustID, ind in zip(cluster_labels,unitInds):
        if clustID == interneurons_lbl:
            units.units_list[ind].type = 'int'
        elif clustID == pyr_lbl:
            units.units_list[ind].type = 'pyr'
        else:
            units.units_list[ind].type = 'int_wide'

        


    '''
    if plot == True: 
        plot_unit_clusters(units)
    '''


    
    




    


    

    


    




