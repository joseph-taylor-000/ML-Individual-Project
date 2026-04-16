Note: This github repository was created on 08/03/26. Development was initially being organised and logged locally.
The original creation of this program was on the 19/02/26.

Updated from previous commit. See previous commit for older version of README.

Required libraries:
matplotlib.pyplot: graphical plotting library for python.
matplotlib.colors: allows for information regarding colours to be assigned
matplotlib.patches: allows for geometry to be drawn on plots
pandas: data processing library for python.
numpy: math library for python.
hdbscan: library containing optimised Hierarchical Density-Based Spacial Clustering of Applications with Noise (HSBSCAN) algorithm. 
sklearn: contains clustering (k-means) algorithm, scaling algorithms, example datasets.
	>>StandardScalar: scales data using mean and standard deviation to ensure similar feature ranges.
time: allows for time keeping in python. Used to time execution of this program.

#data initialisation
* select domain
* select input directory and output directory
* check output directory exists

* loads data from input directory folder
* sorts data numerically
* splits data into training sample and test data

#Training
* for each file:
	>> creates dataframe
	>> chooses sample from data
    >> records sample indices for later separation
	>> removes NaN rows
	>> applies scaling to data
	>> adds to data list
* data list is then concatenated
* HDBSCAN performed on sample

#HDBSCAN
The HDBSCAN algorithm is a density-based clustering algorithm, based upon the preceding 'DBSCAN' algorithm. 

DBSCAN:
* Observes each data point and the data points which surround it within a user-defined radius (epsilon).  
* Core points are points which meet the minimum quantity of surrounding points within epsilon.
* All core points within epsilon of each other are clustered, each point being used to extend the cluster by epsilon.
* Non-core points within the radius of a core point are added to the cluster, but are not used to further extend it.
* Sparse regions treated as noise.

HDBSCAN:
The HDBSCAN advances upon the DBSCAN by removing the need to specify epsilon. 
Instead, the algorithm essentially tries many values of epsilon to accomodate for regions of high and low density.
As the density requirements change on each pass, the algorithm takes stock of how many clusters merge and finds the optimal clustering solution.

Important Parameters: 
* min_cluster_size >> defines the minimum number of points that are allowed in a cluster.
* min_samples >> defines minimum surrounding points to define a point as dense.
* metric >> defines distance calculation method. This is kept as euclidean.
* core_dist_n_jobs >> allows for user to set number of parallel executions of program. Used to decrease processing time.
* approx_min_span_tree >> HDBSCAN algorithm creates a minimum spanning tree. This method speeds up the algorithm by approximating.
* prediction_data >> this bool allows for the use of prediction data from previous trials. It is needed to train the model before use.

Important Methods:
scaler:
.fit(data) >> calculates mean and standard deviation for data 
.fit_transform(data) >> calculates mean and standard deviation for data and then scales data accordingly
.partial_fit(data) >> calculates mean and standard deviation for subsection of data, accumulates for whole data
.transform(data) >> uses precalculated scaler parameters to standardize data

HDBSCAN:
.approximate_predict(model, data) >> uses pretrained algorithm model on data to approximate clusters.
.fit_predict() >> Runs HDBSCAN on data and assigns group for each column.

Using approximate_predict, it is possible to integrate multiple files into the HDBSCAN algorithm and plot the results on the same axis.
This code version uses a for loop to perform approximate cluster predictions for each file within the test data; 
ensuring that test data samples are not shared with training data using saved indices.

#scatter plot 
Parameters:
x-axis >> df["time_s"],      
y-axis >> df["dq_pC"],       
colour >> c=cluster, #cluster = HDBSCAN assigned clusters   
colour map >> cmap="tab10",            
marker-size >> s=1, #smallest = 1
transparency >> alpha=1, #no transparency, most efficient 
rasterization >> rasterized = True, #prevents vector shapes, uses pixels as points for better efficiency 
marker-type >> marker = ',' #smallest marker type, better efficiency

Two for loops are used to assertain the colours used for each cluster and assign them to the graphs legend.

Cluster information is separated into multiple files:

for cluster, group in df.groupby("cluster"): #for each unique cluster, group is the corresponding subsection of dataframe
        file_path = os.path.join(output_dir, f"HDBSCAN_cluster_{cluster}.txt") #separate files for each cluster
        group.to_csv(
            file_path,
            mode="a", #append
            header=not os.path.exists(file_path), #only write header if first file
            index=False
        )

