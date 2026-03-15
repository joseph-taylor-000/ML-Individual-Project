import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mplimg
from matplotlib.colors import LogNorm
import glob
import os

directory = r"M:\OneDrive - The University of Manchester\ML_dataset\S4.4_Sample with usual arrangement\Processed images_0 to 96 hours\100325\*"+".jpg"
files = glob.glob(directory)
#files = files[:1]
fig, ax = plt.subplots()

for file in files:
    img = mplimg.imread(file)
    print(img)
    threshold = 80 #white zone

    y, x = np.where(img > threshold) 
    #img is 2D array of intensity values corresponding to position. 
    #select values bright enough to indicate discharge

    intensity = img[y, x] #list of all intensity values

    scatter = ax.scatter(
            x,
            y,
            c=intensity,
            norm=LogNorm(vmin=50, vmax=255),
            cmap="plasma",
            marker = '.',
            s=10,
            alpha=0.6
        )


ax.set_xlabel("X-position (pixel)")
ax.set_ylabel("Y-position (pixel)")
ax.set_title("Light Intensity Plot")
fig.colorbar(scatter, ax=ax, label="Light Intensity [log scale]") 

plt.tight_layout()
plt.show()