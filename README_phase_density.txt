Note: This github repository was created on 08/03/26. Development was initially being organised and logged locally.
The original creation of this program was on the 26/02/26.

Required libraries:
matplotlib.pyplot: graphical plotting library for python.
pandas: data processing library for python.
numpy: math library for python.

#data initialisation
* create pandas dataframe from csv 
* drop NaN rows from df
* optionally filter magnitude ranges

#grouping
* create dataframe column for rounded phase degrees
* create new dataframe with rounded phase degrees as the index, 
  the corresponding count values for each phase group in one column, 
  and the mean charge for that group in another.
* dataframe is then reindexed to include 360 rows and fills columns for missing phases with 0.
* new dataframe created for plotting with .reset_index() adding a separate column from phase_deg_rounded for the index.
* dataframe saved to csv for sanity checking.

#plot
twin axis plot: 
ax1: density vs. phase, 
ax2: mean PD magnitude vs. phase

