import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mplimg
from matplotlib.colors import LogNorm
import glob
import os

directory = r"M:\OneDrive - The University of Manchester\ML_dataset\S4.4_Sample with usual arrangement\Processed images_0 to 96 hours\100325\0 h - 2h\diff_10*"+".jpg"
files = glob.glob(directory)
files = files[:227]
fig, ax = plt.subplots()

#period = input("Enter desired period for analysis: | format(hr/min/sec): 00 00 00")
period = "01 00 00" #hardset
period_sec = (int(period.rsplit(" ", 2)[0])*3600)+(int(period.rsplit(" ", 2)[1])*60)+(int(period.rsplit(" ", 2)[2])) #repeated rsplit inefficient

file_time_1 = files[0].rsplit("diff_10", 1)[1].replace(" .jpg", '')
file_time_sec_1 = (int(file_time_1.rsplit(" ", 2)[0])*3600)+(int(file_time_1.rsplit(" ", 2)[1])*60)+(int(file_time_1.rsplit(" ", 2)[2]))

file_times = [file_time_sec_1, 0]
i = len(files)-1

for file in files[:i]:
    print(file)
    print(files.index(file))

    file_time = file.rsplit("diff_10", 1)[1].replace(" .jpg", '')
    file_time_sec = (int(file_time.rsplit(" ", 2)[0])*3600)+(int(file_time.rsplit(" ", 2)[1])*60)+(int(file_time.rsplit(" ", 2)[2]))
    file_times[1] = file_time_sec
    if (file_times[1]-file_times[0]>= period_sec):
        i = files.index(file)
        break

#light detection
threshold = 50 #white zone

for file in files[:i]:
    img = mplimg.imread(file)
    #print(img)
    

    y, x = np.where(img > threshold) 
    #img is 2D array of intensity values corresponding to position. 
    #select values bright enough to indicate discharge

    intensity = img[y, x] #list of all intensity values

    scatter = ax.scatter(
            x,
            y,
            c=intensity,
            norm=LogNorm(vmin=1, vmax=255),
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