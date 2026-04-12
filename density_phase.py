import pandas as pd
import matplotlib.pyplot as plt
import glob as glob

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
files = files[:10]

#figure set-up
fig1, ax1 = plt.subplots()
ax2 = ax1.twinx()

fig2, ax3 = plt.subplots()
ax4 = ax3.twinx()

fig3, ax5 = plt.subplots()
ax6 = ax5.twinx()

for file in files:
    df = pd.read_csv(file, usecols=["phase_deg", "q_pC"])
    df.dropna(inplace=True)

#df = df[(df["q_pC"] >= 5) | (df["q_pC"] <= -5)] #optional filters
#df = df[(df["q_pC"] <= 5) & (df["q_pC"] >= -5)]
#df = df[(df["q_pC"] <= 4) & (df["q_pC"] >= 3)]

    df["phase_deg_rounded"] = df["phase_deg"].round().astype(int) #rounding phase to nearest degree

    density_phase = (
        df.groupby("phase_deg_rounded") 
            .agg( #aggregate functions
                counts = ("q_pC", "size"), ##PD counts at phase 
                q_pC_mean=("q_pC", lambda x: x.mean()), #mean magnitude of PD counts
                q_pC_mean_pos = ("q_pC", lambda x: x[x > 0].mean()), #positive mean - mean x where x > 0
                q_pC_mean_neg = ("q_pC", lambda x: (x[x < 0].mean())), #negative mean - mean x where x < 0
                counts_pos = ("q_pC", lambda x: (x > 0).sum()), #positve values count - sum bool where x > 0
                counts_neg = ("q_pC", lambda x: (x < 0).sum()) #negative values count - sum bool where x < 0
            )
        .reindex(range(360))
    )

    density_phase_df = density_phase.reset_index() #separate phase from index

    print(density_phase_df)
    #density_phase_df.to_csv('density_phase_df.txt', index=False)

    #plot 1
    ax1.scatter(
        density_phase_df["phase_deg_rounded"],
        density_phase_df["counts"],
        c="blue",
        s=10,
        alpha=0.6
    )
    
    ax2.scatter(
        density_phase_df["phase_deg_rounded"],
        density_phase_df["q_pC_mean"],
        marker = 'x',
        c='red',
        s=10,
        alpha=0.6
    )

    #plot 2
    ax3.scatter(
            density_phase_df["phase_deg_rounded"],
            density_phase_df["counts_pos"],
            c="blue",
            s=10,
            alpha=0.6
        )
        
    ax4.scatter(
            density_phase_df["phase_deg_rounded"],
            density_phase_df["q_pC_mean_pos"],
            marker = 'x',
            c='red',
            s=10,
            alpha=0.6
        )
    #plot 3
    ax5.scatter(
            density_phase_df["phase_deg_rounded"],
            density_phase_df["counts_neg"],
            c="blue",
            s=10,
            alpha=0.6
        )
        
    ax6.scatter(
            density_phase_df["phase_deg_rounded"],
            density_phase_df["q_pC_mean_neg"],
            marker = 'x',
            c='red',
            s=10,
            alpha=0.6
        )

#plot 1
ax1.set_title("Phase-Discharge Density: All Events")
ax1.set_xlabel("Phase (deg)")
ax1.set_ylabel("Partial Discharge Counts")
ax2.set_ylabel("Discharge Magnitude Mean")
fig1.tight_layout()


#plot 2
ax3.set_title("Phase-Discharge Density: Positive Events")
ax3.set_xlabel("Phase (deg)")
ax3.set_ylabel("Partial Discharge Counts")
ax4.set_ylabel("Discharge Magnitude Mean")
fig2.tight_layout()


#plot 3
ax5.set_title("Phase-Discharge Density: Negative Events")
ax5.set_xlabel("Phase (deg)")
ax5.set_ylabel("Partial Discharge Counts")
ax6.set_ylabel("Discharge Magnitude Mean")
fig3.tight_layout()


plt.show()
