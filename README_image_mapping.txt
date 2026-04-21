Required Libraries: 
matplotlib: graphical plotting library for python.
pandas: data processing library for python.
numpy: math library for python.
glob: file directory library for python.

#data initialisation
* select directory
* select time period for analysis
* load files from directory
* determine start time for peroid (first file in directory)
* determine end time file index for period
* define pixel brightness threshold for noise rejection

#plot light captures
* load images file by file into 2D intensity array
* split 2D intensity array into x and y components and filter noise using threshold value
* create 1D array of remaining image intensity values
* add x and y values to scatter plot with corresponding intensity colour grading


