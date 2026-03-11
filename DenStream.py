import matplotlib.pyplot as plt
import pandas as pd
import glob  
import os
from river import cluster
from sklearn.preprocessing import StandardScaler

#========dataset initialisation=======

#directory = input("Enter dataset directory: ")
directory = r"M:\OneDrive - The University of Manchester\ML_dataset\New datasets_Sample S4.4\255 to 256 h\*"
output_dir = r"M:\OneDrive - The University of Manchester\ML_Individual_Project"

os.makedirs(output_dir, exist_ok=True) 
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
#files = files[:2]

#DenStream
denstream = cluster.DenStream(decaying_factor=0.01,
                              beta=0.5,
                              mu=2.0001,
                              epsilon=2.3,
                              n_samples_init=1000)

# Stream and plot each file
fig, ax = plt.subplots()
scaler = StandardScaler()

for file in files:
    cluster_ids = []

    print(f"Streaming file: {file}")
    df = pd.read_csv(file, usecols=["phase_deg", "q_pC"])
    df.dropna(inplace=True)
    #df = df.sample(200000) #subset of data
    df = df[(df["q_pC"] <= 0) & (df["phase_deg"] <= 180)] #optional filter - abnormal region
    
    df_scaled = scaler.fit_transform(df)

    df["phase_deg_scaled"] = df_scaled[:,1]
    df["q_pC_scaled"] = df_scaled[:,0]

    df = df.drop(columns=["phase_deg", "q_pC"])

    # Stream each row (as a point) into DenStream
    print("Learning...")
    for row in df.itertuples(index=False):
        point = {i: float(v) for i, v in enumerate(row)} #generate dictionary
        denstream.learn_one(point)
        cluster_id = denstream.predict_one(point)
        cluster_ids.append(cluster_id)
        

    print("Saving...")
    df["cluster_id"] = cluster_ids

    for cluster_id, group in df.groupby("cluster_id"):

        file_path = os.path.join(output_dir, f"cluster_{cluster_id}.txt")

        group.to_csv(
            file_path,
            mode="a",
            header=not os.path.exists(file_path),
            index=False
        )

    print("Plotting...")
    scatter = ax.scatter(
    df["phase_deg_scaled"],
    df["q_pC_scaled"],
    c=df["cluster_id"],
    cmap="tab10",
    s=1,
    alpha=1,
    rasterized=True,
    marker='.'
    )
        

ax.set_xlabel("Phase (deg)")
ax.set_ylabel("Partial Discharge Magnitude (pC)")
ax.set_title("PRPD DenStream Density Clustering")

fig.colorbar(scatter, ax=ax, label="Cluster") 
#plt.savefig()
plt.tight_layout()
plt.show()

#plot no good, sample removes relevent data from df (abnormal region), groups have distinct phase cutoffs