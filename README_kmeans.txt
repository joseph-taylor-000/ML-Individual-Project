Note: This github repository was created on 08/03/26. Development was initially being organised and logged locally.
The original creation of this program was on the 17/12/25.

Required libraries:
numpy: math library for python.
pandas: data processing library for python.
matplotlib.pyplot: graphical plotting library for python.
sklearn: contains clustering (k-means) algorithm, scaling algorithms, example datasets.
	>>KMeans: full k-means algorithm
	>>StandardScalar: scales data using mean and standard deviation to ensure similar feature ranges.

#data init
* loads directory as raw string, ignoring '\' conflicts
* reads data from csv using pandas
* removes rows with NaN data in time or charge columns
* converts to numpy 2D array
* scales whole data loaded ~explain scaling algorithm
* optional 2pC filter in charge column for 'noise' or low level microdischarges
* percentage normalisation for charge

#elbow method
The elbow method is a common ML practice for determining the success of 'k' specific grouping in k-means.
Loss is calculated using the kmeans.inertia method, which calculates the sum of the squared distances of each point to its cluster centroid.
This indicates how accurate the grouping is for k groups (closer to centroid = closer group).
However, to remove the risk of overfitting, the ideal k value is determined using the loss score combined with a second difference method.
Thus, the greatest change in loss can be found and this k value can be used. 

	Algorithmically:
		>>k-means performed on data for a range of k values
		>>loss score for each value appended to list
		>>first difference calculated
		>>second differences calculated
		>>ideal k value: index of max second difference value +2
			*+2 added as second index of second difference coincides with k value of 2
		>>plots loss against k for visual inspection

#k-means algorithm
This program uses the optimised built-in version of k-means for scikitlearn. This is an unsupervised clustering method which uses point geometry to find ideal groupings.
A first pass will randomly assign 'k' centroid locations. The data points will be assigned a centroid based on linear distance. Once all points are assigned a centroid, the
centroid location is recalculated as the centre of the points which belong to it. The groups are then recalculated and the change in the centroid positions are stored at each step.
Once the centroid locations reach a stable point of location change, the algorithm finishes.

This program:
* runs k-means 
* plots time vs. charge with colour groupings and centroids.

	 





