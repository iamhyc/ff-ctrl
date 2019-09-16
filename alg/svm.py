# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 11:49:33 2019

@author: shuai wang
"""
import time
from alg.SockFeeder import SockFeeder

# print(__doc__)

# Author: Gael Varoquaux <gael dot varoquaux at normalesup dot org>
# License: BSD 3 clause

# Standard scientific Python imports
import matplotlib.pyplot as plt

# Import datasets, classifiers and performance metrics
from sklearn import datasets, svm, metrics

# The digits dataset
digits = datasets.load_digits()

# The data that we are interested in is made of 8x8 images of digits, let's
# have a look at the first 4 images, stored in the `images` attribute of the
# dataset.  If we were working from image files, we could load them using
# matplotlib.pyplot.imread.  Note that each image must have the same size. For these
# images, we know which digit they represent: it is given in the 'target' of
# the dataset.
images_and_labels = list(zip(digits.images, digits.target))
for index, (image, label) in enumerate(images_and_labels[:4]):
    plt.subplot(2, 4, index + 1)
    plt.axis('off')
    plt.imshow(image, cmap=plt.cm.gray_r, interpolation='nearest')
    plt.title('Training: %i' % label)

# To apply a classifier on this data, we need to flatten the image, to
# turn the data in a (samples, feature) matrix:
n_samples = len(digits.images)
data = digits.images.reshape((n_samples, -1))

# Create a classifier: a support vector classifier
classifier = svm.SVC(C=1,gamma=0.001)

###################### Main Section ######################
sf = SockFeeder('svm')
sf.connect()

while True:
    _, results = sf.get(num=1) #blocking, until get $num samples
    #TODO: 把下面的复制过来并且可以work
    pass

size_vec =[50,100,1120,1019,1058,1110,1077,987,1123,1056]
acc=size_vec
for j in range(10):
    train_size =size_vec[j]
    start=50
# We learn the digits on the first half of the digits
    classifier.fit(data[start:train_size+start], digits.target[start:train_size+start])

# Now predict the value of the digit on the second half:
    expected = digits.target[1001:]
    predicted = classifier.predict(data[1001:])
    print(metrics.accuracy_score(expected, predicted))
    print(classifier.dual_coef_.shape) 
# print("Confusion matrix:\n%s" % metrics.confusion_matrix(expected, predicted))

# images_and_predictions = list(zip(digits.images[n_samples // 2:], predicted))
#for index, (image, prediction) in enumerate(images_and_predictions[:4]):
#    plt.subplot(2, 4, index + 5)
#    plt.axis('off')
#    plt.imshow(image, cmap=plt.cm.gray_r, interpolation='nearest')
#    plt.title('Prediction: %i' % prediction)
#
#plt.show()