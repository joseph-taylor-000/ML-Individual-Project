Required libraries:
matplotlib.pyplot: graphical plotting library for python.
matplotlib.colors >> LogNorm: for plotting colour gradients on a log scale.
pandas: data processing library for python.
glob: file management library for python

#data initialisation
* read files from directory:
* sort files
for each file:
* drop NaN rows
* optional filter
* remove negative and zero values for delta t from dataframe for log compatibility
* create delta t bin by rounding to 7dp
* create phase bin by rounding to nearest degree
* create new dataframe with count column to quantify the number of events which share phase and time bin

#plot
* scatter plot:
	>>x-axis: phase
	>>y-axis: delta t
	>>colour grading: based density, log scale between 1 and max value for the file