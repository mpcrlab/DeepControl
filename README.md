# DeepControl

A project to create a deep learning control system that learns by an air-gapped optical input stream rather than raw pixels. Applications include all sorts of infrastructure with legacy hardware (flood control, manufacturing plants, power plants).

Specifically, below is the configuration.

![configuration](http://imgur.com/gmTRUSn.jpg)

First, an agent trains on human gameplaying data to achieve comparable performance through imitation learning. Next, we use the trained policy network as baseline performance, and implement q-learning to further augment its performance. Our implementation plays [Car and Driver](https://www.youtube.com/watch?v=kcSIBXA8nc4), which is a 1990's DOS racing game.

## Policy Network Data Collection
Run controltrain1.py to collect data. This will store corresponding image frames, keypresses, and extracted car speed at every timestep into .h5 files in a "dataset" folder.

## Policy Network Training (Work in Progress)
Run policy_train.py to train on data collected in the "dataset" folder.
