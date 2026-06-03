# Malaria AI Detection System
An AI-powered malaria detection and parasite-stage classification system using microscopy blood smear images, image processing, object localization, and deep learning.

This project aims to assist malaria diagnosis by automatically detecting malaria parasites from blood smear microscopy images and classifying parasite stages using computer vision and neural networks.


# Project Goal
The objective of this project is to build an intelligent malaria diagnosis pipeline capable of:
- Detecting malaria parasites from blood smear images
- Localizing infected regions/cells
- Classifying parasite developmental stages
- Handling subtle morphological differences between stages
- Improving detection using image preprocessing techniques
- Addressing class imbalance using mathematically informed loss functions
The system is designed to support researchers, clinicians, and medical AI applications in improving malaria screening efficiency.

# Blood Smear Types Used
This project uses two microscopy blood smear types:

## Thin Smears
Used for:
- Parasite stage classification
- Species/stage morphology analysis

Classes include:
- Ring Stage
- Trophozoite
- Gametocyte
- White Blood Cell
- Artefacts
- Other Stage
Thin smears provide detailed parasite morphology and are ideal for stage-level classification.

## Thick Smears
Used for:
- Parasite detection
- Infection identification
Thick smears concentrate parasites, making them useful for detecting infection presence.

# AI Pipeline
The project follows a multi-stage computer vision pipeline:
- Raw Blood Smear Images
- Dataset Cleaning & Label Validation
- YOLO Bounding Box Localization
- Cell Cropping (ROI Extraction)
- Image Processing: (LAB + CLAHE + Normalization)
- CNN Classification
- Malaria Stage Prediction

# Research Motivation
Malaria diagnosis through microscopy is time-consuming and dependent on expert interpretation.
This project investigates how artificial intelligence can assist malaria detection by combining:
- Image processing
- Deep learning
- Object localization
- Mathematical optimization techniques
to improve detection reliability and efficiency.


# Focused on:
- Medical AI
- NLP
- Computer Vision
- Generative AI
- Research-driven Machine Learning