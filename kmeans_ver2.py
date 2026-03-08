import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches
from sklearn.cluster import KMeans
from sklearn.cluster import MiniBatchKMeans
from sklearn.preprocessing import StandardScaler
import glob

#========dataset initialisation=======

#directory = input("Enter dataset directory: ")
directory = r"M:\OneDrive - The University of Manchester\ML_dataset\New datasets_Sample S4.4\0 to 1h\*"
files = glob.glob(directory)
print("\nNumber of files found:", len(files))

files.sort(
    key=lambda f: 
    int(f.rsplit('part', 1)[1]
        .replace('.csv', ''))
) 
#files list modified to be in numerical order
#split at 'part', using section after, remove file type

print("\nFiles found: ")
for i in range (len(files)):
    print(files[i] + "\n")
    
#file selection
files = files[:242]

#=======elbow method========

#elbow data - subsection of files, concat
elbow_files = files[:1]
data_list = []

for file in elbow_files:
    df = pd.read_csv(file, usecols=["dq_pC"]) 
    df.dropna(inplace=True)
    data_list.append(df)

data = pd.concat(data_list).values

#elbow scaling
scaler = StandardScaler()
data = scaler.fit_transform(data)

print('Number of samples: %d' % (data.shape[0]))
print('Number of features: %d' % (data.shape[1]))

#elbow set-up
loss = []
gradient = []
second_diff = []
K_range = range(1,3)

#elbow method
for k in K_range:
    kmeans = KMeans(n_clusters=k, n_init=10)
    kmeans.fit(data)
    loss.append(kmeans.inertia_) 
    #interia = sum of squared distances from each point to its cluster center

#calculate max change in grad of loss thus best k, improved method
loss = np.array(loss) 

gradient = np.gradient(loss)
second_diff = np.gradient(gradient)

K_ideal = np.argmax(second_diff) + 1
K_ideal = 3; #hardset value

print('\n ideal K value: %2d' % K_ideal)

#plot
fig = plt.figure()
ax = fig.add_subplot(111)
plt.xlabel('K')
plt.ylabel('Loss (distortion score)')
ax.set_xticks(K_range)
plt.plot(K_range, loss)
plt.show()

#========FULL KMEANS========

#kmeans parameters
BATCH_SIZE = 10_000

#initialisation
kmeans = MiniBatchKMeans(
    n_clusters=K_ideal,
    batch_size=BATCH_SIZE,
    random_state=42
)

#scaling
for file in files:
    df = pd.read_csv(file, usecols=["dq_pC"])
    df.dropna(inplace=True)
    scaler.partial_fit(df)

#kmeans fit
for file in files:
    df = pd.read_csv(file, usecols=["dq_pC"])
    df.dropna(inplace=True)
    X = scaler.transform(df)
    kmeans.partial_fit(X)

#cluster assignment and plot
plt.figure(figsize=(12, 5))

for file in files:
    df = pd.read_csv(file, usecols=["time_s", "dq_pC"])
    df.dropna(inplace=True)

    X = scaler.transform(df[["dq_pC"]])
    df["cluster"] = kmeans.predict(X)

    #add file to scatter
    scatter = plt.scatter(
    df["time_s"],      
    df["dq_pC"],       
    c=df["cluster"],   
    cmap="tab10",            
    s=1,
    alpha=1,   
    rasterized = True,
    marker = ','                                    
)


print(df.head())

#plot
cmap = plt.get_cmap("tab10")  
colors = []
for i in range(K_ideal):
    colors.append(cmap(i))

handles = []
for i in range(K_ideal):
    patch = mpatches.Patch(color=colors[i], label=f"Cluster {i}")
    handles.append(patch)

plt.legend(handles=handles, title="Clusters", loc="upper right")
plt.xlabel("Time (s)")
plt.ylabel("Partial Discharge Magnitude (pC)")
plt.title("PD Events Clustering: Magnitude vs Time")
plt.tight_layout()
plt.savefig("kmeans_1hr.png", dpi = 300)
plt.show()
