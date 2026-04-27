import numpy as np
import pandas as pd
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.colors as mcolors 
import glob
import os
import time

#data initialisation
file_mode = "all" #single / all
domain = "phase"

#domain selection
if domain == "time":
    parameter = "time_s"
    x_axis = "Time"
    unit = "(seconds)"
elif domain == "phase":
    parameter = "phase_deg"
    x_axis = "Phase"
    unit = "(deg)"

if file_mode == "all":
    #directory selection
    directory_val = 1 

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
output_dir = r"M:\OneDrive - The University of Manchester\ML_Individual_Project\GMM_clusters"

if directory_val < 4:
    output_dir_img = r"M:\OneDrive - The University of Manchester\ML_Individual_Project\Results Plots\PRPD GMM\Sample 4.4"
    file_name = os.path.join(output_dir_img, f"S4.4_{directory.rsplit("4.4\\",1)[1].replace('\*', '')}.png")
else:
    output_dir_img = r"M:\OneDrive - The University of Manchester\ML_Individual_Project\Results Plots\PRPD GMM\Sample 4.3"
    file_name = os.path.join(output_dir_img, f"S4.3_{directory.rsplit("4.3\\",1)[1].replace('\*', '')}.png")

os.makedirs(output_dir, exist_ok=True)
os.makedirs(output_dir_img, exist_ok=True)

#GMM clusterer
NUM_CLUSTERS = 4
gm = GaussianMixture(n_components= NUM_CLUSTERS, 
                    covariance_type = 'full',
                    random_state= 0,
                    init_params= 'kmeans',
                    verbose = 1
                    )

#scaling
scaler = StandardScaler()

#plot init
plt.figure(figsize=(12, 5)) 
handles = []
colours = []

if file_mode == "single":
    directory = r"M:\OneDrive - The University of Manchester\ML_Individual_Project\clusters_255_anomaly\HDBSCAN_cluster_-1.txt"

    df = pd.read_csv(directory, usecols=[parameter, "q_pC"])
    df.dropna(inplace=True)
    #df = df[(df["q_pC"] <= 5) & (df["q_pC"] >= -5)] #optional filter 

    #scaling 
    numpy_scaled = scaler.fit_transform(df)

    #clustering
    clusters = gm.fit_predict(numpy_scaled)
    print(np.unique(clusters))

    #plot
    scatter = plt.scatter(
        df[parameter],
        df["q_pC"],
        c=clusters,
        cmap="tab10",
        norm = mcolors.Normalize(vmin=0, vmax=9),
        s=10,
        alpha=0.6,
    )

    for i in np.unique(clusters):
        colour = scatter.cmap(scatter.norm(i))
        patch = mpatches.Patch(color=colour, label=f"Cluster {i}")
        handles.append(patch)


if file_mode == "all":
    files = glob.glob(directory)
    files = files[:2]

    files.sort(
    key=lambda f: 
    int(f.rsplit('part', 1)[1]
        .replace('.csv', ''))
    ) 

    #pass 1 - fit scaler
    for file in files:
        df = pd.read_csv(file, usecols=["q_pC", parameter])
        #df = df[(df["q_pC"] <= 0) & (df["phase_deg"] <= 180)] #optional filter - abnormal region
        df.dropna(inplace=True)
        scaler.partial_fit(df) #partial mean, sd
    
    print("Training...")
    time_marker = time.time()
    #pass 2 - train GMM model
    for file in files:
        df = pd.read_csv(file, usecols=["q_pC", parameter])
        df.dropna(inplace=True)
        numpy_scaled = scaler.transform(df)
        gm = gm.fit(numpy_scaled)
    print("Training Complete")
    training_time = time.time()-time_marker

    print("Clustering...")
    time_marker = time.time()
    #pass 3 - determine cluster labels
    for file in files:
        df = pd.read_csv(file, usecols=["q_pC", parameter])
        df.dropna(inplace=True)
        numpy_scaled = scaler.transform(df)
        clusters = gm.predict(numpy_scaled)
        df["cluster"] = clusters

        #plot
        scatter = plt.scatter(
            df[parameter],
            df["q_pC"],
            c=clusters,
            cmap="tab10",
            norm = mcolors.Normalize(vmin=0, vmax=(9)),
            s=1,
            alpha=1,
            rasterized = True,
            marker = '.'
        )
    print("Clustering Complete")
    test_time = time.time()-time_marker

    print(f"Saving clusters for part {file.rsplit('part', 1)[1].replace('.csv', '')}...")

    for cluster, group in df.groupby("cluster"): #for each unique cluster, group is the corresponding subsection of dataframe
        file_path = os.path.join(output_dir, f"Directory_{directory_val}_HDBSCAN_cluster_{cluster}.txt") #separate files for each cluster
        group.to_csv(
            file_path,
            mode="a", #append
            header=not os.path.exists(file_path), #only write header if first file
            index=False
        )

    for i in range(NUM_CLUSTERS):
        colour = scatter.cmap(scatter.norm(i))
        patch = mpatches.Patch(color=colour, label=f"Cluster {i}")
        handles.append(patch)

plt.legend(handles=handles, title="Clusters", loc="upper right")

plt.xlabel(f"{x_axis} {unit}")
plt.ylabel("Partial Discharge Magnitude (pC)")
plt.title(f"Gaussian Mixed Model Clustering: PD Magnitude vs {x_axis}")
#plt.colorbar(scatter, label="Cluster")
plt.savefig(fname = file_name)
plt.tight_layout()
plt.show()

print(f"Traing Time: {training_time} \nTest Time: {test_time}")
