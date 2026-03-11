Version: Python 3.12.0

Required libraries:
matplotlib.pyplot: graphical plotting library for python.
pandas: data processing library for python.
glob: file directory library
os: also used for file management
sklearn: contains clustering (k-means) algorithm, scaling algorithms, example datasets.
	>>StandardScalar: scales data using mean and standard deviation to ensure similar feature ranges.
river: python ML library for streaming data into ML algorithms
	>> cluster: contains clustering algorithms. In this program, it is required for DenStream (explained below).

Notes on River library installation:
River library is supported up to Python version 3.12.0 and requires prerequisite installations of both Cython and Rust. 
This is because some of the machine learning algorithms available in river require high speed loops or strict memory management.
By implementing these features using Cython or Rust, python interpreter overhead is lost and this speed can be achieved.

#data initialisation 
* specifies input directory and output directory for cluster information
* creates/validates output directory
* loads files from input directory into list
* sorts file list numerically

#DenStream
'DenStream is a clustering algorithm for evolving data streams. DenStream can discover clusters with arbitrary shape and is robust against noise (outliers).'[1] 
Essentially, DenStream is a density based clustering algorithm that can be used with streaming data to perform a function analagous to DBSCAN clustering. 
It has been implemented to solve memory complications associated with the traditional DBSCAN.
Since it does not require a complete KNN tree of all the data to be loaded into memory, the algorithm can perform clustering on the whole data without requiring massive amounts of memory.

Parameters [1]:
decaying_factor: controls the impact of historical data on current cluster. 
>>0.01 has been chosen to investigate the clusters assuming that previous discharge events have a significant impact on current discharges.
beta / mu: controls the distance threshold from micro cluster centres at which points are considered noise (beta*mu > 1).
>>beta = 0.5, mu = 2.001  have been chosen to minimise noise tolerance to isolate abnormal regions as noise and extract them for further investigation using HDBSCAN.
epsilon: defines the neighbourhood radius for density clustering as in DBSCAN.
>>set at 2.3 to produce several clusters but preventing overfitting at lower epsilon values.
n_samples_init: defines the number of data points used to form the initial microclusters withing the data before streaming begins.
>>1000 is the default value and is usually sufficient (even for large datasets) as streaming means the clusters adapt with more data anyway.

#Streaming and Plotting
For each file in file directory:
* moves data into dataframe, keeps only phase_deg and q_pC columns to reduce bloat
* removes NaN rows
* to extract abnormal regions, filter is applied (df[(df["q_pC"] <= 0) & (df["phase_deg"] <= 180)])
* dataframe is scaled using numpy array, scaled data is then moved back into dataframe as df["q_pC_scaled"] and df["phase_deg_scaled"]
* unscaled data columns removed to reduce bloat
* dataframe processed iteratively per row using .intertuples(), which treats each row in the dataframe as a tuple.
* for each row, a dictionary is generated using df["phase_deg_scaled"] as the index and df["q_pC_scaled"] as the value (enumerated from tuple).
* this is so that the .learn_one() and predict_one() methods from the River cluster library can be used to implement the denstream algorithm.
	>> .learn_one(X) updates the model with a new set of features X [1]
	>> .predict_one(X) predicts the cluster value for a new set of features X [1]
* cluster IDs are then added to dataframe
* dataframe rows saved to text files based on their cluster value
* new file dataframe rows are appended to existing text files
* dataframe plotted with cluster-based colour grading for each point 

References:
[1] River DenStream. Available at (https://riverml.xyz/0.20.1/api/cluster/DenStream/) (Accessed 11 March 2026). 

  

