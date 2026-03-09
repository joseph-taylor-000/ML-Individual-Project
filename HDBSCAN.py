import matplotlib.pyplot as plt
import pandas as pd
import hdbscan
from sklearn.preprocessing import StandardScaler
import glob
import time

start_time = time.time()

#parameters
MIN_CLUSTER_SIZE = 100   

#========dataset initialisation=======

#directory = input("Enter dataset directory: ")
directory = r"M:\OneDrive - The University of Manchester\ML_dataset\New datasets_Sample S4.4\0 to 1h\*"
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
test_data = files[2:3]

#HDBSCAN training using sample
scaler = StandardScaler()
data_list=[]

print("Scaling sample data...\n")

for file in sample: 
    df = pd.read_csv(file, usecols=["dq_pC", "time_s"])
    df.dropna(inplace=True)
    scaler.partial_fit(df)
    data_list.append(df)
    


sample_data = scaler.transform(pd.concat(data_list).values)
print("Files scaled...\n")

clusterer = hdbscan.HDBSCAN(
    min_cluster_size=MIN_CLUSTER_SIZE,
    metric="euclidean",
    core_dist_n_jobs=4,
    approx_min_span_tree=True,
    prediction_data=True
)

print("Training...\n")
clusterer.fit(sample_data)
print("Training Complete\n")

#HDBSCAN clustering and plotting
print("Scaling test data...\n")
for file in test_data:
    df = pd.read_csv(file, usecols=["dq_pC", "time_s"])
    df.dropna(inplace=True)
    scaler.partial_fit(df)

print("Scaling Complete\n")

fig, ax = plt.subplots()

print("HDBSCAN...\n")

for file in test_data:
    df = pd.read_csv(file, usecols=["dq_pC", "time_s"])
    df.dropna(inplace=True)
    X = scaler.transform(df)
    cluster, strengths = hdbscan.prediction.approximate_predict(clusterer, X)

    df["cluster"], df["strengths"] = cluster, strengths

    scatter = ax.scatter(
        df["time_s"],
        df["dq_pC"],
        c=cluster,
        cmap="tab10",
        s=1,
        alpha=1,
        rasterized=True,
        marker=','
    )

print("HDBSCAN Complete\n")
print("Time: %s seconds" % (time.time() - start_time))
print(df)

ax.set_xlabel("Time (s)")
ax.set_ylabel("Partial Discharge Magnitude (pC)")
ax.set_title("HDBSCAN Clustering: PD Magnitude vs Time")

fig.colorbar(scatter, ax=ax, label="Cluster") 

plt.tight_layout()
plt.show()
