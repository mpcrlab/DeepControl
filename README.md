# DeepControl

A project to create a deep learning control system that learns by an air-gapped optical input stream rather than raw pixels. Applications include all sorts of infrastructure with legacy hardware (flood control, manufacturing plants, power plants).

Specifically, below is the configuration.

![configuration](http://imgur.com/gmTRUSn.jpg)

![screenshot1](https://github.com/mpcrlab/DeepControl/raw/master/opticalscreenshot.png)

First, an agent trains on human gameplaying data to achieve comparable performance through imitation learning. Our implementation plays [Car and Driver](https://www.youtube.com/watch?v=kcSIBXA8nc4), which is a 1990's DOS racing game.

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
