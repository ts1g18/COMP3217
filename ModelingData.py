# This class implements a model to train the testing data based on the training data provided
# Its purpose is to provide the predicted binary values (0 or 1) based on the training algorithm implemented
# The predictions for the testing data are provided in the TestingResults.txt as requested on the specification


import pandas
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

#read the training data using panda.read_csv
trainingData = pandas.read_csv('TrainingData.txt', header=None)
# get the binary value that indicates if normal or abnormal and store in list
y_training = trainingData[24].tolist()
# get the values for each hour for each modeling curve and store them in a list
trainingData = trainingData.drop(24, axis=1)
x_training = trainingData.values.tolist()

#Storing full training data before splitting
x_training = np.array(x_training)
y_training = np.array(y_training)
x_train_all = x_training
y_train_all = y_training

#Reading testing data and add the hourly predicted prices for each curve to a list of lists
testingData = pandas.read_csv('TestingData.txt', header=None)
x_testing_values = testingData.values.tolist()


#Splitting training data for testing algorithm
x_train, x_test, y_train, y_test = train_test_split(x_training, y_training, test_size=0.2, random_state=0)

# Scaling between 0 and 1 - normalising
scaler = MinMaxScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)
x_testing_values = scaler.transform(x_testing_values)
x_train_all = scaler.transform(x_train_all)

# Linear Discriminant Analysis
lda = LinearDiscriminantAnalysis()
lda.fit(x_train, y_train)
y_pred = lda.predict(x_testing_values)
y_pred = [int(x) for x in y_pred]

#Printing results to output file
predictedData = pandas.DataFrame({'Prediction': y_pred})
testingData = testingData.join(predictedData)
testingData.to_csv("TestingResults.txt", header=None, index=None)
