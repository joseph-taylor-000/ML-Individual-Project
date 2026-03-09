import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

directory = r"M:\OneDrive - The University of Manchester\ML_dataset\New datasets_Sample S4.4\0 to 1h\Unit1.1_Qmin0pC_QpC_PhDeg_VkV_0.000_3600.400s_part01.csv"
df = pd.read_csv(directory, usecols=["q_pC", "time_s"])
df.dropna(inplace=True)
#df = df[(df["q_pC"] >= 5) | (df["q_pC"] <= -5)] #optional filters
#df = df[(df["q_pC"] <= 5) & (df["q_pC"] >= -5)]
#df = df[(df["q_pC"] <= 4) & (df["q_pC"] >= 3)]

df["time_us"] = (df["time_s"] * 1e6).astype(int) #rounds to microsecond resolution of groupings

density_time = (
    df["time_us"]
    .value_counts() #number of magnitude values with same time value
    .sort_index() #sort index for ascending time values
    )

density_time_df = density_time.reset_index()
density_time_df.columns = ["time_intervals", "density"]
density_time_df["time_intervals"] = density_time_df["time_intervals"]/1e6


#plot
plt.figure(figsize=(12, 5))
fig, ax1 = plt.subplots()

ax1.scatter(
    density_time_df["time_intervals"],
    density_time_df["density"],
    s=10,
    alpha=0.6
)

ax1.set_yscale("log")

plt.xlabel("Time (s)")
plt.ylabel("Partial Discharge Counts")
plt.title("Time-Discharge Density")
plt.tight_layout()
plt.show()
