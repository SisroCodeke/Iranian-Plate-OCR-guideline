# 1. Environment Setup

This guide details the necessary steps to set up your development environment for the Iranian License Plate Recognition (LPR) project using **Conda** and **Ultralytics**. A properly configured environment is crucial for managing dependencies and ensuring the project runs smoothly.

## Prerequisites

Before you begin, ensure you have **Anaconda** or **Miniconda** installed on your system. If you don't, you will need to download and install one of them from  [anaconda](https://www.anaconda.com/download). we use conda since it will simplify CUDA related processess and reduce the chance of dependency problems

## Setting up a Conda Environment

Using a dedicated Conda environment helps isolate project dependencies and prevents conflicts. Follow these steps to create and activate a new environment for this project:

1.  **Create a new Conda environment**. Open your terminal or command prompt and run the following command. This creates an environment named `ultralytics-env` with Python 3.12(latest python version supported by ultralytics):

    ```bash
    conda create --name ultralytics-env python=3.12 -y
    ```

2.  **Activate the new environment**. After creation, activate the environment using:

    ```bash
    conda activate ultralytics-env
    ```

    Your terminal prompt should change to indicate that you are now inside the `ultralytics-env` environment.

## Installing Ultralytics

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

## Speeding Up Installation (Optional)

To potentially **speed up the package installation process** in Conda, you can use `libmamba`, a fast and dependency-aware alternative solver.

1.  **Install `conda-libmamba-solver`**. This package provides the libmamba solver. If your Conda version is 4.11 or above, this step can likely be skipped as `libmamba` might be included by default.

    ```bash
    conda install conda-libmamba-solver
    ```

2.  **Configure Conda to use `libmamba`**. Set `libmamba` as the default solver:

    ```bash
    conda config --set solver libmamba
    ```

This configuration should result in faster package installations.

## Using Ultralytics Docker Image (Alternative)

As an alternative to setting up the environment manually, Ultralytics offers **Docker images with a Conda environment included**. Using Docker ensures a consistent and reproducible environment.

You can pull and run the latest Ultralytics image with the Conda environment using:

```bash
sudo docker pull ultralytics/ultralytics:latest-conda
sudo docker run -it --ipc=host --gpus all ultralytics/ultralytics:latest-conda # Example with GPU support
```

This approach is ideal for deployment or complex workflows without manual configuration.

## Next Steps

You have successfully set up your environment and installed the necessary packages for running Ultralytics. You are now ready to proceed to the next step: **Dataset Preparation**.
