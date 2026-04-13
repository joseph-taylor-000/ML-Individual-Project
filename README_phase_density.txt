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
* create global dataframe for density readings

#grouping
* create dataframe column for rounded phase degrees
* create new dataframe with columns:
>>rounded phase degrees as the index 
>>the corresponding count values for each phase group 
>>the total charge for that group in another
>>the count value of only positive magnitude events
>>the total charge of positive events
>>the count value of only negative magnitude events
>>the total charge value of negative events

* dataframe is then reindexed to include 360 rows
* new dataframe created for plotting with .reset_index() adding a separate column from phase_deg_rounded for the index.
* values added to global dataframe
* global RMS for all values, only positive values, only negative values calculated

#plot - 3 plots, one for all data, one for positive, one for negative
twin axis plots: 
ax1: density vs. phase, 
ax2: RMS PD magnitude vs. phase

