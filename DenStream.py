import matplotlib.pyplot as plt
import pandas as pd
import glob  
import os
from river import cluster
from sklearn.preprocessing import StandardScaler

#data initialisation
directory_val = 3 

#directory selection
if directory_val == 1:
    directory = r"M:\OneDrive - The University of Manchester\ML_dataset\New datasets_Sample S4.4\0 to 1h\*" #0-1hr
elif directory_val == 2:
    directory = r"M:\OneDrive - The University of Manchester\ML_dataset\New datasets_Sample S4.4\252 to 253 h\*" #252 to 253hr
elif directory_val == 3:
    directory = r"M:\OneDrive - The University of Manchester\ML_dataset\New datasets_Sample S4.4\255 to 256 h\*" #255 to 256hr

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
files = files[:2]

output_dir = r"M:\OneDrive - The University of Manchester\ML_Individual_Project"
os.makedirs(output_dir, exist_ok=True) 
#safety - prevents error if output_dir already exists, 
#creates directory if does not exist

#DenStream
denstream = cluster.DenStream(decaying_factor=0.01,
                              beta=0.5,
                              mu=2.0001,
                              epsilon=0.9,
                              n_samples_init=10000)


fig, ax = plt.subplots()
scaler = StandardScaler()

#---------------------------------------------------
#training scaler
for file in files:
    df = pd.read_csv(file, usecols=["phase_deg", "q_pC"])
    df.dropna(inplace=True)
    #df = df.sample(200000) #subset of data
    #df = df[(df["q_pC"] <= 0) & (df["phase_deg"] <= 180)] #optional filter - abnormal region
    scaler = scaler.partial_fit(df)

#training DenStream
for file in files:
    print(f"Streaming file: {file} for training")
    df = pd.read_csv(file, usecols=["phase_deg", "q_pC"])
    df.dropna(inplace=True)
    #df = df.sample(200000) #subset of data
    #df = df[(df["q_pC"] <= 0) & (df["phase_deg"] <= 180)] #optional filter - abnormal region
    
    #scaling
    df_scaled = scaler.transform(df) 

    print("Training...")
    for row in df_scaled:
        #row to dictionary conversion for DenStream input
        for phase, charge in enumerate(row): 
            point = {phase: float(charge)}

        denstream.learn_one(point) #train algorithm

#clustering data
for file in files:
    clusters= []

    print(f"Streaming file: {file}")
    df = pd.read_csv(file, usecols=["phase_deg", "q_pC"])
    df.dropna(inplace=True)
    #df = df.sample(200000) #subset of data
    #df = df[(df["q_pC"] <= 0) & (df["phase_deg"] <= 180)] #optional filter - abnormal region
    
    #scaling
    df_scaled = scaler.transform(df) 

    print("Clustering...")
    for row in df_scaled:
        #row to dictionary conversion for DenStream input
        for phase, charge in enumerate(row): 
            point = {phase: float(charge)}

        cluster = denstream.predict_one(point) #find appropriate cluster
        clusters.append(cluster)
        
    print(clusters)

    print("Saving...")
    df["cluster"] = clusters

    for cluster, group in df.groupby("cluster"):

        file_path = os.path.join(output_dir, f"cluster_{cluster}.txt")

        group.to_csv(
            file_path,
            mode="a",
            header=not os.path.exists(file_path),
            index=False
        )

    print("Plotting...")
    scatter = ax.scatter(
    df["phase_deg"],
    df["q_pC"],
    c=df["cluster"],
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

