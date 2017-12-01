# DeepControl

## [LINK TO PUBLIC DATASET](https://drive.google.com/drive/folders/1SjSheeJO09zaGBIkAiLw6ToQiecFdm4i?usp=sharing)

Here's the link to the dataset mentioned in the paper.

## Brief Overview

A project to create a deep learning control system that learns by an air-gapped optical input stream rather than raw pixels. Applications include all sorts of infrastructure with legacy hardware (flood control, manufacturing plants, power plants).

Specifically, below is the configuration.

![configuration](http://imgur.com/gmTRUSn.jpg)

![screenshot1](https://github.com/mpcrlab/DeepControl/raw/master/opticalscreenshot.png)

### Abstract

Historically, businesses and governments have hesitated to modernize their legacy systems and infrastructure to digital because of the enormous costs associated with this transition[1], including the overhaul of active and rigorously tested mechanical equipment and systems that have been operating reliably for many decades. The digitization of infrastructure presents clear benefits over the rigid but stable operation of legacy systems, including the ability to remotely control and oversee operation[2], implement predictive machine learning algorithms to anticipate component breakdown[3], or automate and optimize processes[4]. In response, we present an alternative scalable and adaptable deep learning control system paradigm that, if developed further, could be bootstrapped to autonomously control legacy systems, costing under $2,000 in some cases. Specifically, we used supervised learning to train an 8-layer convolutional neural network (CNN) on expert human gameplaying data of a racing simulator game running on a separate dedicated low-power computer. The training input was captured through a webcam, and when trained on a task of minimizing lap time on a designated track, the trained CNN achieved comparable performance when it drove the car. Our study not only corroborates the robustness of CNNs, but also suggests that in the near future, a control system that utilizes CNNs’ ability to map noisy optical input to appropriate actions could bridge the gap between analog human-controlled systems and surrounding digital infrastructure, particularly in industrial settings. Additionally, we are open-sourcing our dataset and code to expedite research and contribute to the democratization of AI at github.com/mpcrlab/DeepControl.

## Policy Network Data Collection
### Steps:
#### 1. Run policy_collect.py to collect data.
This will store corresponding image frames, keypresses, and extracted car speed at every timestep into .h5 files in a "dataset" folder. It will store it in batches of 500 frames as one .h5 file, and to toggle data collection press the spacebar.

#### 2. Run deleteblankframes.py
Since the policy_collect.py script produces extraneous blank frames, run deleteblankframes.py to delete them to prepare for policy network training.

#### 3. Run convertfloat.py
Since policy_collect.py stores in float64 which is very heavy on RAM, use convertfloat.py to automatically convert all images in data files to uint8. This will result in no loss of information.

## Policy Network Training
Run policy_train.py to train on data collected in the "dataset" folder. 

## Policy Network Run (Real-time testing)
Run policy_run.py to run on the trained neural network and control the game real-time.
