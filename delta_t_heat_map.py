import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob 
from matplotlib.colors import LogNorm

#directory selection
directory_val = 2

#directory selection
#Sample 4.4 directories
if directory_val == 1:
    directory = r"M:\OneDrive - The University of Manchester\ML_dataset\New datasets_Sample S4.4\0 to 1h\*" #0-1hr
elif directory_val == 2:
    directory = r"M:\OneDrive - The University of Manchester\ML_dataset\New datasets_Sample S4.4\252 to 253 h\*" #252 to 253hr
elif directory_val == 3:
    directory = r"M:\OneDrive - The University of Manchester\ML_dataset\New datasets_Sample S4.4\255 to 256 h\*" #255 to 256hr

#Sample 4.3 directories
elif directory_val == 4:
    directory = r"M:\OneDrive - The University of Manchester\ML_dataset\New datasets_Sample S4.3\0 to 1h\*" #0 to 1hr
elif directory_val == 5:
    directory = r"M:\OneDrive - The University of Manchester\ML_dataset\New datasets_Sample S4.3\95 to 96h (sample opened for inspection at 96 h)\*" #95 to 96hr
elif directory_val == 6:
    directory = r"M:\OneDrive - The University of Manchester\ML_dataset\New datasets_Sample S4.3\190 to 191h\*" #190 to 191hr
    
#noise directories
elif directory_val == 7:
    directory = r"M:\OneDrive - The University of Manchester\ML_dataset\New datasets_Sample S4.4\Noise_0 to 120s\*" #0 to 120s
elif directory_val == 8:
    directory = r"M:\OneDrive - The University of Manchester\ML_dataset\New datasets_Sample S4.4\Noise_0 to 1000s\*" #0 to 1000s

files = glob.glob(directory)
#files = files[:1]

files.sort(
    key=lambda f: 
    int(f.rsplit('part', 1)[1]
        .replace('.csv', ''))
) 

#find min/max dt
max_charges = []
min_charges =[]

for file in files:
    print(file)
    df = pd.read_csv(file, usecols=["d_time_s"])
    #df = df[(df["q_pC"] <= 1) & (df["q_pC"] >= -1)] #low level filter

    df.dropna(inplace=True)

    max_charges.append(df["d_time_s"].max())
    min_charges.append(df["d_time_s"].min())

dt_min = min(min_charges)
dt_max = max(max_charges)


fig, ax = plt.subplots()

for file in files:
    print(file)
    df = pd.read_csv(file, usecols=["phase_deg", "q_pC", "d_time_s"])
    df.dropna(inplace=True)
    #df = df.sample(10000)

    #positive times only
    df_pos = df[df["d_time_s"] > 0]
    df["d_time_s"] = df["d_time_s"].round(6)

    #plot 
    scatter = ax.scatter(
        df["phase_deg"],
        df["q_pC"],
        c=df["d_time_s"],
        norm=LogNorm(vmin=dt_min, vmax=dt_max),
        cmap="plasma",
        marker = '.',
        s=10,
        alpha=0.6
    )

#plt.yscale("log")
ax.set_xlabel("Phase (deg)")
ax.set_ylabel("PD Magnitude (pC)")
ax.set_title("Phase vs. PD Magnitude: Δt Colour Grading")
fig.colorbar(scatter, ax=ax, label="Δt (s) [log scale]") 

plt.tight_layout()
plt.show()