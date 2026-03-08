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
* loads directory as raw string, ignoring '\' conflicts
* creates list of files in directory using glob
* files are sorted to be read in numerical order
	>>file name split at 'part'
	>>uses section after 'part'
	>>removes file extension
	>>sorts using integer value remaining
*number of files to be used manually specified

#elbow method
Algorithm works as in previous README.

* subsection of files selected that is representative of whole data.
* files concatenated to single list
*scaling applied

* elbow inertia method as before.
	>>second difference found using gradient of curve (numpy) for more accurate elbow
* elbow plotted on graph

#chunked k-means algorithm
Algorithm works as in previous README, however, MiniBatchKMeans uses small subsections of whole data (batch size = 10000). Each batch is scaled separately, with a scaling pass being performed first for all files to ensure correct scaling parameters (mean, sd) for the k-means pass.

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
marker-type >> marker = ',' #smallest marker type, better efficiency

#legend
* colours added to list from colour map
* handles created using patch geometry, with each colour and a cluster label 






