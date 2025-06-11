# Iranian-Plate-OCR-guideline
An end-to-end pipeline for Iranian License Plate Recognition (LPR) using the Ultralytics YOLO framework. This repository provides a step-by-step guide covering environment setup, dataset preparation, model training, validation, and inference using iranian license plate images from the IR-LPR dataset.

## Project Overview

This project implements an automatic system to detect and recognise characters from Iranian license plates. Leveraging the power of Ultralytics YOLO, a state-of-the-art object detection model, we build a complete workflow from data handling to model deployment. The guide uses the publicly available [IR-LPR dataset](https://github.com/mut-deep/IR-LPR), which provides a large collection of annotated Iranian car and license plate images, including specific data for character recognition.

## Features

*   Detailed guide for setting up the development environment using Conda.
*   Instructions for utilizing the [IR-LPR dataset](https://github.com/mut-deep/IR-LPR).
*   Steps for training a custom Ultralytics YOLO model for Iranian license plate detection and character recognition.
*   Guidance on model validation and evaluation.
*   Examples for running inference on new images.

## Repository Structure

This repository is structured to provide a clear, step-by-step guide. Each major phase of the pipeline is detailed in its own markdown file.

/
├── README.md                         # Project introduction and overview  
├── docs/                             # Documentation guides  
│   ├── 1_Environment_Setup.md        # Software setup (Conda, Ultralytics)  
│   ├── 2_Dataset_Preparation/        # Dataset-related guides  
│   │   └── Dataset_Preparation.md    # Downloading/preparing IR-LPR dataset  
│   ├── 3_Training/                   # Training guides  
│   │   └── Training.md               # YOLO model training steps  
│   ├── 4_Validation/                 # Validation guides  
│   │   └── Validation.md             # Model validation steps  
│   └── 5_Inference_Example/          # Inference guides  
│      └── Inference_Example.md       # How to run predictions  

*(Note: The numbering (1, 2, 3, 4, 5) follows a logical flow for the guide, addressing your requested steps in a practical order: Environment -> Dataset -> Train -> Validate -> Example. This means step 3 in the guide is 'Training', step 4 is 'Validation', and step 5 is 'Inference Example'.)*

## Getting Started

Follow the numbered markdown files in sequence to set up the project and run the pipeline.

1.  [Environment Setup](Docs/1_Environment_Setup.md)
2.  [Dataset Preparation](2_Dataset_Preparation.md)
3.  [Training](3_Training.md)
4.  [Validation](4_Validation.md)
5.  [Inference Example](5_Inference_Example.md)

## Dataset

This project uses the **IR-LPR: Large Scale of Iranian License Plate Recognition Dataset**. This dataset includes a total of **20,967 car images** with detection annotations for the whole license plate and its characters, and **27,745 license plate images** specifically for character recognition. The data is available for download via Google Drive links provided in the original [mut-deep/IR-LPR GitHub repository](https://github.com/mut-deep/IR-LPR).

Authors of the IR-LPR dataset: Mahdi Rahmani, Melika Sabaghian, Seyyede Mahila Moghadami, Mohammad Mohsen Talaie, Mahdi Naghibi, Mohammad Ali Keyvanrad.

## Licence

This project is covered by the MIT License. The IR-LPR dataset has its own licenses, including GPL-3.0. Please refer to the respective repositories for details.

## Acknowledgements

*   [Ultralytics](https://github.com/ultralytics/ultralytics) for their powerful YOLO framework and clear documentation.
*   The authors of the [IR-LPR dataset](https://github.com/mut-deep/IR-LPR) for providing a valuable resource for this project.
*   The students of Malek Ashtar University of Technology for their help in preparing the IR-LPR dataset.
