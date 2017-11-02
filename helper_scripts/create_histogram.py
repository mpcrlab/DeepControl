# This program takes the log that is outputted by extract_labelhistogram.py and plots a histogram with it

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab

mu, sigma = 100, 15
x = mu + sigma*np.random.randn(10000)
#log = [1, 1, 10, 1, 10, 1, 1, 1, 1, 10, 1, 6, 14, 1, 1, 14, 1, 1, 1, 6, 1, 16, 1, 16, 6, 11, 1, 1, 14, 11, 5, 1, 1, 16, 1, 1, 10, 1, 16, 1, 6, 6, 10, 1, 16, 5, 1, 1, 6, 1, 6, 11, 1, 1, 11, 0, 6, 1, 16, 10, 16, 11, 1, 1, 5, 11, 5, 11, 5, 1, 16, 1, 9, 1, 1, 11, 11, 8, 1, 11, 1, 11, 15, 14, 6, 0, 10, 10, 1, 1, 1, 1, 6, 1, 1, 6, 1, 16, 1, 1, 6, 10, 16, 6, 1]
#log = [11, 1, 16, 1, 5, 1, 11, 8, 1, 7, 10, 1, 9, 1, 1, 11, 10, 1, 1, 1, 1, 6, 6, 14, 11, 1, 10, 1, 6, 8, 1, 6, 1, 11, 1, 6, 1, 11, 10, 1, 10, 10, 6, 11, 6, 14, 14, 1, 1, 1, 1, 9, 10, 8, 1, 1, 1, 1, 1, 1, 1, 14, 1, 1, 17, 7, 1, 1, 1, 1, 16, 1, 6, 1, 1, 1, 1, 6, 1, 1, 10, 9, 10, 1, 1, 15, 1, 16, 6, 14, 16, 1, 6, 6, 6, 1, 5, 10, 10, 1, 11, 1, 6, 11, 6, 1, 1, 10, 10, 1, 11, 1, 10, 10, 15, 10, 1, 14, 1, 1]
#log = [1, 11, 1, 1, 1, 0, 6, 10, 10, 1, 1, 1, 11, 1, 1, 6, 1, 1, 1, 1, 0, 1, 11, 1, 1, 1, 1, 1, 1, 6, 16, 1, 1, 1, 1, 10, 1, 10, 10, 7, 11, 1, 11, 6, 1, 10, 1, 10, 1, 10, 1, 1, 14, 1, 11, 5, 1, 11, 10, 16, 1, 1, 1, 16, 14, 1, 1, 1, 1, 5, 1, 11, 1, 5, 10, 1, 14, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5, 6, 1, 1, 10, 1, 1, 16, 1, 11, 1, 1, 14, 1, 1, 6]
log = [16, 0, 10, 1, 1, 1, 1, 11, 8, 16, 1, 6, 1, 0, 10, 1, 10, 1, 6, 1, 1, 10, 1, 1, 10, 1, 10, 1, 16, 1, 14, 11, 7, 6, 1, 5, 1, 1, 1, 1, 1, 1, 6, 1, 1, 1, 11, 7, 11, 6, 8, 1, 6, 6, 10, 1, 1, 1, 1, 10, 1, 1, 10, 1, 9, 11, 1, 1, 1, 1, 6, 6, 1, 6, 10, 1, 16, 1, 8, 11, 1, 11, 10, 10, 6, 16, 6, 1, 1, 1, 10, 1, 1, 11, 10, 6, 1, 6, 11, 6, 8, 1, 11, 1, 10, 14, 10, 11, 4, 9, 10]
histogram = [i for i in range(20)]

for i in range(len(log)):
    histogram[log[i]] += 1


# the histogram of the data
#n, bins, patches = plt.hist(histogram)

#histogram = np.hstack((histogram.normal(size=1000), histogram.normal(loc=5, scale=2, size=1000)))

plt.bar([i for i in range(20)], height=histogram)
plt.xticks(x, [i for i in range(20)]);


plt.xlabel('One-hot vector index')
plt.ylabel('Number of instances')
plt.title('Histogram of key inputs in Car and Driver')
plt.axis([0, 20, 0, 100])

plt.grid(True)

plt.show()
