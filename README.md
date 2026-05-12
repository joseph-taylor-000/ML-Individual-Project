<img src="images/3.14_python.png" width="100" alt="Autoencoder network diagram"><h1 align="center">ML Assisted Partial Discharge Analysis</h1>

<p align="center">
  <img src="images/Autoencoder network diagram.drawio.png" width="600" alt="Autoencoder network diagram">
</p>
<h2>Overview: </h2>
This code repository contains the library installation instructions, source code and alogrithmic explanations related to the author's 'Advancing the Fundamental Understanding of Electrical Tree Initiation Mechanisms using ML Assisted Data Analysis' dissertation project.
Each branch corresponds to a specific area of investigation as intuitive, these include: Autoencoder, Density, Gaussian-Mixture-Modelling, HDBSCAN, Image-Processing, K-means. Within each of these, a separate README file is available with a description of the corresponding program e.g. README_HDBSCAN.
The contents of these README file have been collated in this complete repository README, complete with flowcharts for each program.
<h2>Required Libraries: </h2>
Default Python Libraries:
These libraries come pre-installed with python 3.14 and do not require additional installation.
<ul>
  <li>Glob</li>
  <li>OS</li>
  <li>Time</li>
</ul>
Additional Python Libraries:
These libraries DO NOT come pre-installed with python 3.14 and require additional installation. Instructions for the installation of each library are provided.
<ul>
  <li><a href = https://pandas.pydata.org/docs/getting_started/install.html>PANDAS</a></li>
  <li><a href = https://numpy.org/doc/stable/user/absolute_beginners.html>NumPy</a></li>
  <li><a href = https://matplotlib.org/stable/users/explain/quick_start.html>Matplotlib</a></li>
  <li><a href = https://pytorch.org/>Pytorch</a></li>
  <li><a href = https://pypi.org/project/river/>River</a> - River library is supported up to Python version 3.12.0 and requires prerequisite installations of both Cython and Rust. 
This is because some of the machine learning algorithms available in river require high speed loops or strict memory management.
By implementing these features using Cython or Rust, python interpreter overhead is lost and this speed can be achieved.
</li>
</ul>
<h2>Density Branch: </h2>
This branch contains scripts tailored towards analysing event frequency trends and PD event structure in several domains.
<h3>Time Density: </h3>
Data initialisation:

* select directory
* load directory into files 
* drop NaN rows from df
* optionally filter magnitude ranges
* create global dataframe for density readings

Grouping:
* create dataframe column for rounded phase degrees
* create new dataframe with columns:
	* time_us as the index,  
	* the corresponding count values for each phase group,  <br>
	* the total charge for that group in another, <br>
	* the count value of only positive magnitude events, <br>
	* the total charge of positive events, <br>
	* the count value of only negative magnitude events, <br>
	* the total charge value of negative events, <br>

* new dataframe created for plotting with .reset_index() adding a separate column from time_us for the index.
* RMS calculated for all values, only positive values, only negative values calculated
* add file dataframe to plot

Plot:
3 plots, one for all data, one for positive, one for negative <br>
twin axis plots: <br>
ax1: density vs. time, <br>
ax2: RMS PD magnitude vs. time <br>

<h3>Phase Density: </h3>

Data initialisation:
* select directory
* load directory into files 
* drop NaN rows from df
* optionally filter magnitude ranges
* create global dataframe for density readings

Grouping:
* create dataframe column for rounded phase degrees
* create new dataframe with columns:
	* rounded phase degrees as the index, <br> 
	* the corresponding count values for each phase group, <br> 
	* the total charge for that group in another, <br>
	* the count value of only positive magnitude events, <br>
	* the total charge of positive events, <br>
	* the count value of only negative magnitude events, <br>
	* the total charge value of negative events, <br>

* dataframe is then reindexed to include 360 rows
* new dataframe created for plotting with .reset_index() adding a separate column from phase_deg_rounded for the index.
* values added to global dataframe
* global RMS for all values, only positive values, only negative values calculated

Plot: <br>
3 plots, one for all data, one for positive, one for negative <br>
twin axis plots:  <br>
ax1: density vs. phase, <br>
ax2: RMS PD magnitude vs. phase <br>

<h3>Δt-phase Event Frequency Histogram: </h3> 

Data initialisation:
* create dataframe, read data from csv
* drop NaN rows
* optional filter
* remove negative and zero values for delta t from dataframe

Binning:
* log spaced bins for delta t
* 150 bins between min and max values
* 1 bin per phase degree from 0-360
* 361 bins total

Histogram plot:
* plot of phase_deg vs. d_time_s
* bins specified as above
* PD counts taken as the number of rows that occupy the same bins
* colour gradient is logarithmic
 
<h3>Δt-PRPD heatmap</h3>

Data initialisation:
* read files from directory
* sort files
* determine global min/max delta t values for all files

For each file:
* drop NaN rows
* optional filter
* remove negative and zero values for delta t from dataframe for log compatibility

Scatter Plot:
* x-axis: phase
* y-axis: PD Magnitude
* colour grading: based on Δt, log scale between minimum and maximum values

<h2>K-means Branch: </h2>
This branch contains scripts for single file and multi-file k-means clustering algorithms.

<h3>Single File K-means: </h3>
Data initialisation:
* loads directory as raw string, ignoring '\' conflicts
* reads data from csv using pandas
* removes rows with NaN data in time or charge columns
* converts to numpy 2D array
* scales whole data loaded ~explain scaling algorithm
* optional 2pC filter in charge column for 'noise' or low level microdischarges
* percentage normalisation for charge
<br>
<br>
Elbow method: <br>
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

K-means algorithm: <br>
This program uses the optimised built-in version of k-means for scikitlearn. This is an unsupervised clustering method which uses point geometry to find ideal groupings.
A first pass will randomly assign 'k' centroid locations. The data points will be assigned a centroid based on linear distance. Once all points are assigned a centroid, the
centroid location is recalculated as the centre of the points which belong to it. The groups are then recalculated and the change in the centroid positions are stored at each step.
Once the centroid locations reach a stable point of location change, the algorithm finishes.

This program:
* runs k-means 
* plots time vs. charge with colour groupings and centroids.

Program Flowchart: <br>
<img src="images/K-means Streaming Algorithm.drawio.png" alt="K-means Diagram">

<h3>Multi-file K-means: </h3>
Data initialisation: <br>
* directory selected by user
* domain selected by user
* loads directory as raw string, ignoring '\' conflicts
* creates list of files in directory using glob
* files are sorted to be read in numerical order
* number of files to be used manually specified

Elbow method updates for streaming application:
* subsection of files selected that is representative of whole data.
* files concatenated to single list
* scaling applied
* elbow inertia method as before.
	>>second difference found using gradient of curve (numpy) for more accurate elbow
* elbow plotted on graph

Chunked k-means algorithm: <br>
Kmeans algorithm works as above, however, MiniBatchKMeans uses small subsections of whole data (batch size = 10000). Each batch is scaled separately, with a scaling pass being performed first for all files to ensure correct scaling parameters (mean, sd) for the k-means pass.

Scatter plotted file by file. 'cluster' field added to dataframe to assign grouping to data row 
>> {df["cluster"]=kmeans.predict(X)}.

Parameters: <br>
x-axis >> df["time_s"],      
y-axis >> df["dq_pC"],       
colour >> c=df["cluster"],   
colour map >> cmap="tab10",            
marker-size >> s=1, #smallest = 1
transparency >> alpha=1, #no transparency, most efficient  <br>
rasterization >> rasterized = True, #prevents vector shapes, uses pixels as points for better efficiency <br>
marker-type >> marker = '.' #smallest marker type, better efficiency <br>

Legend:
* colours added to list from colour map
* handles created using patch geometry, with each colour and a cluster label

<h2>HDBSCAN Branch: </h2>
This branch contains scripts for streamed HDBSCAN and DBSCAN clustering.

<h3>HDBSCAN Library Approach: </h3>
This approach uses the HDBSCAN library. <br>

Data initialisation:
* select domain
* select input directory and output directory
* check output directory exists
* loads data from input directory folder
* sorts data numerically
* splits data into training sample and test data

Training:
* for each file:
	>> creates dataframe
	>> chooses sample from data
    >> records sample indices for later separation
	>> removes NaN rows
	>> applies scaling to data
	>> adds to data list
* data list is then concatenated
* HDBSCAN performed on sample

HDBSCAN: <br>
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
Scaler Class: <br>
.fit(data) >> calculates mean and standard deviation for data <br>
.fit_transform(data) >> calculates mean and standard deviation for data and then scales data accordingly <br>
.partial_fit(data) >> calculates mean and standard deviation for subsection of data, accumulates for whole data <br>
.transform(data) >> uses precalculated scaler parameters to standardize data <br>

HDBSCAN Class: <br>
.approximate_predict(model, data) >> uses pretrained algorithm model on data to approximate clusters. <br>
.fit_predict() >> Runs HDBSCAN on data and assigns group for each column. <br>
<br>

Using approximate_predict, it is possible to integrate multiple files into the HDBSCAN algorithm and plot the results on the same axis.
This code version uses a for loop to perform approximate cluster predictions for each file within the test data; 
ensuring that test data samples are not shared with training data using saved indices.

Program Flowchart: <br>
<img src="images/HDBSCAN Flowchart.drawio.png" alt="HDBSCAN Diagram">

Scatter plot: <br>
x-axis >> df["time_s"],    
y-axis >> df["dq_pC"],    
colour >> c=cluster, #cluster = HDBSCAN assigned clusters  
colour map >> cmap="tab10",         
marker-size >> s=1, #smallest = 1 <br>
transparency >> alpha=1, #no transparency, most efficient <br>
rasterization >> rasterized = True, #prevents vector shapes, uses pixels as points for better efficiency <br>
marker-type >> marker = ',' #smallest marker type, better efficiency <br>

A for loop is used to assertain the colours used for each cluster and assign them to the graphs legend.

	Cluster information is separated into multiple files:
		for cluster, group in df.groupby("cluster"): #for each unique cluster, group is the corresponding subsection of dataframe <br>
		        file_path = os.path.join(output_dir, f"HDBSCAN_cluster_{cluster}.txt") #separate files for each cluster <br>
		        group.to_csv( <br>
		            file_path, <br>
		            mode="a", #append <br>
		            header=not os.path.exists(file_path), #only write header if first file <br>
		            index=False <br>
		        ) <br>

<h3>DenStream Approach: </h3>
This approach uses the DenStream class from the River library. <br>
Note: DenStream was posed as an alternative to the streaming HDBSCAN used in the final report however it has been omitted from the final report due to poor results / redundancy and excessive load times.

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

Data initialisation: 
* specifies input directory and output directory for cluster information
* creates/validates output directory
* loads files from input directory into list
* sorts file list numerically

DenStream:
'DenStream is a clustering algorithm for evolving data streams. DenStream can discover clusters with arbitrary shape and is robust against noise (outliers).'[1] 
Essentially, DenStream is a density based clustering algorithm that can be used with streaming data to perform a function analagous to DBSCAN clustering. 
It has been implemented to solve memory complications associated with the traditional DBSCAN.
Since it does not require a complete KNN tree of all the data to be loaded into memory, the algorithm can perform clustering on the whole data without requiring massive amounts of memory.

Parameters [1]:<br>
decaying_factor: controls the impact of historical data on current cluster. >>0.01 has been chosen to investigate the clusters assuming that previous discharge events have a significant impact on current discharges.<br><br>
beta / mu: controls the distance threshold from micro cluster centres at which points are considered noise (beta*mu > 1).>>beta = 0.5, mu = 2.001  have been chosen to minimise noise tolerance to isolate abnormal regions as noise and extract them for further investigation using HDBSCAN.<br><br>
epsilon: defines the neighbourhood radius for density clustering as in DBSCAN >> set at 0.9 to produce several clusters but preventing overfitting at lower epsilon values.<br><br>
n_samples_init: defines the number of data points used to form the initial microclusters withing the data before streaming begins >>1000 is the default value and is usually sufficient (even for large datasets) as streaming means the clusters adapt with more data anyway.<br><br>

Streaming and Plotting:
For each file in file directory:
* moves data into dataframe, keeps only phase_deg and q_pC columns to reduce bloat
* removes NaN rows
* to extract abnormal regions, filter is applied (df[(df["q_pC"] <= 0) & (df["phase_deg"] <= 180)])
* dataframe is scaled using numpy array, saved into new df_scaled
* df_scaled processed iteratively per row
* for each row, a dictionary is generated using phase and q_pC columns from df_scaled.
* this is so that the .learn_one() and predict_one() methods from the River cluster library can be used to implement the denstream algorithm.
	pass 1 >> .learn_one(X) updates the model with a new set of features X [1] <br>
	pass 2 >> .predict_one(X) predicts the cluster value for a new set of features X [1]<br>
* cluster IDs are then added to dataframe
* dataframe rows saved to text files based on their cluster value
* new file dataframe rows are appended to existing text files
* dataframe plotted with cluster-based colour grading for each point 

<h2>Gaussian-Mixture-Model Branch: </h2>

<h3>Gaussian-Mixture-Model (GMM)</h3>
This program assigns points to clusters based on the Gaussian Mixture Module algorithm.
This algorithm assumes a Gaussian normal distribution of the points within each cluster.
It assigning probabilties of cluster assignment to each point, based upon calculations of mean and standard deviation done iteratively.
The final clusters are decided based upon each point's membership liklihood.

	GaussianMixture object initialised with parameters:
		gm = GaussianMixture(n_components= 4, #number of clusters
	                     	     covariance_type = 'full', #shape of cluster covariance matrix
	                     	     random_state= 0, #seed for init params 'random'
	                     	     init_params= 'kmeans', #initialises EM algorithm using 'kmeans' / 'random'
	                     	      verbose = 1 #iterations displayed
	                     	)

Program Flowchart: <br>
<img src="images/GMM Flowchart.drawio.png" alt="GMM Diagram">

Data initialisation:
* select file load mode (single / all)
* select domain (phase / time)
* select file directory
* define GMM clusterer
* init scaler

Single File Mode:
* loads file from directory into data frame
* uses phase and charge columns
* drops NaN rows
* scales data and stores in numpy array
* lables are assigned by fitting GMM to data
* plot data on scatter plot

All Files Mode:
* load files in dataframes iteratively
* for each file:
	* on first pass, fit scaler object to data set using partial fit
	* on second pass, transform data using optimized scaler and determine train cluster distribution parameters
	* on third pass, transform data using otimized scaler and determine GMM cluster labels
	* plot data on scatter plot

Plot:
* phase vs. charge magnitude / time vs. charge magnitude plot 
* point colours based on labels
* legend created using patch geometry with label and colour assignment corresponding with scatter plot

<h2>Autoencoder Branch: </h2>

<h3>Autoencoder:</h3>
This program uses Pytorch to create an autoencoder network. 
This is a type of neural network used to deconstruct and reconstruct a given input. 
In the class definition, the process can be described algorithmically:

Important methods:
* nn.Linear(input_data_size, output_data_size) - applies a linear transformation to data, transforming input to output size<br>
* nn.ReLU() - applies rectified linear units activation function:<br>

				  3|     /      ReLU: max(0, x) >>> returns x if greater than 0
				   |    /       This works well for activation as negitive values are ignored,
				  2|   /        positive values are represented linearly.
  				   |  /
				  1| /
  		_________|/_____
		-3 -2 -1 0 1 2 3 

Encoder function - encodes data to reduced representation: <br>
encoder:  Linear transform --> ReLU Activation --> Linear transform --> ReLU Activation --> 
          Linear transform --> ReLU Activation --> Linear transform (Decreasing input size gradually from initial to initial/16)

Decoder function - decodes encoded data to recreate input data:<br>
decoder:  Linear transform --> ReLU Activation --> Linear transform --> ReLU Activation --> 
          Linear transform  (Increasing input size gradually from initial/16 to initial)

Forward function - forward pass through autoencoder network: <br>
forward: input --> encoder --> code --> decoder --> output

Histogram generator function: <br>
creates numpy histogram, will be implemented to create PRPD histogram dataset

Program Flowchart: <br>
<img src="images/Autoencoder Flowchart.drawio.png" alt="Autoencoder Diagram">

Data initialisation:
* directory selection (different time ranges)
* file sorting - numerical
* determine max and min charge values accross all files for histogram ranges
* define linearly spaced bins - phase between 0-360, charge between min-max values
* create histograms using high-level PD data. Use 10,000 rows per histogram then move to next 10,000
* flatten histograms to 1 dimensional representation and convert to Tensor for non-linear autoencoder
* enable GPU processing to decrease training time
* apply signed min-max (-1, 1) normalisation to avoid phase-magnitude skew, prepare autoencoder for future normalised ranges
* create data loader to batch training

Autoencoder training:
* instantiate autoencoder object with training data histogram size as input size
* criterion - function to minimise , set as mean square error loss function: 
	* (1/N)Σ{lower: i=0; upper: N}|Y_i - Y{Pk}_i| - will be used to determine loss at each epoch, where  N = epochs, Y_i = input, Y{Pk}_i = reconstructed
* optimiser - Adam optimiser used to train model, learning rate set to 1e-3 as common, weight decay set to 1e-5 as common
* epochs = 50 i.e. 50 training cycles
	In each epoch:
	* load batch into autoencoder
	* autoencoder calls forward() method --> puts data through network
	* calculate loss using criterion (MSE loss)
optimisation steps:
	* reset gradient to avoid accumulation
	* calculate ideal weight values for network using backpropagation (calculate gradients)
	* update weight values according to Adam optimiser 
	(weight = weight - learning_rate * gradient, where gradient is d(loss)/d(weight) and learning rate is constant)

Data testing:
* create histogram set for test data
* convert set to tensor, signed min-max normalise

Data reconstruction comparisons:
Compare original input data to autoencoder reconstruction graphically to determine effectiveness of network's relvant feature preservation
For both training data (complete recreation) and test data (unknown recreation):
* disable weight training for test period
* create reconstruction using trained model and input data
* determine error using mean square difference of input-reconstruction in single dimension (per row)
* create dataset for histogram representation using input data first element (first sample)
* create dataset for histogram representation using reconstruction data first element (first sample)
* filter out histogram entries that do not meet average error threshold, keep only histograms that have analogous activity <br>

Create plots for original and reconstructed: <br>
	
			plt.subplot(1,2,1) #plot grid layout: 1 row, 2 graphs, 1st graph
			    plt.title("xxx Data") 
			    plt.imshow(original.T, #fix imshow default transposition
			               aspect='auto',
			               origin='lower', #fix imshow default origin
			               extent=[0, 360, q_min, q_max]) #set graph limits 0-360 for phase, min-max for charge
			    plt.colorbar()
				
<h3>PRPD Histogram Streaming:</h3>

Data initialisation: <br>
* directory selection (different time ranges)
* file sorting - numerical
* determine max and min charge values accross all files for histogram ranges
* define linearly spaced bins - phase between 0-360, charge between min-max values

Histogram creation: <br>
* create empty numpy array (zeros) for global histogram
* create numpy histogram for each file from file directory
* add to global histogram

Plot histogram: <br>
				<code>plt.imshow(
				    hist.T, #fix imshow transposition
				    origin="lower", #fix default imshow origin position
				    aspect="auto",
				    norm=LogNorm(vmin = 1, vmax = hist.max()), #log colours
				    extent=[0, 360, q_min, q_max] #set x range, y range
					)</code>
		
<h2>Image-Processing Branch:</h2>

<h3>Image-mapping:</h3>
The purpose of this program was to collate image captures from specific times and regions to identify patterns or light localisation.

Program Flowchart: <br>
<img src="images/Image Analysis Flowchart.drawio.png" alt="Image-mapping Diagram">

Data initialisation: <br>
* select directory
* select file mode
* determine start time for peroid (first file in directory)
* define pixel brightness threshold for noise rejection

Single file: <br>
* load single file from directory 
* determine closest image file time
* modify file list to exclude all other files

All files: <br>
* select time period for analysis
* load files from directory
* determine end time file index for period

Plot light captures:  <br>
* load images file by file into 2D intensity array
* split 2D intensity array into x and y components and filter noise using threshold value
* create 1D array of remaining image intensity values
* add x and y values to scatter plot with corresponding intensity colour grading

<h2>AI Disclaimer: </h2>
Throughout this project, ChatGPT was used to aid the planning and general discussion of program logic pre-development.<br>
This included in-depth negotiations considering conventional approaches and their problem-specific integration solutions.<br>
For example, one of these discussions was to develop an overview of the typical HDBSCAN library approach and how it could be adapted to a streaming approach.
A typical prompt would have been 'What is the best library to use for reading many files? Show examples'.<br>
ChatGPT was also used in code debugging, following typical prompts such as:<br>
'Explain this error' or 'What is wrong with this code block?'.<br>
The use of AI within this project conforms to all standards of academic integrity enforced by the University of Manchester [2].

<h2>References:</h2>
[1] River DenStream. Available at (https://riverml.xyz/0.20.1/api/cluster/DenStream/) (Accessed 11 March 2026). <br>
[2] “Academic Integrity,” University of Manchester Library, [Online]. Available: https://www.education.library.manchester.ac.uk/mle/academic-integrity/#/lessons/sKF9jqPXxLIj_kjNJqwjLwtEeDtFiNaJ
. [Accessed: May 5, 2026].
