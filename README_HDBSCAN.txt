Note: This github repository was created on 08/03/26. Development was initially being organised and logged locally.
The original creation of this program was on the 19/02/26.

Required libraries:
matplotlib.pyplot: graphical plotting library for python.
pandas: data processing library for python.
hdbscan: library containing optimised Hierarchical Density-Based Spacial Clustering of Applications with Noise (HSBSCAN) algorithm. 
sklearn: contains clustering (k-means) algorithm, scaling algorithms, example datasets.
	>>StandardScalar: scales data using mean and standard deviation to ensure similar feature ranges.

#data initialisation
* loads data from csv
* removes NaN rows
* applies scaling to data

#HDBSCAN
The HDBSCAN algorithm is a density based clustering algorithm, based upon the preceding 'DBSCAN' algorithm. 
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
Important Method:
.fit_predict() >> Runs HDBSCAN on data and assigns group for each column.

#scatter plot 
Parameters:
x-axis >> df["time_s"],      
y-axis >> df["dq_pC"],       
colour >> c=labels, #labels = HDBSCAN assigned clusters   
colour map >> cmap="tab10",            
marker-size >> s=1, #smallest = 1
transparency >> alpha=1, #no transparency, most efficient 
rasterization >> rasterized = True, #prevents vector shapes, uses pixels as points for better efficiency 
marker-type >> marker = ',' #smallest marker type, better efficiency
