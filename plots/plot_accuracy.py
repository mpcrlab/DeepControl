import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy.signal as sign

data = pd.read_json('run-train12-1-withstraightrecovery3Alex1-tag-Accuracy_.json')

yhat = sign.savgol_filter(data[2], 15, 3)
for index, num in enumerate(yhat):
    yhat[index] *= 100

plt.plot(data[1],yhat, color='black', linewidth=0.5)
plt.title("Classification accuracy of CNN throughout the training process")
plt.ylabel("Accuracy (%)")
plt.xlabel("Training epochs")
plt.show()
