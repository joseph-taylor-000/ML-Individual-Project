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

* create 1500 delta t bins using log spacing between the min/max values
* create 361 phase bin using linear spacing between 0 and 360
* define global histogram

--------------------------
#histogram plotting
for each file:
* create numpy.histogram2d histogram
* add to global histogram


#plot
plt.imshow(
    hist.T, #fix imshow transposition
    origin="lower", #fix default imshow origin position
    aspect="auto",
    norm=LogNorm(vmin = 1, vmax = hist.max()), #log colours
    extent=[0, 360, dt_min, dt_max] #set x range, y range
)
