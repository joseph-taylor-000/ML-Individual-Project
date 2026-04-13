import pandas as pd
import matplotlib.pyplot as plt
import glob as glob
import numpy as np


#data initialisation
directory_val = 3 

#directory selection
if directory_val == 1:
    directory = r"M:\OneDrive - The University of Manchester\ML_dataset\New datasets_Sample S4.4\0 to 1h\*" #0-1hr
elif directory_val == 2:
    directory = r"M:\OneDrive - The University of Manchester\ML_dataset\New datasets_Sample S4.4\252 to 253 h\*" #252 to 253hr
elif directory_val == 3:
    directory = r"M:\OneDrive - The University of Manchester\ML_dataset\New datasets_Sample S4.4\255 to 256 h\*" #255 to 256hr

files = glob.glob(directory)
#files = files[:10]

#figure set-up
fig1, ax1 = plt.subplots()
ax2 = ax1.twinx()

fig2, ax3 = plt.subplots()
ax4 = ax3.twinx()

fig3, ax5 = plt.subplots()
ax6 = ax5.twinx()

for file in files:
    print(file)

    df = pd.read_csv(file, usecols=["time_s", "q_pC"])
    df.dropna(inplace=True)

#df = df[(df["q_pC"] >= 5) | (df["q_pC"] <= -5)] #optional filters
#df = df[(df["q_pC"] <= 5) & (df["q_pC"] >= -5)]
#df = df[(df["q_pC"] <= 4) & (df["q_pC"] >= 3)]

    df["time_us"] = (df["time_s"] * 1e0).astype(int) #rounds to microsecond resolution of groupings

    density_time = (
        df.groupby("time_us") 
            .agg( #aggregate functions
                counts = ("q_pC", "size"), ##PD counts at time 
                q_pC_sq_total=("q_pC", lambda x: (x**2).sum()), #sum of PD counts squared (for RMS)
                q_pC_sq_total_pos = ("q_pC", lambda x: ((x[x > 0])**2).sum()), #positive sum of squares - sum x where x > 0
                q_pC_sq_total_neg = ("q_pC", lambda x: ((x[x < 0])**2).sum()), #negative sum of squares- sum x where x < 0
                counts_pos = ("q_pC", lambda x: (x > 0).sum()), #positve values count - sum bool where x > 0
                counts_neg = ("q_pC", lambda x: (x < 0).sum()) #negative values count - sum bool where x < 0
            )
    )

    density_time_df = density_time.reset_index() #separate time from index
    density_time_df["q_pC_rms"] = np.sqrt(density_time_df["q_pC_sq_total"]/density_time_df["counts"].where(density_time_df["counts"] > 0))
    density_time_df["q_pC_rms_pos"] = np.sqrt(density_time_df["q_pC_sq_total_pos"]/density_time_df["counts_pos"].where(density_time_df["counts_pos"] > 0))
    density_time_df["q_pC_rms_neg"] = -(np.sqrt(density_time_df["q_pC_sq_total_neg"]/density_time_df["counts_neg"].where(density_time_df["counts_neg"] > 0)))
    density_time_df["time_us"] = density_time_df["time_us"]*1e-0


    #plot 1
    ax1.scatter(
        density_time_df["time_us"],
        density_time_df["counts"],
        c="blue",
        s=10,
        alpha=0.6
    )

    ax2.scatter(
        density_time_df["time_us"],
        density_time_df["q_pC_rms"],
        marker = 'x',
        c='red',
        s=10,
        alpha=0.6
    )

    #plot 2
    ax3.scatter(
            density_time_df["time_us"],
            density_time_df["counts_pos"],
            c="blue",
            s=10,
            alpha=0.6
        )
        
    ax4.scatter(
            density_time_df["time_us"],
            density_time_df["q_pC_rms_pos"],
            marker = 'x',
            c='red',
            s=10,
            alpha=0.6
        )
    #plot 3
    ax5.scatter(
            density_time_df["time_us"],
            density_time_df["counts_neg"],
            c="blue",
            s=10,
            alpha=0.6
        )
        
    ax6.scatter(
            density_time_df["time_us"],
            density_time_df["q_pC_rms_neg"],
            marker = 'x',
            c='red',
            s=10,
            alpha=0.6
        )

#plot 1
ax1.set_title("Time-Discharge Density: All Events")
ax1.set_xlabel("Time (seconds)")
ax1.set_ylabel("Partial Discharge Counts")
ax2.set_ylabel("Discharge Magnitude Root Mean Squared")
fig1.tight_layout()


#plot 2
ax3.set_title("Time-Discharge Density: Positive Events")
ax3.set_xlabel("Time (seconds)")
ax3.set_ylabel("Partial Discharge Counts")
ax4.set_ylabel("Discharge Magnitude Root Mean Squared")
fig2.tight_layout()


#plot 3
ax5.set_title("Time-Discharge Density: Negative Events")
ax5.set_xlabel("Time (seconds)")
ax5.set_ylabel("Partial Discharge Counts")
ax6.set_ylabel("Discharge Magnitude Root Mean Squared")
fig3.tight_layout()


plt.show()

