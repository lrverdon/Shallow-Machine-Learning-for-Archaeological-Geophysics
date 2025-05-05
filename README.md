# Shallow Machine Learning for Archaeological Geophysics
Code for the shallow machine learning based semantic segmentation of geophysical data from archaeological contexts, implemented as a Jupyter Notebook. This code accompanies the paper: Verdonck, L., Dabas, M. and Bui, M. 2025. Interactive, shallow machine-learning based semantic segmentation of 2D and 3D geophysical data from archaeological sites.<br/> The installation and use have been tested on Windows 10 and Linux (Ubuntu 18.04) operating systems.
## Installation
To run the code on your computer, download a package manager such as Conda or Mamba. Whereas installing packages using Conda can be slow or fail because it is unable to resolve dependencies, Mamba is often faster and better at resolving dependencies. The instructions below are based on the use of Mamba, but you can replace ‘mamba’ with ‘conda’ if you are using Conda on your computer.  

**Windows**
1. Download this Github repository as a zip file using the ‘Code’ button at the top of this page and then ‘Download ZIP’. Save the file on your computer and extract it.
2. Install Mamba using the Miniforge distribution. From [https://github.com/conda-forge/miniforge](https://github.com/conda-forge/miniforge?tab=readme-ov-file#install), download the Windows installer and follow the instructions.
3. Open the Miniforge Prompt installed in the Windows Start menu. To create the new environment (step 4), the current environment (enclosed in parentheses) should be 'base'. If the current environment is not 'base', type
   ```
   mamba activate base
   ```
5. In the Miniforge Prompt, change to the directory where you extracted the zip file (this directory includes the `environment.yml` file). Type the following and press Enter:

   ```
   mamba env create -f environment.yml
   ```
   An environment is created, in which Python, napari and all other packages necessary to run the Jupyter notebook are installed. This environment is called ‘my_environment’. If you would like another name for the environment, first change the name in the first line of the `environment.yml` file. To activate the environment, type:
   ```
   mamba activate my_environment
   ```
   (assuming that the created environment is called ‘my_environment’). Then type:
   ```
   jupyter notebook
   ```   
   An internet browser will open, from which you can select the Jupyter notebook `ML_for_Arch_Geophys.ipynb`. 
6. Follow the instructions in the notebook.

**Ubuntu**   
1. Download this Github repository as a zip file using the ‘Code’ button at the top of this page and then ‘Download ZIP’. Save the file on your computer and extract it.
2. Go to [https://github.com/conda-forge/miniforge](https://github.com/conda-forge/miniforge?tab=readme-ov-file#unix-like-platforms-macos-linux--wsl). Under ‘Install – Unix-like platforms (macOS, Linux, & WSL)’, the commands are given to install Mamba. In a regular Ubuntu terminal, type:
    ```
    wget -O Miniforge3.sh "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
    bash Miniforge3.sh -b -p "${HOME}/conda"
    source "${HOME}/conda/etc/profile.d/conda.sh"
    source "${HOME}/conda/etc/profile.d/mamba.sh"
    ```
3. Change to the directory where you extracted the zip file. Type the following and press Enter:
   ```
   mamba env create -f environment.yml
   ```
   An environment is created, in which Python, napari and all other packages necessary to run the Jupyter notebook are installed. This environment is called ‘my_environment’. If you would like another name for the environment, first change the name in the first line of the `environment.yml` file. In order to be able to activate the environment, you may be asked to run the following, then close and re-open the terminal:
   ```
   mamba init
   ```
   To activate the environment, type:
   ```
   mamba activate my_environment
   ```
   (assuming that the created environment is called ‘my_environment’). Then type:
   ```
   jupyter notebook
   ```
   An internet browser will open, from which you can select the Jupyter notebook `ML_for_Arch_Geophys.ipynb`. 
4. Follow the instructions in the notebook.
