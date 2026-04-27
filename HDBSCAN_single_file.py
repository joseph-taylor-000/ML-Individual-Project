import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import hdbscan
from sklearn.preprocessing import StandardScaler
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches

#parameters
MIN_CLUSTER_SIZE = 100   

#load data
directory = r"M:\OneDrive - The University of Manchester\ML_Individual_Project\HDBSCAN_cluster_-1_with_time.txt"
df = pd.read_csv(directory, usecols=["phase_deg", "q_pC"])
df.dropna(inplace=True)
#df = df[(df["q_pC"] <= 5) & (df["q_pC"] >= -5)] #optional filter 

#scaling 
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df)

#HDBSCAN clustering
clusterer = hdbscan.HDBSCAN(
    min_cluster_size=MIN_CLUSTER_SIZE,
    metric="euclidean",
    core_dist_n_jobs=6
)

labels = clusterer.fit_predict(df_scaled)
print(labels)

#plot
fig, ax = plt.subplots()

scatter = ax.scatter(
    df["phase_deg"],
    df["q_pC"],
    c=labels,
    cmap="tab10",
    s=10,
    alpha=0.6,
    #rasterized = True,
    #marker = '.'
)


colours = []
for i in np.unique(labels):
    colour = scatter.cmap(scatter.norm(i)) #replicates colour assignment from matplotlib  
    colours.append(colour)

handles = []
for i in np.unique(labels):
    patch = mpatches.Patch(color=colours[i], label=f"Cluster {i}")
    handles.append(patch)

plt.legend(handles=handles, title="Clusters")

plt.xlabel("Phase (deg)")
plt.ylabel("Partial Discharge Magnitude (pC)")
plt.title("HDBSCAN Clustering: PD Magnitude vs Phase")
#plt.colorbar(scatter, label="Cluster")
plt.tight_layout()
plt.show()
