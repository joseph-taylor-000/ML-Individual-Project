<img src="images/3.14_python.png" width="100" alt="Autoencoder network diagram"><h1 align="center">ML Assisted Partial Discharge Analysis</h1>

<p align="center">
  <img src="images/Autoencoder network diagram.drawio.png" width="600" alt="Autoencoder network diagram">
</p>

This code repository contains the library installation instructions, source code and alogrithmic explanations related to the author's 'Advancing the Fundamental Understanding of Electrical Tree Initiation Mechanisms using ML Assisted Data Analysis' dissertation project.
Each branch corresponds to a specific area of investigation as intuitive, these include: Autoencoder, Density, Gaussian-Mixture-Modelling, HDBSCAN, Image-Processing, K-means. Within each of these, a separate README file is available with a description of the corresponding program e.g. README_HDBSCAN.
The contents of these README file have been collated in this complete repository README, complete with flowcharts for each program.
<h2> Required Libraries: </h2>
Default Python Libraries:
These libraries come pre-installed with python 3.14 and do not require additional installation.
<ul>
  <li>Glob</li>
  <li>OS</li>
  <li>Time</li>
</ul>
Additional Python Libraries:
These libraries DO NOT come pre-installed with python 3.14 and require additional installation. Instructions for the installation of each library are provided.
<ul>
  <li><a href = https://pandas.pydata.org/docs/getting_started/install.html>PANDAS</a></li>
  <li><a href = https://numpy.org/doc/stable/user/absolute_beginners.html>NumPy</a></li>
  <li><a href = https://matplotlib.org/stable/users/explain/quick_start.html>Matplotlib</a></li>
  <li><a href = https://pytorch.org/>Pytorch</a></li>
  <li><a href = https://pypi.org/project/river/>River</a> - River library is supported up to Python version 3.12.0 and requires prerequisite installations of both Cython and Rust. 
This is because some of the machine learning algorithms available in river require high speed loops or strict memory management.
By implementing these features using Cython or Rust, python interpreter overhead is lost and this speed can be achieved.
</li>
</ul>
