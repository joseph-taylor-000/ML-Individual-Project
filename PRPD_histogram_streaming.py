import pandas as pd
import matplotlib.pyplot as plt
import glob 
from matplotlib.colors import LogNorm
import numpy as np
#------------------------
#data initialisation

#directory selection
directory_val = 3 
use_noise_data = False

#directory selection
if directory_val == 1:
    directory = r"M:\OneDrive - The University of Manchester\ML_dataset\New datasets_Sample S4.4\0 to 1h\*" #0-1hr
elif directory_val == 2:
    directory = r"M:\OneDrive - The University of Manchester\ML_dataset\New datasets_Sample S4.4\252 to 253 h\*" #252 to 253hr
elif directory_val == 3:
    directory = r"M:\OneDrive - The University of Manchester\ML_dataset\New datasets_Sample S4.4\255 to 256 h\*" #255 to 256hr
if use_noise_data == True:
    noise_dir = r"M:\OneDrive - The University of Manchester\ML_dataset\New datasets_Sample S4.4\Noise_0 to 1000s\*" #noise data
else:
    noise_dir = ''

files = glob.glob(directory)
files = files[:1]

files.sort(
    key=lambda f: 
    int(f.rsplit('part', 1)[1]
        .replace('.csv', ''))
) 

fig, ax = plt.subplots()
max_charges = []
min_charges = []

#find min/max charges
for file in files:
    print(file)
    df = pd.read_csv(file, usecols=["phase_deg", "q_pC", "d_time_s"])
    #df = df[(df["q_pC"] <= 1) & (df["q_pC"] >= -1)] #low level filter

    df.dropna(inplace=True)

    max_charges.append(df["q_pC"].max())
    min_charges.append(df["q_pC"].min())

q_min = min(min_charges)
q_max = max(max_charges)

#bin edges 
phase_bins_count = 361 #1 degree binning
q_bins_count = 1500 

phase_bins = np.linspace(0, 360, phase_bins_count) 
q_bins = np.linspace(q_min, q_max, q_bins_count) #linear bins
#q_bins = np.logspace(np.log10(q_min), np.log10(q_max), 20) #LOG bins

#------------------------------------------------------------------

#global histogram
hist = np.zeros((phase_bins_count-1, q_bins_count-1), dtype=np.int32) #array of zeros with histogram shape, integers

for file in files:
    print(file)
    df = pd.read_csv(file, usecols=["phase_deg", "q_pC", "d_time_s"])
    df.dropna(inplace=True)

    #add to histogram, ignore xedges yedges
    h, _, _ = np.histogram2d(
        df["phase_deg"],
        df["q_pC"],
        bins=[phase_bins, q_bins],
        #range=[[0, 360], [q_min, q_max]]
    )

    hist += h.astype(np.int32)

plt.imshow(
    hist.T, #fix imshow transposition
    origin="lower", #fix default imshow origin position
    aspect="auto",
    norm=LogNorm(vmin = 1, vmax = hist.max()), #log colours
    extent=[0, 360, q_min, q_max] #set x range, y range
)

plt.xlabel("Phase (deg)")
plt.ylabel("Charge (pC)")
plt.title("PRPD Histogram")
plt.colorbar(label="PD Counts [log scale]")

plt.tight_layout()
plt.show()