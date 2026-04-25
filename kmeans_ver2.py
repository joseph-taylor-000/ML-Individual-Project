import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.colors as mcolors
from sklearn.cluster import KMeans
from sklearn.cluster import MiniBatchKMeans
from sklearn.preprocessing import StandardScaler
import glob
import time

#========dataset initialisation=======
directory_val = 1
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


files = glob.glob(directory)
print("\nNumber of files found:", len(files))

files.sort(
    key=lambda f: 
    int(f.rsplit('part', 1)[1]
        .replace('.csv', ''))
) 
#files list modified to be in numerical order
#split at 'part', using section after, remove file type
#file int for sort key

print("\nFiles found: ")
for i in range (len(files)):
    print(files[i] + "\n")
    
#file selection
#files = files[:2]

#=======elbow method========
elbow_start_time = time.time()

#elbow data - subsection of files, concat
elbow_files = files[:2]
data_list = []

for file in elbow_files:
    df = pd.read_csv(file, usecols=["q_pC", parameter]) 
    df.dropna(inplace=True)
    data_list.append(df)

data = pd.concat(data_list).values

#elbow scaling
scaler = StandardScaler()
data = scaler.fit_transform(data)

print(f'Number of samples: {(data.shape[0])}')
print(f'Number of features: {(data.shape[1])}')

#elbow set-up
loss = []
gradient = []
second_diff = []
K_range = range(1,10)

#elbow method
for k in K_range:
    kmeans = KMeans(n_clusters=k, n_init=10)
    kmeans.fit(data) #calculate global mean, std using file accumulation
    loss.append(kmeans.inertia_) 
    #interia = sum of squared distances from each point to its cluster center

#calculate max change in grad of loss thus best k, improved method
loss = np.array(loss) 

gradient = np.gradient(loss)
second_diff = np.gradient(gradient)

K_ideal = np.argmax(second_diff) + 2 #k_ideal corresponds to index of greatest second diff + 2
#K_ideal = 3; #hardset value

print(f"Elbow Method time: {time.time()-elbow_start_time}")
print(f'\n ideal K value: {K_ideal}')

#plot
fig, ax = plt.subplots()

plt.xlabel('K')
plt.ylabel('Loss (distortion score)')
plt.title('Elbow Method')
ax.set_xticks(K_range)
plt.plot(K_range, loss)
plt.show()

#========FULL KMEANS========
kmeans_start_time = time.time()

#kmeans parameters
BATCH_SIZE = 10_000

#initialisation
kmeans = MiniBatchKMeans(
    n_clusters=K_ideal,
    batch_size=BATCH_SIZE,
    random_state=42 #The answer to life, the universe and everything
)

#scaling
for file in files:
    df = pd.read_csv(file, usecols=["q_pC", parameter])
    df.dropna(inplace=True)
    df = df.sample(100000)
    scaler.partial_fit(df) #global mean, standard deviation

#kmeans fit
for file in files:
    print(file)
    df = pd.read_csv(file, usecols=["q_pC", parameter])
    df.dropna(inplace=True)
    df = df.sample(100000)

    X = scaler.transform(df) #transform data using scaler global values
    kmeans.partial_fit(X) #update predicted centroid positions

#cluster assignment and plot
plt.figure(figsize=(12, 5))

for file in files:
    print(file)
    df = pd.read_csv(file, usecols=["q_pC", parameter])
    df.dropna(inplace=True)

    X = scaler.transform(df[["q_pC", parameter]])
    df["cluster"] = kmeans.predict(X) #assign cluster based on proximity

    #add file to scatter
    scatter = plt.scatter(
    df[parameter],      
    df["q_pC"],       
    c=(df["cluster"]),
    norm = mcolors.Normalize(vmin=0,vmax=(K_ideal-1)),  #consistant normalisation 
    cmap=plt.get_cmap("tab10", K_ideal), #consistant colourmap, only required colours 
    s=1,
    alpha=1,   
    rasterized = True,
    marker = '.'                                    
)

print(f"K-means Clustering Time: {time.time()-kmeans_start_time}")
print(df.head())

#plot
handles = []

for i in range(K_ideal):
    colour = scatter.cmap(scatter.norm(i)) 
    patch = mpatches.Patch(color=colour, label=f"Cluster {i}")
    handles.append(patch)

plt.legend(handles=handles, title="Clusters", loc="upper right")


plt.xlabel(f"{x_axis} {unit}")
plt.ylabel("Partial Discharge Magnitude (pC)")
plt.title(f"K-means Clustering: PD Magnitude vs {x_axis}")
plt.tight_layout()
#plt.savefig("kmeans_1hr.png", dpi = 300)
plt.show()
