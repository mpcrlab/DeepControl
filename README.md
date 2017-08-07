# DeepControl

A project to create a deep learning control system that learns by an air-gapped optical input stream rather than raw pixels. Applications include all sorts of infrastructure with legacy hardware (flood control, manufacturing plants, power plants).

Specifically, below is the configuration.

![configuration](http://imgur.com/gmTRUSn.jpg)

First, we use imitation learning to help train an agent to play a DOS game called [Car and Driver](https://www.youtube.com/watch?v=kcSIBXA8nc4) by first collecting data, then training deep CNNs on it.

## Policy Network Data Collection
Run controltrain1.py to collect data. This will store corresponding image frames, keypresses, and extracted car speed at every timestep into .h5 files in a "dataset" folder.

## Policy Network Training (Work in Progress)
Run policy_train.py to train on data collected in the "dataset" folder.
