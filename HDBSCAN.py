import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import hdbscan
from sklearn.preprocessing import StandardScaler
import glob
import os
import time
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches

start_time = time.time()

#parameters
MIN_CLUSTER_SIZE = 100   

#========dataset initialisation=======

#directory = input("Enter dataset directory: ")
directory = r"M:\OneDrive - The University of Manchester\ML_dataset\New datasets_Sample S4.4\255 to 256 h\*"
output_dir = r"M:\OneDrive - The University of Manchester\ML_Individual_Project\HDBSCAN_clusters"

os.makedirs(output_dir, exist_ok=True) 
#safety - prevents error if output_dir already exists, 
#creates directory if does not exist

files = glob.glob(directory)
print("\nNumber of files found:", len(files))
#df = df[(df["q_pC"] <= 5) & (df["q_pC"] >= -5)] #optional filter 

files.sort(
    key=lambda f: 
    int(f.rsplit('part', 1)[1]
        .replace('.csv', ''))
) 

print("\nFiles found: ")
for i in range (len(files)):
    print(files[i] + "\n")
    
#file selection
sample = files[:10]
test_data = files[10:15]

#HDBSCAN training using sample
scaler = StandardScaler()
data_list=[] 

print("Scaling sample data...\n")

for file in sample: 
    df = pd.read_csv(file, usecols=["q_pC", "phase_deg"])
    #df = df[(df["q_pC"] <= 0) & (df["phase_deg"] <= 180)] #optional filter - abnormal region
    df = df.sample(100000)
    df.dropna(inplace=True)
    scaler.partial_fit(df)
    data_list.append(df)
    


sample_data = scaler.transform(pd.concat(data_list).values)
print("Files scaled...\n")

clusterer = hdbscan.HDBSCAN(
    min_cluster_size=MIN_CLUSTER_SIZE,
    metric="euclidean",
    core_dist_n_jobs=6,
    approx_min_span_tree=True,
    prediction_data=True
)

print("Training...\n")
clusterer.fit(sample_data)
print("Training Complete\n")

#HDBSCAN clustering and plotting
print("Scaling test data...\n")
for file in test_data:
    df = pd.read_csv(file, usecols=["q_pC", "phase_deg"])
    #df = df[(df["q_pC"] <= 0) & (df["phase_deg"] <= 180)] #optional filter - abnormal region
    df = df.sample(100000)
    df.dropna(inplace=True)
    scaler.partial_fit(df)

print("Scaling Complete\n")

fig, ax = plt.subplots()

print("HDBSCAN...\n")

for file in test_data:
    df = pd.read_csv(file, usecols=["q_pC", "phase_deg",  "d_time_s"])
    #df = df[(df["q_pC"] <= 0) & (df["phase_deg"] <= 180)] #optional filter - abnormal region
    df = df.sample(100000) #if sample size smaller than training samples, data may be added to clusters non-sequentially, which breaks colour index later
    df.dropna(inplace=True)
    X = scaler.transform(df[["q_pC", "phase_deg"]])
    cluster, strengths = hdbscan.prediction.approximate_predict(clusterer, X)

    df["cluster"], df["strengths"] = cluster, strengths

    scatter = ax.scatter(
        df["phase_deg"],
        df["q_pC"],
        c=cluster,
        cmap="tab20",
        s=1,
        alpha=1,
        rasterized=True,
        marker=','
    )

    colours = []
    for i in np.unique(cluster):
        colour = scatter.cmap(scatter.norm(i)) #replicates colour assignment from matplotlib  
        colours.append(colour)

    handles = []
    for i in np.unique(cluster):
        patch = mpatches.Patch(color=colours[i], label=f"Cluster {i}")
        handles.append(patch)

    ax.legend(handles=handles, title="Clusters", loc="lower right")

    print(f"Saving clusters for part {file.rsplit('part', 1)[1].replace('.csv', '')}...")

    for cluster, group in df.groupby("cluster"):

        file_path = os.path.join(output_dir, f"HDBSCAN_cluster_{cluster}.txt")

        group.to_csv(
            file_path,
            mode="a",
            header=not os.path.exists(file_path),
            index=False
        )

print("HDBSCAN Complete\n")
print("Time: %s seconds" % (time.time() - start_time))
print(df)


ax.set_xlabel("Phase (deg)")
ax.set_ylabel("Partial Discharge Magnitude (pC)")
ax.set_title("HDBSCAN Clustering: PD Magnitude vs Phase")

#fig.colorbar(scatter, ax=ax, label="Cluster") 

plt.tight_layout()
plt.show()
