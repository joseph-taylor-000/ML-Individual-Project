import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LogNorm

#data initialisation
directory = r"M:\OneDrive - The University of Manchester\ML_dataset\New datasets_Sample S4.4\0 to 1h\Unit1.1_Qmin0pC_QpC_PhDeg_VkV_0.000_3600.400s_part01.csv"
df = pd.read_csv(directory, usecols=["phase_deg", "q_pC", "d_time_s", "time_s"])
df.dropna(inplace=True)

# df = df[(df["q_pC"] >= 5) | (df["q_pC"] <= -5)] # optional filtering

#positive times only
df_pos = df[df["d_time_s"] > 0]

#log spaced bins for d_time_s, 150 between min and max values
dt_bins = np.logspace(
    np.log10(df_pos["d_time_s"].min()),
    np.log10(df_pos["d_time_s"].max()),
    150
)

phase_bins = np.linspace(0, 360, 361) #phase bins begin at 0, end at 360, 361 values

#plot
plt.figure()

plt.hist2d(
    df_pos["phase_deg"], #x-axis
    df_pos["d_time_s"], #y-axis
    bins=[phase_bins, dt_bins], #x-bin number, y-bin number
    norm=LogNorm() #colour - represents log10(events in bin)
)

plt.yscale("log")
plt.xlabel("Phase (deg)")
plt.ylabel("Δt (s) [log scale]")
plt.title("Phase vs. Δt Density Histogram")

cbar = plt.colorbar()
cbar.set_label("PD Counts [log scale]")

plt.tight_layout()
plt.show()
