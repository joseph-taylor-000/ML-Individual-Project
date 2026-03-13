import pandas as pd
import matplotlib.pyplot as plt
import glob as glob

files = glob.glob("M:/OneDrive - The University of Manchester/ML_dataset/New datasets_Sample S4.4/Noise_0 to 120s/*.csv")
data_list =[]
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()

for file in files:
    df = pd.read_csv(file, usecols=["phase_deg", "q_pC"])
    df.dropna(inplace=True)

#df = df[(df["q_pC"] >= 5) | (df["q_pC"] <= -5)] #optional filters
#df = df[(df["q_pC"] <= 5) & (df["q_pC"] >= -5)]
#df = df[(df["q_pC"] <= 4) & (df["q_pC"] >= 3)]

    df["phase_deg_rounded"] = df["phase_deg"].round().astype(int) #rounding phase to nearest degree

    density_phase = (
        df.groupby("phase_deg_rounded") 
            .agg(
                count=("phase_deg_rounded", "size"), #PD counts at phase
                q_pC_mean=("q_pC", lambda x: x.abs().mean()) #mean magnitude of PD counts
            )
        .reindex(range(360), fill_value=0)
    )

    density_phase_df = density_phase.reset_index()
    density_phase_df.columns = ["phase_deg_rounded", "density", "q_pC"]

    print(density_phase_df)
    #density_phase_df.to_csv('density_phase_df.txt', index=False)

    #plot
    ax1.scatter(
        density_phase_df["phase_deg_rounded"],
        density_phase_df["density"],
        c="blue",
        s=10,
        alpha=0.6
    )
    
    ax2.scatter(
        density_phase_df["phase_deg_rounded"],
        density_phase_df["q_pC"],
        marker = 'x',
        c='red',
        s=10,
        alpha=0.6
    )

ax1.set_xlabel("Phase (deg)")
ax1.set_ylabel("Partial Discharge Counts")
ax2.set_ylabel("Discharge Magnitude Mean")

plt.title("Phase-Discharge Density")
plt.tight_layout()
plt.show()

