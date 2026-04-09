import pandas as pd
import matplotlib.pyplot as plt
import glob 
import numpy as np
import torch 
import torch.nn as nn 
import torch.optim as optim

class Autoencoder(nn.Module):
    def __init__(self, input_size):
        super().__init__()
        self.input_size = input_size 
        
        self.encoder = nn.Sequential(
            #latent space
            nn.Linear(self.input_size, 256),
            nn.ReLU(),
            nn.Linear(256, 64),
            nn.ReLU(),
            nn.Linear(64, 16)
        )

        self.decoder = nn.Sequential(
            nn.Linear(16, 64),
            nn.ReLU(),
            nn.Linear(64, 256),
            nn.ReLU(),
            nn.Linear(256, self.input_size),
            nn.Sigmoid()
        )

    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded
    


def generate_hist(data, phase_bins, q_bins, q_min, q_max):
    phase_deg = data[:, 1]
    q_pC = data[:, 0]

    h, _, _ = np.histogram2d( #ignore xedges, yedges
        phase_deg, 
        q_pC,
        bins=[phase_bins, q_bins],
        range=[[0, 360], [q_min, q_max]]
    )

    return h

#--------------------------------------------------------------------------------------------------------------------------------
#data initialisation

directory_val = 3 
use_noise_data = False

#directory selection
if directory_val == 1:
    directory = r"M:\OneDrive - The University of Manchester\ML_dataset\New datasets_Sample S4.4\0 to 1h\*" #0-1hr
elif directory_val == 2:
    directory = r"M:\OneDrive - The University of Manchester\ML_dataset\New datasets_Sample S4.4\252 to 253 h\*" #252 to 253hr
elif directory_val == 3:
    directory = r"M:\OneDrive - The University of Manchester\ML_dataset\New datasets_Sample S4.4\255 to 256 h\*" #255 to 256hr
if use_noise_data == True:
    noise_dir = r"M:\OneDrive - The University of Manchester\ML_dataset\New datasets_Sample S4.4\Noise_0 to 1000s\*" #noise data
else:
    noise_dir = ''

#file loading
files = glob.glob(directory)
files = files[:1]
files.sort(
    key=lambda f: 
    int(f.rsplit('part', 1)[1]
        .replace('.csv', ''))
) 

max_charges = []
min_charges = []
all_samples = []

#max / min charges 
for file in files:
    print(file)
    df = pd.read_csv(file, usecols=["phase_deg", "q_pC"])

    #filters
    #df = df[(df["q_pC"] <= 1) & (df["q_pC"] >= -1)] #low level filter

    #df = df[(df["q_pC"] >= 1) | (df["q_pC"] <= -1)] #high level filter
    #df = df[(df["q_pC"] <= 20) & (df["q_pC"] >= -20)] #remove significant anomalies to improve bin accuracy while preserving input size, according to full data histograms

    df.dropna(inplace=True)
    min_charges.append(df["q_pC"].min())
    max_charges.append(df["q_pC"].max())
     
q_min = min(min_charges)
q_max = max(max_charges)    

#bin edges - alter when optimal bins are found
phase_bins_count = 36 #361
q_bins_count = 20 #200

phase_bins = np.linspace(0, 360, phase_bins_count)  
q_bins = np.linspace(min(min_charges), max(max_charges), q_bins_count) #linear bins
#q_bins = np.logspace(np.log10(q_min), np.log10(q_max), 20) #LOG bins


#generate histograms in chunks
for file in files:
    print(file)
    df = pd.read_csv(file, usecols=["phase_deg", "q_pC"])

    #filters - high level
    df = df[(df["q_pC"] >= 1) | (df["q_pC"] <= -1)] #high level filter
    df = df[(df["q_pC"] <= 20) & (df["q_pC"] >= -20)] #remove significant anomalies to improve bin accuracy while preserving input size, according to full data histograms

    df.dropna(inplace=True)
    data = df.to_numpy()
    
    #generate histograms using 10000 rows
    for i in range(0, len(data), 10000):
        chunk = data[i:i+10000]

        h = generate_hist(chunk, phase_bins, q_bins, q_min, q_max)
        
        '''plt.imshow(h.T,  #sanity check
                   aspect='auto', 
                   origin='lower', 
                   extent=[0, 360, q_min, q_max])
        plt.colorbar()
        plt.show()'''

        h = h.flatten() #1 dim rep
        all_samples.append(h)

#create tensor for all samples
X_train = torch.tensor(all_samples, dtype=torch.float32) #convert all_samples to single tensor
X_train = X_train.to('cuda') #enable GPU processing
X_train = X_train / X_train.max() #min-max normalisation ---this may be wrong for non-absolute values

#define data loader to batch training
data_loader = torch.utils.data.DataLoader(
    dataset = torch.utils.data.TensorDataset(X_train),
    batch_size = 64,
    shuffle = True
)

#---------------------------------------------------------------------------------------------------------------------
#initialize autoencoder
model = Autoencoder(X_train.shape[1]) #histogram size = 361*200
model = model.to('cuda') #enable GPU processing
criterion = nn.MSELoss() #Mean Squared Error loss function
optimiser = optim.Adam(model.parameters(),
                             lr = 1e-3, #learning rate
                             weight_decay = 1e-5)

#training
epochs = 50 #alter for min loss
outputs = []

for epoch in range(epochs):
    for batch in data_loader:
        #print(batch)
        data = batch[0] #relevent column only from tensordataset touple (input data, no label)
        data = data.to('cuda')
        recon = model(data)
        loss = criterion(recon, data)

        optimiser.zero_grad() #reset optimiser gradient to zero to avoid accumulation
        loss.backward() #backpropagation through network to minimise loss
        optimiser.step() #updates weight values accordingly

    print(f"Epoch: {epoch+1}, Loss: {loss.item():.6f}")
    outputs.append((epoch, data, recon))

#testing
all_samples = [] #re-purpose all samples

#create test data tensor
if use_noise_data == True: 
    files = glob.glob(noise_dir)
    files = files[:1]

for file in files:
    print(file)
    df = pd.read_csv(file, usecols=["phase_deg", "q_pC"])

    #filters
    df = df[(df["q_pC"] <= 0.6) & (df["q_pC"] >= -0.6)] #low level filter

    df.dropna(inplace=True)
    data = df.to_numpy()
    
    for i in range(0, len(data), 10000):
        chunk = data[i:i+10000]

        h = generate_hist(chunk, phase_bins, q_bins, q_min, q_max)
        h = h.flatten()

        all_samples.append(h)

#create tensor for all samples
X_test = torch.tensor(all_samples, dtype=torch.float32) #convert all_samples to single tensor
X_test = X_test.to('cuda') #enable GPU processing
X_test = X_test / X_test.max() #min-max normalisation ---this may be wrong for non-absolute values

hist_shape = (phase_bins_count-1, q_bins_count-1) #bin sizes - 1  

#training data reconstructions
with torch.no_grad(): #prevent weight training
    recon_train = model(X_train)
    train_errors = torch.mean((X_train - recon_train)**2, dim=1) #mean square error for single sample (feature average, dim=1)
    train_errors = train_errors.cpu().numpy() #move to program host memory as numpy array
    print(train_errors)

    #recreate histograms from flattened tensors
    original = X_train[0].cpu().numpy().reshape(hist_shape) #select first item in training data tensor, move to host memory as numpy array, reshape to original histogram dimensions
    reconstructed = recon_train[0].cpu().numpy().reshape(hist_shape) #same for reconstructed

    plt.figure(figsize=(10,4))

    #original
    plt.subplot(1,2,1) #plot grid layout: 1 row, 2 graphs, 1st graph
    plt.title("Original Training Data")
    plt.imshow(original.T,
               aspect='auto',
               origin='lower',
               extent=[0, 360, q_min, q_max])
    plt.colorbar()

    #reconstructed
    plt.subplot(1,2,2) #2nd graph
    plt.title("Reconstructed Test Data")
    plt.imshow(reconstructed.T,
               aspect='auto',
               origin='lower',
               extent=[0, 360, q_min, q_max])
    plt.colorbar()

    plt.tight_layout()
    plt.show()

#test data reconstructions
with torch.no_grad(): #prevent weight training
    recon_test = model(X_test)
    test_errors = torch.mean((X_test - recon_test)**2, dim=1) #mean square error for single sample (feature average, dim=1)
    test_errors = test_errors.cpu().numpy() #move to program host memory as numpy array
    print(test_errors)

    #recreate histograms from flattened tensors
    original = X_test[0].cpu().numpy().reshape(hist_shape) #select first item in training data tensor, move to host memory as numpy array, reshape to original histogram dimensions
    reconstructed = recon_test[0].cpu().numpy().reshape(hist_shape)

    plt.figure(figsize=(10,4))

    #original
    plt.subplot(1,2,1) #plot grid layout: 1 row, 2 graphs, 1st graph
    plt.title("Original Test Data")
    plt.imshow(original.T, 
               aspect='auto',
               origin='lower', 
               extent=[0, 360, q_min, q_max])
    plt.colorbar()

    #reconstructed
    plt.subplot(1,2,2) #2nd graph
    plt.title("Reconstructed Test Data")
    plt.imshow(reconstructed.T,
               aspect='auto',
               origin='lower',
               extent=[0, 360, q_min, q_max])
    plt.colorbar()

    plt.tight_layout()
    plt.show()

