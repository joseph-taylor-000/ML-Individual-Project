Required libraries:
matplotlib.pyplot: graphical plotting library for python.
matplotlib.colors >> LogNorm: for plotting colour gradients on a log scale.
pandas: data processing library for python.
numpy: math library for python.

#data initialisation
* read files from directory:
* sort files
for each file:
* drop NaN rows
* optional filter
* remove negative and zero values for delta t from dataframe for log compatibility

#plot
* scatter plot:
	>>x-axis: phase
	>>y-axis: PD Magnitude
	>>colour grading: based on Δt, log scale between minimum and maximum values
