import numpy as np
import pandas as pd
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

#load data
directory = r"M:\OneDrive - The University of Manchester\ML_Individual_Project\clusters_255_anomaly\HDBSCAN_cluster_-1.txt"
df = pd.read_csv(directory, usecols=["phase_deg", "q_pC"])
df.dropna(inplace=True)
#df = df[(df["q_pC"] <= 5) & (df["q_pC"] >= -5)] #optional filter 

#scaling 
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df)

#gaussian mixture model
gm = GaussianMixture(n_components= 2, 
                     covariance_type = 'full',
                     random_state= 0,
                     init_params= 'kmeans',
                     verbose = 1
                     )

labels = gm.fit_predict(df_scaled)
print(np.unique(labels))

#plot
plt.figure(figsize=(12, 5))

scatter = plt.scatter(
    df_scaled[:,1],
    df_scaled[:,0],
    c=labels,
    cmap="tab10",
    s=10,
    alpha=0.6,
    #rasterized = True,
    #marker = '.'
)


colours = []
for i in np.unique(labels): #small bug - if clusters are not assigned in numerical order, range breaks
    colour = scatter.cmap(scatter.norm(i)) #replicates colour assignment from matplotlib  
    colours.append(colour)

handles = []
for i in np.unique(labels):
    patch = mpatches.Patch(color=colours[i], label=f"Cluster {i}")
    handles.append(patch)

plt.legend(handles=handles, title="Clusters", loc="upper right")

plt.xlabel("Phase (deg)")
plt.ylabel("Partial Discharge Magnitude (pC)")
plt.title("Gaussian Mixed Model Clustering: PD Magnitude vs Phase")
#plt.colorbar(scatter, label="Cluster")
plt.tight_layout()
plt.show()
