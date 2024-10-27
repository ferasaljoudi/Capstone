<div style="width: 100%;">
    <a href="#"><img src="https://raw.githubusercontent.com/ferasaljoudi/AssetsRepository/main/BrownSVGs/requirementsDocument.svg" alt="Requirements Document" style="width: 100%"></a>
</div>
<br>

1. [Introduction](#introduction)<br>
    1.1 [Document Purpose](#document-purpose)<br>
    1.2 [Project Scope](#project-scope)<br>
    1.3 [Product Value](#product-value)<br>
    1.4 [Intended Audience](#intended-audience)<br>
    1.5 [References](#references)<br>

2. [Overall Description](#overall-description)<br>
    2.1 [Product Perspective](#product-perspective)<br>
    2.2 [User Classes and Characteristics](#user-classes-and-characteristics)<br>
    2.3 [Operating Environment](#operating-environment)<br>
    2.4 [Design and Implementation Constraints](#design-and-implementation-constraints)<br>
    2.5 [Assumptions and Dependencies](#assumptions-and-dependencies)<br>

3. [System Features](#system-features)<br>
    3.1 [Real-Time Eye Closure Detection](#real-time-eye-closure-detection)<br>
        &nbsp;&nbsp;&nbsp;&nbsp;3.1.1 [Description](#description)<br>
        &nbsp;&nbsp;&nbsp;&nbsp;3.1.2 [Functional Requirements](#functional-requirements)<br>
    3.2 [Alert System](#alert-system)<br>
        &nbsp;&nbsp;&nbsp;&nbsp;3.2.1 [Description](#description)<br>
        &nbsp;&nbsp;&nbsp;&nbsp;3.2.2 [Functional Requirements](#functional-requirements)<br>

4. [Data Requirements](#data-requirements)<br>
    4.1 [Model Data](#model-data)<br>
    4.2 [Data Dictionary](#data-dictionary)<br>
    4.3 [Data Integrity](#data-integrity)<br>
        &nbsp;&nbsp;&nbsp;&nbsp;4.3.1 [Training Data](#training-data)<br>
        &nbsp;&nbsp;&nbsp;&nbsp;4.3.2 [Captured Data](#captured-data)<br>

5. [Interface Requirements](#interface-requirements)<br>
    5.1 [User Interfaces](#user-interfaces)<br>
    5.2 [Hardware Interfaces](#hardware-interfaces)<br>
    5.3 [Software Interfaces](#software-interfaces)<br>

6. [Quality Attributes](#quality-attributes)<br>
    6.1 [Usability](#usability)<br>
    6.2 [Performance](#performance)<br>
    6.3 [Safety](#safety)<br>
    6.4 [Reliability](#reliability)<br>

7. [Non-Functional Requirements](#non-functional-requirements)<br>
    7.1 [Scalability](#scalability)<br>
    7.2 [Compatibility](#compatibility)<br>

8. [Glossary](#glossary)<br>

9. [Analysis Models](#analysis-models)<br>


# Introduction

## Document Purpose

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The purpose of this document is to outline the requirements for the development of a IFS DriverAlert system that alerts drivers when it detects eye closure, aiming to reduce accidents caused by drowsy driving. This document will serve as a reference for the project team throughout the design, development, and testing phases, providing a clear understanding of the system's objectives, features, and constraints.

## Project Scope

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The project aims to develop a driver drowsiness detection system that monitors a driver's eye closures and sounds an alert to prevent accidents caused by drowsy driving. The system will use a camera, a machine learning model, a Raspberry Pi 5 and a buzzer/speaker, enabling real-time detection of eye closures without requiring internet connectivity. The project will include the development of a Convolutional Neural Network (CNN) model for eye closure detection, integration of OpenCV for image processing, and implementation of an alert system using a buzzer or speaker.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The final product will be an `affordable`, `standalone`, `offline solution` that can be installed in any vehicle, making it accessible to a wide range of drivers. The project will focus on providing a practical, cost-effective alternative to the drowsiness detection systems currently found in high-end vehicles.

## Product Value

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;This driver drowsiness detection system enhances road safety by providing drivers with an affordable, accessible solution to reduce accidents caused by drowsiness. Unlike similar systems integrated into premium cars, this product is designed to be low-cost, easy to install, and capable of functioning offline, removing dependency on internet connectivity and costly high-end hardware.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The system's affordability and standalone nature make it a viable option for everyday drivers who seek enhanced safety without the need to invest in luxury vehicles. By offering this technology to a broader audience, the project aims to make a meaningful impact in reducing accidents, injuries, and fatalities related to drowsy driving.

## Intended Audience

This document is intended for the following audience:

- <b>Project Team:</b> The team members responsible for designing, developing, and testing the IFS DriverAlert system. This document will serve as a guide for ensuring alignment on project requirements and objectives throughout development.
- <b>Project Team:</b> The course instructor overseeing the project as part of the university curriculum. This document will provide the professor with a clear understanding of the project scope, objectives, and requirements.
- <b>Mentor:</b> The mentor assigned to regularly review project progress and offer support as needed. This document will help the mentor understand the project's direction, monitor adherence to requirements, and provide informed guidance.

## References

- <b>Driver Fatigue Detection Systems:</b>
    - <a href="https://carbuzz.com/car-advice/driver-fatigue-detection-systems-how-does-anti-sleep-tech-work" target="_blank" title="Volvo XC90">Driver Fatigue Detection Systems</a>: Overview of existing driver fatigue detection technologies used in high-end vehicles, explaining their features and functions.
    - <a href="https://www.tesla.com/ownersmanual/model3/en_eu/GUID-65BF21B8-50C5-4FA5-86A4-DA363DCD0484.html" target="_blank" title="Tesla">Tesla Model 3 Owner's Manual</a>: Details on Tesla's driver monitoring system, including its role in improving driver safety through fatigue detection.
- <b>Drowsiness Detection Datasets:</b>
    - <a href="https://www.kaggle.com/datasets/dheerajperumandla/drowsiness-dataset" target="_blank" title="Drowsiness_dataset">Drowsiness Dataset</a>: Contains images for open/closed eye states and yawning detection.
    - <a href="https://www.kaggle.com/datasets/prasadvpatil/mrl-dataset" target="_blank" title="MRL Eye Dataset">Drowsiness Detection Dataset</a>: Provides images of open and closed eyes to aid in eye closure detection modeling.

# Overall Description

`In progress...`

# System Features

`In progress...`

# Data Requirements

## Model Data

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;We are utilizing the _<a href="https://www.kaggle.com/datasets/prasadvpatil/mrl-dataset" target="_blank" title="MRL Eye Dataset">MRL Eye Dataset</a>_ which provides images of open and closed eyes. The decision to focus exclusively on the eye region is based on the following reasons:

- <b>Simpler and Faster:</b> Focusing on the eyes reduces the amount of data the model needs to process, enabling quicker and more efficient detection, especially on lower-power devices like the Raspberry Pi.
- <b>Targeted Detection:</b> Since drowsiness is primarily indicated by eye closure, using an eye-only dataset provides a focused approach that aligns well with the project's objective.
- <b>Less Data Required:</b> Training on eye images requires less labeled samples, which can reduce both the time and resources needed for model training.

## Data Dictionary

`In progress...`

## Data Integrity

### Training Data

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The MRL Eye Dataset is licensed under a public domain dedication, allowing free usage, modification, distribution, and performance without permission. This permissive license ensures that our usage of the dataset adheres to legal and ethical standards, supporting the integrity of our project.

### Captured Data

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;For the operational system, all captured images are processed in real-time for drowsiness detection. No images are stored or saved, ensuring user privacy and minimizing data retention concerns. This approach maintains data integrity by processing only the necessary visual data and disposing of it immediately after use.

# Interface Requirements

`In progress...`

# Quality Attributes

`In progress...`

# Non-Functional Requirements

`In progress...`

# Glossary

`In progress...`

# Analysis Models

`In progress...`
