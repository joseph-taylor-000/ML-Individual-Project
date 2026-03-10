import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LogNorm

#data initialisation
directory = r"M:\OneDrive - The University of Manchester\ML_dataset\New datasets_Sample S4.4\0 to 1h\Unit1.1_Qmin0pC_QpC_PhDeg_VkV_0.000_3600.400s_part01.csv"
df = pd.read_csv(directory, usecols=["phase_deg", "q_pC", "d_time_s", "time_s"])
df.dropna(inplace=True)

#positive times only
df_pos = df[df["d_time_s"] > 0]
df["d_time_s"] = df["d_time_s"].round(6)

#plot 
plt.scatter(
    df["phase_deg"],
    df["q_pC"],
    c=df["d_time_s"],
    norm=LogNorm(vmin=df["d_time_s"].min(), vmax=df["d_time_s"].max()),
    cmap="plasma",
    marker = '.',
    s=10,
    alpha=0.6
)

#plt.yscale("log")
plt.xlabel("Phase (deg)")
plt.ylabel("PD Magnitude (pC)")
plt.title("Phase vs. PD Magnitude: Δt Colour Grading")

cbar = plt.colorbar()
cbar.set_label("Δt (s) [log scale]")

plt.tight_layout()
plt.show()