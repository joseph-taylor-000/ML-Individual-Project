import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

#dataset initialisation
directory = r"M:\OneDrive - The University of Manchester\ML_Individual_Project\clusters_255_anomaly\HDBSCAN_cluster_-1.txt"
dataset = pd.read_csv(directory)
data_pandas = dataset[["phase_deg", "q_pC"]] #select desired fields from dataframe
dataset.dropna(inplace=True)
data = data_pandas.to_numpy()

data = StandardScaler().fit_transform(data)

#data = data[(np.abs(data[:,1]) > 2)] #removes values less than 2pC

data[:,1] = data[:,1] / data[:,1].max() #gives percentage normalisation for charge

print('Number of samples: %d' % (data.shape[0]))
print('Number of features: %d' % (data.shape[1]))

#elbow method
loss = []
gradient = []
second_diff = []
K_range = range(1,5)

for k in K_range:
    kmeans = KMeans(n_clusters=k, n_init=10)
    kmeans.fit(data)
    loss.append(kmeans.inertia_)

#calculate max change in grad of loss thus best k
for i in range(1, len(loss)):
    gradient.append(loss[i] - loss[i-1])
for i in range(1, len(gradient)):
    second_diff.append(gradient[i] - gradient[i-1])

K_ideal = np.argmax(second_diff) + 2
#K_ideal = 10; #hardset value

print('\n ideal K value: %2d' % K_ideal)

fig = plt.figure()
ax = fig.add_subplot(111)
plt.xlabel('K')
plt.ylabel('Loss (distortion score)')
ax.set_xticks(K_range)
plt.plot(K_range, loss)
plt.show()

print(data_pandas)

kmeans = KMeans(n_clusters=K_ideal, n_init=10)
predictions = kmeans.fit_predict(data)
centroids = kmeans.cluster_centers_

plt.figure(figsize=(12, 5))

scatter = plt.scatter(
    data[:,0],      
    data[:,1],       
    c=predictions,   
    cmap="tab10",            
    s=10,
    alpha=0.6,   
    rasterized = True,
    marker = ',' 

)

cmap = plt.get_cmap("tab10")  
colours = []
for i in range(K_ideal):
    colour = scatter.cmap(scatter.norm(i))
    colours.append(colour)

handles = []
for i in range(K_ideal):
    patch = mpatches.Patch(color=colours[i], label=f"Cluster {i}")
    handles.append(patch)

plt.legend(handles=handles, title="Clusters", loc="lower right")
plt.xlabel('Phase (deg)')
plt.ylabel('Charge (pC)')
plt.title('K-means Clustering: Phase Resolved Partial Discharge')

#predict which cluster each data point will belong to (data[a] is one data point (all columns on row a))
for i in range(0, K_ideal):
    current_centroid_assignment = np.where(predictions == i)[0]
    ax.scatter(data[current_centroid_assignment, 0], 
               data[current_centroid_assignment, 1])
    plt.plot(centroids[i, 0], centroids[i, 1], 'k*', markersize=12)

plt.show()
