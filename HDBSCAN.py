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

time_marker = time.time()

#parameters
MIN_CLUSTER_SIZE = 100   

#========dataset initialisation=======
directory_val = 5
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
#Sample 4.4 directories
if directory_val == 1:
    directory = r"M:\OneDrive - The University of Manchester\ML_dataset\New datasets_Sample S4.4\0 to 1h\*" #0-1hr
elif directory_val == 2:
    directory = r"M:\OneDrive - The University of Manchester\ML_dataset\New datasets_Sample S4.4\252 to 253 h\*" #252 to 253hr
elif directory_val == 3:
    directory = r"M:\OneDrive - The University of Manchester\ML_dataset\New datasets_Sample S4.4\255 to 256 h\*" #255 to 256hr

#Sample 4.3 directories
elif directory_val == 4:
    directory = r"M:\OneDrive - The University of Manchester\ML_dataset\New datasets_Sample S4.3\0 to 1h\*" #0 to 1hr
elif directory_val == 5:
    directory = r"M:\OneDrive - The University of Manchester\ML_dataset\New datasets_Sample S4.3\95 to 96h (sample opened for inspection at 96 h)\*" #95 to 96hr
elif directory_val == 6:
    directory = r"M:\OneDrive - The University of Manchester\ML_dataset\New datasets_Sample S4.3\190 to 191h\*" #190 to 191hr
    
#noise directories
elif directory_val == 7:
    directory = r"M:\OneDrive - The University of Manchester\ML_dataset\New datasets_Sample S4.4\Noise_0 to 120s\*" #0 to 120s
elif directory_val == 8:
    directory = r"M:\OneDrive - The University of Manchester\ML_dataset\New datasets_Sample S4.4\Noise_0 to 1000s\*" #0 to 1000s

#output directories
output_dir = r"M:\OneDrive - The University of Manchester\ML_Individual_Project\HDBSCAN_clusters"

if directory_val < 4:
    output_dir_img = r"M:\OneDrive - The University of Manchester\ML_Individual_Project\Results Plots\PRPD HDBSCAN\S4.4"
    file_name = os.path.join(output_dir_img, f"S4.4_{directory.rsplit("4.4\\",1)[1].replace('\*', '')}.png")
else:
    output_dir_img = r"M:\OneDrive - The University of Manchester\ML_Individual_Project\Results Plots\PRPD HDBSCAN\S4.3"
    file_name = os.path.join(output_dir_img, f"S4.3_{directory.rsplit("4.3\\",1)[1].replace('\*', '')}.png")

os.makedirs(output_dir, exist_ok=True) 
os.makedirs(output_dir_img, exist_ok=True) 
#safety - prevents error if output_dir already exists, 
#creates directory if does not exist

files = glob.glob(directory)
print("\nNumber of files found:", len(files))


files.sort(
    key=lambda f: 
    int(f.rsplit('part', 1)[1]
        .replace('.csv', ''))
) 

print("\nFiles found: ")
for i in range (len(files)):
    print(files[i] + "\n")
    
#file selection
sample = files #Note - test data file range and sample range must be equal
test_data = sample

#HDBSCAN training using sample
scaler = StandardScaler()
data_list=[] 
indices =[]

print("Scaling sample data...\n")

for file in sample: 
    df = pd.read_csv(file, usecols=["q_pC", parameter])
    #df = df[(df["q_pC"] <= 0) & (df["phase_deg"] <= 180)] #optional filter - abnormal region
    df = df[(df["q_pC"] >= 0.5) | (df["q_pC"] <= -0.5)] #noise filter
    df = df.sample(10000)
    indices.append(df.index) #keep sample indices
    df.dropna(inplace=True)

    scaler.partial_fit(df) #partial mean, sd
    data_list.append(df)

data_list = pd.concat(data_list) #concat to single dataframe
data_list = data_list.values #convert to numpy array for transform
sample_data = scaler.transform(data_list) #transform using scaler

print("Files scaled...\n")
print(f"Scaling Completion Time: {time.time()-time_marker} seconds\n")
time_marker = time.time()

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

print(f"Training Completion Time: {time.time()-time_marker} seconds\n")
time_marker = time.time()

#HDBSCAN clustering and plotting
print("Calculating Scaler Parameters...\n")


for file in test_data:
    df = pd.read_csv(file, usecols=["q_pC", parameter])
    #df = df[(df["q_pC"] <= 0) & (df["phase_deg"] <= 180)] #optional filter - abnormal region
    df = df[(df["q_pC"] >= 0.5) | (df["q_pC"] <= -0.5)] #noise filter

    i = test_data.index(file)
    df = df.drop(index=indices[int(i)]) #remove test data samples before sampling

    df = df.sample(100000)
    df.dropna(inplace=True)
    scaler.partial_fit(df)
    

print("Calculation Complete\n")

fig, ax = plt.subplots()

print("HDBSCAN...\n")

clusters = []
for file in test_data:
    df = pd.read_csv(file, usecols=["q_pC", "time_s", "phase_deg", "d_time_s"])
    #df = df[(df["q_pC"] <= 0) & (df["phase_deg"] <= 180)] #optional filter - abnormal region
    df = df[(df["q_pC"] >= 0.5) | (df["q_pC"] <= -0.5)] #noise filter

    i = test_data.index(file)
    df = df.drop(index=indices[i]) #remove test data samples before sampling
    

    df = df.sample(100000) #if sample size smaller than training samples, data may be added to clusters non-sequentially, which breaks colour index later
    df.dropna(inplace=True)
    X = scaler.transform(df[["q_pC", parameter]]) #scaling
    cluster,_ = hdbscan.prediction.approximate_predict(clusterer, X) #returns cluster and strengths - strengths not used

    df["cluster"] = cluster
    clusters.append(cluster)

    scatter = ax.scatter(
        df[parameter],
        df["q_pC"],
        c=cluster,
        cmap="tab20",
        norm = mcolors.Normalize(vmin=0, vmax=(19)),  #consistant normalisation for tab20
        s=1,
        alpha=1,
        rasterized=True,
        marker='.'
    )

    print(f"Saving clusters for part {file.rsplit('part', 1)[1].replace('.csv', '')}...")

    for cluster, group in df.groupby("cluster"): #for each unique cluster, group is the corresponding subsection of dataframe
        file_path = os.path.join(output_dir, f"Directory_{directory_val}_HDBSCAN_cluster_{cluster}.txt") #separate files for each cluster
        group.to_csv(
            file_path,
            mode="a", #append
            header=not os.path.exists(file_path), #only write header if first file
            index=False
        )

print("HDBSCAN Complete\n")
print(f"HDBSCAN Completion Time: {time.time()-time_marker} seconds")
print(df)

clusters = np.concatenate(clusters)
handles = []
for i in np.unique(clusters):
    colour = scatter.cmap(scatter.norm(i))
    patch = mpatches.Patch(color=colour, label=f"Cluster {i}")
    handles.append(patch)

ax.legend(handles=handles, title="Clusters")

ax.set_xlabel(f"{x_axis} {unit}")
ax.set_ylabel("Partial Discharge Magnitude (pC)")
ax.set_title(f"HDBSCAN Clustering: PD Magnitude vs {x_axis}")
plt.savefig(fname = file_name)
#fig.colorbar(scatter, ax=ax, label="Cluster") 

plt.tight_layout()
plt.show()
