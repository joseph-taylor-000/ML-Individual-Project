import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob 
from matplotlib.colors import LogNorm

#data initialisation
directory = r"M:\OneDrive - The University of Manchester\ML_dataset\New datasets_Sample S4.4\255 to 256 h\*"
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