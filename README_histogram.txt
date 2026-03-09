Note: This github repository was created on 08/03/26. Development was initially being organised and logged locally.
The original creation of this program was on the 02/03/26.

Required libraries:
matplotlib.pyplot: graphical plotting library for python.
matplotlib.colors >> LogNorm: for plotting colour gradients on a log scale.
pandas: data processing library for python.
numpy: math library for python.

#data initialisation
* create dataframe, read data from csv
* drop NaN rows
* optional filter
* remove negative and zero values for delta t from dataframe

#bins
* log spaced bins for delta t
* 150 bins between min and max values

* 1 bin per phase degree from 0-360
* 361 bins total

#histogram plot
* plot of phase_deg vs. d_time_s
* bins specified as above
* PD counts taken as the number of rows that occupy the same bins
* colour gradient is logarithmic
 