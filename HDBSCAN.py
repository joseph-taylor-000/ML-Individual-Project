import matplotlib.pyplot as plt
import pandas as pd
import hdbscan
from sklearn.preprocessing import StandardScaler
import glob
import os
import time

start_time = time.time()

#parameters
MIN_CLUSTER_SIZE = 100   

#========dataset initialisation=======

#directory = input("Enter dataset directory: ")
directory = r"M:\OneDrive - The University of Manchester\ML_dataset\New datasets_Sample S4.4\255 to 256 h\*"
output_dir = r"M:\OneDrive - The University of Manchester\ML_Individual_Project"

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
sample = files[:1]
test_data = files[2:]

#HDBSCAN training using sample
scaler = StandardScaler()
data_list=[] 

print("Scaling sample data...\n")

for file in sample: 
    df = pd.read_csv(file, usecols=["q_pC", "phase_deg"])
    df = df[(df["q_pC"] <= 0) & (df["phase_deg"] <= 180)] #optional filter - abnormal region
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
    df = df[(df["q_pC"] <= 0) & (df["phase_deg"] <= 180)] #optional filter - abnormal region
    df.dropna(inplace=True)
    scaler.partial_fit(df)

print("Scaling Complete\n")

fig, ax = plt.subplots()

print("HDBSCAN...\n")

for file in test_data:
    df = pd.read_csv(file, usecols=["q_pC", "phase_deg",  "d_time_s"])
    df = df[(df["q_pC"] <= 0) & (df["phase_deg"] <= 180)] #optional filter - abnormal region
    df.dropna(inplace=True)
    X = scaler.transform(df[["q_pC", "phase_deg"]])
    cluster, strengths = hdbscan.prediction.approximate_predict(clusterer, X)

    df["cluster"], df["strengths"] = cluster, strengths

    scatter = ax.scatter(
        df["phase_deg"],
        df["q_pC"],
        c=cluster,
        cmap="tab10",
        s=1,
        alpha=1,
        rasterized=True,
        marker=','
    )

    print("Saving...")

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

fig.colorbar(scatter, ax=ax, label="Cluster") 

plt.tight_layout()
plt.show()
