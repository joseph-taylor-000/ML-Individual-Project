Note: This github repository was created on 08/03/26. Development was initially being organised and logged locally.
The original creation of this program was on the 26/02/26.

Required libraries:
matplotlib.pyplot: graphical plotting library for python.
pandas: data processing library for python.
numpy: math library for python.

#data initialisation
* create pandas dataframe from csv file 
* drop NaN rows from df
* optionally filter magnitude ranges

#grouping
* create dataframe column for microsecond time intervals
* create new dataframe with time intervals, 
  and the corresponding PD count values for each interval
* sort the dataframe in ascending order
* new dataframe created for plotting with .reset_index() adding a separate column for the index.
* time intervals restored to original values.

#plot
single axis plot:
x-axis: time
y-axis: partial discharge counts

