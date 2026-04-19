import numpy as np
import pandas as pd
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import glob

#data initialisation
file_mode = "all" #single / all
domain = "phase" 

if file_mode == "all":
    #directory selection
    directory_val = 3 

    if directory_val == 1:
        directory = r"M:\OneDrive - The University of Manchester\ML_dataset\New datasets_Sample S4.4\0 to 1h\*" #0-1hr
    elif directory_val == 2:
        directory = r"M:\OneDrive - The University of Manchester\ML_dataset\New datasets_Sample S4.4\252 to 253 h\*" #252 to 253hr
    elif directory_val == 3:
        directory = r"M:\OneDrive - The University of Manchester\ML_dataset\New datasets_Sample S4.4\255 to 256 h\*" #255 to 256hr


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

    df = pd.read_csv(directory, usecols=["phase_deg", "q_pC"])
    df.dropna(inplace=True)
    #df = df[(df["q_pC"] <= 5) & (df["q_pC"] >= -5)] #optional filter 

    #scaling 
    numpy_scaled = scaler.fit_transform(df)

    #clustering
    clusters = gm.fit_predict(numpy_scaled)
    print(np.unique(clusters))

    #plot
    scatter = plt.scatter(
        df["phase_deg"],
        df["q_pC"],
        c=clusters,
        cmap="tab10",
        s=10,
        alpha=0.6,
    )

    for i in np.unique(clusters): #small bug - if clusters are not assigned in numerical order, range breaks
        colour = scatter.cmap(scatter.norm(i)) #replicates colour assignment from matplotlib  
        colours.append(colour)

    for i in np.unique(clusters):
        patch = mpatches.Patch(color=colours[i], label=f"Cluster {i}")
        handles.append(patch)

    plt.legend(handles=handles, title="Clusters", loc="upper right")

    plt.xlabel("Phase (deg)")
    plt.ylabel("Partial Discharge Magnitude (pC)")
    plt.title("Gaussian Mixed Model Clustering: PD Magnitude vs Phase")
    #plt.colorbar(scatter, label="Cluster")
    plt.tight_layout()
    plt.show()

if file_mode == "all":
    files = glob.glob(directory)
    files = files[:10]

    files.sort(
    key=lambda f: 
    int(f.rsplit('part', 1)[1]
        .replace('.csv', ''))
    ) 

    for file in files:
        df = pd.read_csv(file, usecols=["q_pC", "phase_deg"])
        #df = df[(df["q_pC"] <= 0) & (df["phase_deg"] <= 180)] #optional filter - abnormal region
        df.dropna(inplace=True)
        scaler.partial_fit(df) #partial mean, sd
    
    for file in files:
        df = pd.read_csv(file, usecols=["q_pC", "phase_deg"])
        df.dropna(inplace=True)
        numpy_scaled = scaler.transform(df)
        clusters = gm.fit_predict(numpy_scaled)

        #plot
        scatter = plt.scatter(
            df["phase_deg"],
            df["q_pC"],
            c=clusters,
            cmap="tab10",
            s=1,
            alpha=1,
            rasterized = True,
            marker = '.'
        )

    
    for i in range(NUM_CLUSTERS): #small bug - if clusters are not assigned in numerical order, range breaks
        colour = scatter.cmap(scatter.norm(i)) #replicates colour assignment from matplotlib  
        colours.append(colour)

    for i in range(NUM_CLUSTERS):
        patch = mpatches.Patch(color=colours[i], label=f"Cluster {i}")
        handles.append(patch)

    plt.legend(handles=handles, title="Clusters", loc="upper right")

    plt.xlabel("Phase (deg)")
    plt.ylabel("Partial Discharge Magnitude (pC)")
    plt.title("Gaussian Mixed Model Clustering: PD Magnitude vs Phase")
    #plt.colorbar(scatter, label="Cluster")
    plt.tight_layout()
    plt.show()
