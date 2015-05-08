import sklearn as sk
import numpy as nm
import matplotlib.pyplot as plt

# Sean Bryan
# sean.a.bryan@asu.edu
# 9/5/2014
# example taken from the book by Raul Garreta
# http://www.amazon.com/Learning-scikit-learn-Machine-Python/dp/1783281936

# load the faces dataset
# (internet connection required...at least for the first load)
from sklearn.datasets import fetch_olivetti_faces
faces = fetch_olivetti_faces()

# make a fancy plotting function
def print_faces(images, target, top_n):
	# set up the figure size in inches
	fig = plt.figure(figsize=(12.0,12.0))
	fig.subplots_adjust(left=0,right=1,bottom=0,top=1,hspace=0.05,wspace=0.05)
	for i in xrange(top_n):
		# plot the images in a matrix of 20x20
		p = fig.add_subplot(20,20,i+1,xticks=[],yticks=[])
		p.imshow(images[i],cmap=plt.cm.bone)
		# label the image with the target value
		p.text(0,14,str(target[i]))
		p.text(0,60,str(i))

# plot some faces
print_faces(faces.images, faces.target, 400)
import pylab
pylab.ion()
pylab.show()

# import the SVM module
from sklearn.svm import SVC
# this imports the Support Vector Classifier
# by default, the kernel is the slightly fancy rbf kernel
# let's switch to the linear one instead
svc_l = SVC(kernel='linear')

# split into training and testing sets, randomly
from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(faces.data,faces.target, test_size = 0.25, random_state=0)

# do the training on the training set
svc_l.fit(X_train,y_train)
# the results of the training are stored "inside" the object svc_l

# run the classifier on the data set aside for evaluation
y_test_predicted = svc_l.predict(X_test)

# count how often the predicted matches the actual
number_correct = len(nm.where(y_test == y_test_predicted)[0])
# count how many test examples there where
total_number_of_test_samples = len(y_test)
# print out the accuracy rate
print 'Correctly classified ' + str(number_correct) + ' out of ' + str(total_number_of_test_samples) + ' test samples'
