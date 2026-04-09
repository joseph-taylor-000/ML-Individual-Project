Required libraries:
matplotlib.pyplot: graphical plotting library for python.
from matplotlib.colors import LogNorm: allows for logarithmic colour plotting.
pandas: data processing library for python.
numpy: math library for python.
glob: file directory library for python.
------------------------------------------
#data initialisation
>>directory selection (different time ranges)
>>file sorting - numerical
>>determine max and min charge values accross all files for histogram ranges
>>define linearly spaced bins - phase between 0-360, charge between min-max values
------------------------------------------
#histogram creation
>>create empty numpy array (zeros) for global histogram
>>create numpy histogram for each file from file directory
>>add to global histogram
-----------------------------------------
#plot histogram
plt.imshow(
    hist.T, #fix imshow transposition
    origin="lower", #fix default imshow origin position
    aspect="auto",
    norm=LogNorm(vmin = 1, vmax = hist.max()), #log colours
    extent=[0, 360, q_min, q_max] #set x range, y range
)