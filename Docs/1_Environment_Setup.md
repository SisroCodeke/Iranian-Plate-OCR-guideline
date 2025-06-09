# 1. Environment Setup

This guide details the necessary steps to set up your development environment for the Iranian License Plate Recognition (LPR) project using **Conda** and **Ultralytics**. A properly configured environment is crucial for managing dependencies and ensuring the project runs smoothly.  
*(base on [ultralytics conda quickstart](https://docs.ultralytics.com/guides/conda-quickstart)).*  

we will  
1- install conda
2- create Environment
3- install dependencies for using GPU for [training step](Docs/3_Training/3_Training.md) in the future


## 1-1 Installing Conda/Miniconda

Before you begin, ensure you have **Anaconda** or **Miniconda** installed on your system. If you don't, you will need to download them from  [anaconda](https://www.anaconda.com/download). We will use conda since it will simplify CUDA related processess and reduce the chance of dependency problems

## 1-2 Setting up Conda Environment

after installations Using a dedicated Conda environment helps isolate project dependencies and prevents conflicts. Follow these steps to create and activate a new environment for this project:

1.  **Create a new Conda environment**. Open your terminal or command prompt and run the following command. This creates an environment named `ultralytics-env` with Python 3.12(latest python version supported by ultralytics):

    ```bash
    conda create --name ultralytics-env python=3.12 -y
    ```

2.  **Activate the new environment**. After creation, activate the environment using:

    ```bash
    conda activate ultralytics-env
    ```

    Your terminal prompt should change to indicate that you are now inside the `ultralytics-env` environment.

## 1-3 Installing Ultralytics

With the environment activated, you can now install the Ultralytics package.

1.  **Install Ultralytics**. The recommended way is to install the Ultralytics package from the `conda-forge` channel:

    ```bash
    conda install -c conda-forge ultralytics
    ```

2.  **Installation in a CUDA-Enabled Environment** (Recommended for GPU acceleration). If you have a **CUDA-enabled GPU**, it is best practice to install `ultralytics`, `pytorch`, and `pytorch-cuda` together to resolve any potential conflicts and enable GPU acceleration. This is crucial for intensive tasks like deep learning model training and inference. Use the following command:

    ```bash
    conda install -c pytorch -c nvidia -c conda-forge pytorch torchvision pytorch-cuda=11.8 ultralytics
    ```
    *(Note: The `pytorch-cuda=11.8` version might need adjustment based on your CUDA toolkit version and available PyTorch builds you should change it base on your system).*

## Next Steps

Once you have successfully set up your environment and installed the necessary packages for running Ultralytics. You are now ready to proceed to the next step: **[Dataset Preparation](Docs/2_Dataset_Preparation/2_Dataset_Preparation.md)**.
