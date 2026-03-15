import pandas as pd
import matplotlib.pyplot as plt
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

fig, ax = plt.subplots()
max_values = []

for file in files:
    print(file)
    df = pd.read_csv(file, usecols=["phase_deg", "q_pC", "d_time_s"])
    df.dropna(inplace=True)

    #positive times only
    df_pos = df[df["d_time_s"] > 0]

    #phase-time bins
    df["d_time_s"] = df["d_time_s"].round(7) #rounds d_time to 7 decimal places (0.1x micro range)
    df["phase_deg_rounded"] = df["phase_deg"].round().astype(int) #rounding phase to nearest degree

    df_grouped = (df.groupby(["phase_deg_rounded", "d_time_s"]) .size()).reset_index(name = "count")

    max_values.append(df_grouped["count"].max())



for file in files:
    print(file)
    df = pd.read_csv(file, usecols=["phase_deg", "q_pC", "d_time_s"])
    df.dropna(inplace=True)

    #positive times only
    df_pos = df[df["d_time_s"] > 0]

    #phase-time bins
    df["d_time_s"] = df["d_time_s"].round(7) #rounds d_time to 7 decimal places (0.1x micro range)
    df["phase_deg_rounded"] = df["phase_deg"].round().astype(int) #rounding phase to nearest degree

    df_grouped = (df.groupby(["phase_deg_rounded", "d_time_s"]) .size()).reset_index(name = "count")
    print(df_grouped)

    #plot 
    scatter = ax.scatter(
        df_grouped["phase_deg_rounded"],
        df_grouped["d_time_s"],
        c=df_grouped["count"],
        norm=LogNorm(vmin=1, vmax=max(max_values)),
        cmap="plasma",
        marker = '.',
        s=10,
        alpha=0.6
    )

plt.yscale("log")
ax.set_xlabel("Phase (deg)")
ax.set_ylabel("Δt (s) [log scale]")
ax.set_title("Phase vs. Δt Density Histogram")
fig.colorbar(scatter, ax=ax, label="PD Counts [log scale]") 

plt.tight_layout()
plt.show()