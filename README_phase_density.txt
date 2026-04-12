Note: This github repository was created on 08/03/26. Development was initially being organised and logged locally.
The original creation of this program was on the 26/02/26.

Required libraries:
matplotlib.pyplot: graphical plotting library for python.
pandas: data processing library for python.
numpy: math library for python.
glob: file directory library

#data initialisation
* select directory
* load directory into files 
* drop NaN rows from df
* optionally filter magnitude ranges

#grouping
* create dataframe column for rounded phase degrees
* create new dataframe with columns:
>>rounded phase degrees as the index 
>>the corresponding count values for each phase group 
>>the mean charge for that group in another
>>the count value of only positive magnitude events
>>the mean of positive events
>>the count value of only negative magnitude events
>>the mean value of negative events
* dataframe is then reindexed to include 360 rows
* new dataframe created for plotting with .reset_index() adding a separate column from phase_deg_rounded for the index.
* data from each file in directory is plotted via a streaming for loop, 1 file per iteration

#plot - 3 plots, one for all data, one for positive, one for negative
twin axis plots: 
ax1: density vs. phase, 
ax2: mean PD magnitude vs. phase

