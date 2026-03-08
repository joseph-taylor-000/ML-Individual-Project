import matplotlib.pyplot as plt
import pandas as pd
import hdbscan
from sklearn.preprocessing import StandardScaler

#parameters
MIN_CLUSTER_SIZE = 100   

#load data
directory = r"M:\OneDrive - The University of Manchester\ML_dataset\New datasets_Sample S4.4\0 to 1h\Unit1.1_Qmin0pC_QpC_PhDeg_VkV_0.000_3600.400s_part01.csv"
df = pd.read_csv(directory, usecols=["time_s", "q_pC"])
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
plt.figure(figsize=(12, 5))

scatter = plt.scatter(
    df["time_s"],
    df["q_pC"],
    c=labels,
    cmap="tab10",
    s=1,
    alpha=1,
    rasterized = True,
    marker = ','
)

plt.xlabel("Time (s)")
plt.ylabel("Partial Discharge Magnitude (pC)")
plt.title("HDBSCAN Clustering: PD Magnitude vs Time")
plt.colorbar(scatter, label="Cluster")
plt.tight_layout()
plt.show()
