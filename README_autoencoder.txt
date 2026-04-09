Required libraries:
matplotlib.pyplot: graphical plotting library for python.
pandas: data processing library for python.
numpy: math library for python.
glob: file directory library for python.
torch: Pytorch Library - Advanced ML library for python
---------------------------------
#Autoencoder - non-linear
This program uses Pytorch to create an autoencoder network. 
This is a type of neural network used to deconstruct and reconstruct a given input. 
In the class definition, the process can be described algorithmically:

Important methods:
>>nn.Linear(input_data_size, output_data_size) - applies a linear transformation to data, transforming input to output size
>>nn.ReLU() - applies rectified linear units activation function:

        3|     /      ReLU: max(0, x) >>> returns x if greater than 0
         |    /       This works well for activation as negitive values are ignored,
        2|   /        positive values are represented linearly.
         |  /
        1| /
_________|/_____
-3 -2 -1 0 1 2 3 

#encoder function - encodes data to reduced representation
encoder:  Linear transform --> ReLU Activation --> Linear transform --> ReLU Activation --> 
          Linear transform --> ReLU Activation --> Linear transform (Decreasing input size from initial to 16)

#decoder function - decodes encoded data to recreate input data
decoder:  Linear transform --> ReLU Activation --> Linear transform --> ReLU Activation --> 
          Linear transform --> Sigmoid Activation (Increasing input size from 16 to initial)

#forward function - forward pass through autoencoder network
forward: input --> encoder --> code --> decoder --> output
-------------------------------
#histogram generator function
creates numpy histogram, will be implemented to create PRPD histogram dataset
-------------------------------
#data initialisation
>>directory selection (different time ranges)
>>file sorting - numerical
>>determine max and min charge values accross all files for histogram ranges
>>define linearly spaced bins - phase between 0-360, charge between min-max values
>>create histograms using high-level PD data. Use 10,000 rows per histogram then move to next 10,000
>>flatten histograms to 1 dimensional representation and convert to Tensor for non-linear autoencoder
>>enable GPU processing to decrease training time
>>apply min-max normalisation to avoid phase-magnitude skew, prepare autoencoder for future normalised ranges
>>create data loader to batch training
-------------------------------
#autoencoder training
>>instantiate autoencoder object with training data histogram size as input size
>>criterion - function to minimise , set as mean square error loss function: 
(1/N)Σ{lower: i=0; upper: N}|Y_i - Y{Pk}_i| - will be used to determine loss at each epoch, where  N = epochs, Y_i = input, Y{Pk}_i = reconstructed
>>optimiser - Adam optimiser used to train model, learning rate set to 1e-3 as common, weight decay set to 1e-5 as common

>>epochs = 50 i.e. 50 training cycles
In each epoch:
>>load batch into autoencoder
>>autoencoder calls forward() method --> puts data through network
>>calculate loss using criterion (MSE loss)
optimisation steps:
	>>reset gradient to avoid accumulation
	>>calculate ideal weight values for network using backpropagation (calculate gradients)
	>>update weight values according to Adam optimiser 
	(weight = weight - learning_rate * gradient, where gradient is d(loss)/d(weight) and learning rate is constant)
------------------------------------
#data testing
>>create histogram set for test data
>>convert set to tensor, min-max normalise

#data reconstruction comparisons
Compare original input data to autoencoder reconstruction graphically to determine effectiveness of network's relvant feature preservation
For both training data (complete recreation) and test data (unknown recreation):
>>disable weight training for test period
>>create reconstruction using trained model and input data
>>determine error using mean square difference of input-reconstruction in single dimension (per row)

>>create dataset for histogram representation using input data first element (first sample)
>>create dataset for histogram representation using reconstruction data first element (first sample)

>>create plots for original and reconstructed:
plt.subplot(1,2,1) #plot grid layout: 1 row, 2 graphs, 1st graph
    plt.title("xxx Data") 
    plt.imshow(original.T, #fix imshow default transposition
               aspect='auto',
               origin='lower', #fix imshow default origin
               extent=[0, 360, q_min, q_max]) #set graph limits 0-360 for phase, min-max for charge
    plt.colorbar()



 


