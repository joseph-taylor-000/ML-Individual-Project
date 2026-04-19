Required libraries:
matplotlib.pyplot: graphical plotting library for python.
matplotlib.patches: allows for geometry to be drawn on plots
pandas: data processing library for python.
numpy: math library for python.
sklearn: contains clustering (k-means) algorithm, scaling algorithms, example datasets.
	>>StandardScalar: scales data using mean and standard deviation to ensure similar feature ranges.
	>>GaussianMixture: Gaussian Mixture Model (GMM) Algorithm

#gaussian mixture model (GMM)
This program assigns points to clusters based on the Gaussian Mixture Module algorithm.
This algorithm assumes a Gaussian normal distribution of the points within each cluster.
It assigning probabilties of cluster assignment to each point, based upon calculations of mean and standard deviation done iteratively.
The final clusters are decided based upon each point's membership liklihood.

* GaussianMixture object initialised with parameters:
	gm = GaussianMixture(n_components= 4, #number of clusters
                     	     covariance_type = 'full', #shape of cluster covariance matrix
                     	     random_state= 0, #seed for init params 'random'
                     	     init_params= 'kmeans', #initialises EM algorithm using 'kmeans' / 'random'
                     	      verbose = 1 #iterations displayed
                     	)

#data initialisation
* select file load mode (single / all)
* select file directory
* define GMM clusterer
* init scaler

#SINGLE FILE MODE:
* loads file from directory into data frame
* uses phase and charge columns
* drops NaN rows
* scales data and stores in numpy array
* lables are assigned by fitting GMM to data

#plot
* phase vs. charge magnitude plot
* point colours based on labels
* legend created using patch geometry with label and colour assignment corresponding with scatter plot

#ALL FILES MODE
* load files in dataframes iteratively
for each file:
	* on first pass, fit scaler object to data set using partial fit
	* on second pass, transform data using optimized scaler and determine clusters using GMM clustering
	* plot data on scatter plot

