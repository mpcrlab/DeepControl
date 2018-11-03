# DeepControl

## [LINK TO PUBLIC DATASET](https://drive.google.com/drive/folders/1SjSheeJO09zaGBIkAiLw6ToQiecFdm4i?usp=sharing)

Here's the link to the dataset mentioned in the paper.

### Abstract

The problem of minimizing risk in industrial plant settings is of high interest for research. Long hours in industrial control rooms induce fatigue, drowsiness, and ease of distraction, posing a risk of failure or catastrophe. Considering the critical importance industrial plants have on the modern-day economy, the minimization of risk in such settings should be prioritized. Recently, deep learning has proven successful on a host of applications, including online recommendation systems, online language translation, image recognition, robotics, and medical diagnosis. This research aimed to develop a deep learning control system that learned to match human performance on a simulated task (a 1990's Microsoft DOS racing game called Car & Driver) with only optical input, serving as a preliminary prototype for controlling a power plant from only optical feed of dials and gauges. A supervised learning approach was taken; a convolutional neural network (CNN) was trained on 6 hours of pre-recorded human expert play data to return the optimal keystroke given a still frame image of the task. When evaluated offline on a test dataset of still image frames of the same task, the CNN achieved ~90\% accuracy. To evaluate the CNN online on the task itself, a novel hardware interface consisting of two connected Arduino boards was developed to facilitate CNN-task interaction. When all components were incorporated into a cohesive control system, the CNN achieved near-human performance on the in-game metrics “Average Speed,” “Top Speed,” and “Lap Time.” This demonstrates that this system can achieve human-performance when applied to an actual power plant scenario.


## Brief Overview

A project to create a deep learning control system that learns by an air-gapped optical input stream rather than raw pixels. Applications include all sorts of infrastructure with legacy hardware (flood control, manufacturing plants, power plants).

Specifically, below is the configuration.

![configuration](http://imgur.com/gmTRUSn.jpg)

## Policy Network Procedure
### *Collection*
#### 1. Run `policy_collect.py` to collect data.
This will store corresponding image frames and keypresses at every timestep into .h5 files in a "dataset" folder. It will store it in batches of 500 frames as one .h5 file, and to toggle data collection press the spacebar.

#### 2. `Run deleteblankframes.py`
Since the policy_collect.py script produces extraneous blank frames, run `deleteblankframes.py` to delete them to prepare for policy network training.

#### 3. Adjust and Drag to /dataset/ folder
Drag collected data in the `/sim-datasets/datasetname/fixed/fixed/` to `/dataset/`, renaming it with `dataset_rename.py` if needed.


### *Training*
Run `policy_train.py` to train on data collected in `/dataset/`. 

### *Real-time evaluation*
Run `policy_run.py` to run on the trained neural network and control the simulator in real-time.

## Some Figures/Results

![accuracy](https://github.com/mpcrlab/DeepControl/raw/master/plots/12-1training_accuracy.png)

![loss](https://github.com/mpcrlab/DeepControl/raw/master/plots/12-1training_loss.png)

![screenshot1](https://github.com/mpcrlab/DeepControl/raw/master/opticalscreenshot.png)
