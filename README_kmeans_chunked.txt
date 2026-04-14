Note: This github repository was created on 08/03/26. Development was initially being organised and logged locally.
The original creation of this program was on the 23/12/25.

Required libraries:
numpy: math library for python.
pandas: data processing library for python.
matplotlib.pyplot: graphical plotting library for python.
matplotlib.colors: specific colour grading for pyplots.
matplotlib.patches: add geometric shapes to plots
sklearn: contains clustering (k-means) algorithm, scaling algorithms, example datasets.
	>>KMeans: full k-means algorithm
	>>MiniBatchKMeans: 'chunked' k-means algorithm, performs k-means on sections of whole data and combines results.
	>>StandardScalar: scales data using mean and standard deviation to ensure similar feature ranges.
glob: file directory library.

#data initialisation
* directory selected by user
* domain selected by user

* loads directory as raw string, ignoring '\' conflicts
* creates list of files in directory using glob
* files are sorted to be read in numerical order
	>>file name split at 'part'
	>>uses section after 'part'
	>>removes file extension
	>>sorts using integer value remaining
*number of files to be used manually specified

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
			*+2 added as 0 index of second difference coincides with k value of 2
		>>plots loss against k for visual inspection

#elbow method updates for streaming application:
* subsection of files selected that is representative of whole data.
* files concatenated to single list
* scaling applied

* elbow inertia method as before.
	>>second difference found using gradient of curve (numpy) for more accurate elbow
* elbow plotted on graph

#k-means algorithm
This program uses the optimised built-in version of k-means for scikitlearn. This is an unsupervised clustering method which uses point geometry to find ideal groupings.
A first pass will randomly assign 'k' centroid locations. The data points will be assigned a centroid based on linear distance. Once all points are assigned a centroid, the
centroid location is recalculated as the centre of the points which belong to it. The groups are then recalculated and the change in the centroid positions are stored at each step.
Once the centroid locations reach a stable point of location change, the algorithm finishes.

#chunked k-means algorithm
Algorithm works as above, however, MiniBatchKMeans uses small subsections of whole data (batch size = 10000). Each batch is scaled separately, with a scaling pass being performed first for all files to ensure correct scaling parameters (mean, sd) for the k-means pass.

#scatter plot of 
Scatter plotted file by file. 'cluster' field added to dataframe to assign grouping to data row {df["cluster"]=kmeans.predict(X)}.

Parameters:
x-axis >> df["time_s"],      
y-axis >> df["dq_pC"],       
colour >> c=df["cluster"],   
colour map >> cmap="tab10",            
marker-size >> s=1, #smallest = 1
transparency >> alpha=1, #no transparency, most efficient 
rasterization >> rasterized = True, #prevents vector shapes, uses pixels as points for better efficiency 
marker-type >> marker = '.' #smallest marker type, better efficiency

#legend
* colours added to list from colour map
* handles created using patch geometry, with each colour and a cluster label 






