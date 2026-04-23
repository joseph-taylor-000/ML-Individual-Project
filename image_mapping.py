import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mplimg
from matplotlib.colors import LogNorm
import glob

#data initialisation
directory_val = 3 
use_region = True #ensure directory_val is set to correspond with region
threshold = 50 #white zone

#directory selection
if directory_val == 1:
    directory = r"M:\OneDrive - The University of Manchester\ML_dataset\New datasets_Sample S4.4\LIGHT IMAGES\S4.4_0 to 1 h\*"+".jpg" #0-1hr
elif directory_val == 2:
    directory = r"M:\OneDrive - The University of Manchester\ML_dataset\New datasets_Sample S4.4\LIGHT IMAGES\S4.4_252to253h\*"+".jpg" #252 to 253hr
elif directory_val == 3:
    directory = r"M:\OneDrive - The University of Manchester\ML_dataset\New datasets_Sample S4.4\LIGHT IMAGES\S4.4_255to256h\*"+".jpg" #255 to 256hr

files = glob.glob(directory)
files_np = np.array(files) #numpy array for later indexing
fig, ax = plt.subplots()

#determine first file time to determine time passed
file_time_1 = files[0].rsplit("diff_30", 1)[1].replace(" .jpg", '') #extract first file time in 00 00 00 format
file_time_1 = file_time_1.rsplit(" ", 2) #split file time into hours, mins, seconds as different array elements
file_time_sec_1 = (int(file_time_1[0])*3600)+(int(file_time_1[1])*60)+(int(file_time_1[2])) #convert file time to seconds

#use only extracted region
if use_region == True:
    #init region directory into dataframe
    reg_dir = r"M:\OneDrive - The University of Manchester\ML_Individual_Project\HDBSCAN_cluster_-1_with_time.txt"
    df = pd.read_csv(reg_dir, usecols=["time_s"])
    df = df.to_numpy() #numpy array of time tuples

    file_list = []
    for i in range(np.shape(df)[0]-1): #iterate through numpy array
        for file in files:
            #print(df[i])
            #print(file)
            #print(files.index(file))

            #calculate file time in seconds
            file_time = file.rsplit("diff_30", 1)[1].replace(" .jpg", '')
            file_time = file_time.rsplit(" ", 2)
            file_time_sec = (int(file_time[0])*3600)+(int(file_time[1])*60)+(int(file_time[2]))

            #print(df[i])
            #print(file_time_sec-file_time_sec_1)

            #find closest image capture
            if abs((file_time_sec-file_time_sec_1) - df[i])<20: #20 seconds between images
                file_list.append(files.index(file))

    files_np = files_np[file_list] #keep only files with index in file_list
    print(files_np)

    for file in np.unique(files_np):
        img = mplimg.imread(file) #2D int array of img intensity values
        print(img)

        y, x = np.where(img > threshold) 
        #img is 2D array of intensity values corresponding to position. 
        #select values bright enough to indicate discharge
        #returns row first (y)

        intensity = img[y, x] #1D list of all intensity values

        scatter = ax.scatter(
                x,
                y,
                c=intensity,
                norm=LogNorm(vmin=threshold, vmax=intensity.max()),
                cmap="plasma", #gist_rainbow for greater contrast between all regions, plasma for clear high/low regions
                marker = '.',
                s=10,
                alpha=0.6
            )
        
    ax.set_facecolor((0, 0, 0))
    ax.set_xlabel("X-position (pixel)")
    ax.set_ylabel("Y-position (pixel)")
    ax.set_title("Light Intensity Plot")
    fig.colorbar(scatter, ax=ax, label="Light Intensity [log scale]") 

    plt.tight_layout()
    plt.show() 
        
#-----------------------------------------------------------------------------------------------------

if use_region == False: 
    #period = input("Enter desired period for analysis: | format(hr/min/sec): 00 00 00")
    period = "01 00 00" #hardset
    period = period.rsplit(" ", 2)
    period_sec = (int(period[0])*3600)+(int(period[1])*60)+(int(period[2])) #second conversion

    file_times = [file_time_sec_1, 0] #comparitor array for two int elements, 0 is placeholder
    i = len(files)-1

    for file in files[:i]:
        print(file)
        print(files.index(file))

        #calculate file time in seconds
        file_time = file.rsplit("diff_30", 1)[1].replace(" .jpg", '')
        file_time = file_time.rsplit(" ", 2)
        file_time_sec = (int(file_time[0])*3600)+(int(file_time[1])*60)+(int(file_time[2]))

        #add to comparitor
        file_times[1] = file_time_sec

        #stop looping when specified period has been reached
        if (file_times[1]-file_times[0]>= period_sec):
            i = files.index(file)
            break


    for file in files[:i]:
        img = mplimg.imread(file) #2D int array of img intensity values
        print(img)

        y, x = np.where(img > threshold) 
        #img is 2D array of intensity values corresponding to position. 
        #select values bright enough to indicate discharge
        #returns row first (y)

        intensity = img[y, x] #1D list of all intensity values

        scatter = ax.scatter(
                x,
                y,
                c=intensity,
                norm=LogNorm(vmin=threshold, vmax=intensity.max()),
                cmap="plasma", #gist_rainbow for greater contrast between all regions, plasma for clear high/low regions
                marker = '.',
                s=10,
                alpha=0.6
            )

    ax.set_facecolor((0, 0, 0))
    ax.set_xlabel("X-position (pixel)")
    ax.set_ylabel("Y-position (pixel)")
    ax.set_title("Light Intensity Plot")
    fig.colorbar(scatter, ax=ax, label="Light Intensity [log scale]") 

    plt.tight_layout()
    plt.show() 