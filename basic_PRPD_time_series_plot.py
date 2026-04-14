import pandas as pd
import matplotlib.pyplot as plt
import glob 
#------------------------
#data initialisation

#directory selection
directory_val = 1
domain = "phase"

#directory selection
if directory_val == 1:
    directory = r"M:\OneDrive - The University of Manchester\ML_dataset\New datasets_Sample S4.4\0 to 1h\*" #0-1hr
elif directory_val == 2:
    directory = r"M:\OneDrive - The University of Manchester\ML_dataset\New datasets_Sample S4.4\252 to 253 h\*" #252 to 253hr
elif directory_val == 3:
    directory = r"M:\OneDrive - The University of Manchester\ML_dataset\New datasets_Sample S4.4\255 to 256 h\*" #255 to 256hr

files = glob.glob(directory)

#domain selection
if domain == "time":
    parameter = "time_s"
    y_label = "Event Time"
    unit = "(seconds)"
elif domain == "phase":
    parameter = "phase_deg"
    y_label = "Phase"
    unit = "(deg)"

fig, ax = plt.subplots()

for file in files:
    print(file)
    df = pd.read_csv(file, usecols=["q_pC", parameter])

    #plot 
    scatter = ax.scatter(
        df[parameter],
        df["q_pC"],
        marker = '.',
        c = 'blue',
        s=1,
        alpha=1
    )

ax.set_xlabel(f"{y_label} {unit}")
ax.set_ylabel("PD Magnitude (pC)")
ax.set_title(f"{y_label} vs. PD Magnitude")


plt.tight_layout()
plt.show()