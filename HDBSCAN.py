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
directory_val = 3 
domain = "phase"

if domain == "time":
    parameter = "time_s"
    x_axis = "Time"
    unit = "(seconds)"
elif domain == "phase":
    parameter = "phase_deg"
    x_axis = "Phase"
    unit = "(deg)"

#directory selection
if directory_val == 1:
    directory = r"M:\OneDrive - The University of Manchester\ML_dataset\New datasets_Sample S4.4\0 to 1h\*" #0-1hr
elif directory_val == 2:
    directory = r"M:\OneDrive - The University of Manchester\ML_dataset\New datasets_Sample S4.4\252 to 253 h\*" #252 to 253hr
elif directory_val == 3:
    directory = r"M:\OneDrive - The University of Manchester\ML_dataset\New datasets_Sample S4.4\255 to 256 h\*" #255 to 256hr


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
    df = pd.read_csv(file, usecols=["q_pC", parameter])
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
print("Calculating Scaler Parameters...\n")
for file in test_data:
    df = pd.read_csv(file, usecols=["q_pC", parameter])
    #df = df[(df["q_pC"] <= 0) & (df["phase_deg"] <= 180)] #optional filter - abnormal region
    df = df.sample(100000)
    df.dropna(inplace=True)
    scaler.partial_fit(df)

print("Calculation Complete\n")

fig, ax = plt.subplots()

print("HDBSCAN...\n")

for file in test_data:
    df = pd.read_csv(file, usecols=["q_pC", "time_s", "phase_deg", "d_time_s"])
    #df = df[(df["q_pC"] <= 0) & (df["phase_deg"] <= 180)] #optional filter - abnormal region
    df = df.sample(100000) #if sample size smaller than training samples, data may be added to clusters non-sequentially, which breaks colour index later
    df.dropna(inplace=True)
    X = scaler.transform(df[["q_pC", parameter]]) #scaling
    cluster,_ = hdbscan.prediction.approximate_predict(clusterer, X) #returns cluster and strengths - strengths not used

    df["cluster"] = cluster

    scatter = ax.scatter(
        df[parameter],
        df["q_pC"],
        c=cluster,
        cmap="tab20",
        s=1,
        alpha=1,
        rasterized=True,
        marker='.'
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

    for cluster, group in df.groupby("cluster"): #for each unique cluster, group is the corresponding subsection of dataframe
        file_path = os.path.join(output_dir, f"HDBSCAN_cluster_{cluster}.txt") #separate files for each cluster
        group.to_csv(
            file_path,
            mode="a", #append
            header=not os.path.exists(file_path), #only write header if first file
            index=False
        )

print("HDBSCAN Complete\n")
print(f"Program Completion Time: {time.time()-start_time} seconds")
print(df)


ax.set_xlabel(f"{x_axis} {unit}")
ax.set_ylabel("Partial Discharge Magnitude (pC)")
ax.set_title(f"HDBSCAN Clustering: PD Magnitude vs {x_axis}")

#fig.colorbar(scatter, ax=ax, label="Cluster") 

plt.tight_layout()
plt.show()
