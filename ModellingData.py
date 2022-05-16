# This class implements a model to train the testing data based on the training data provided
# Its purpose is to provide the predicted binary values (0 or 1) based on the training algorithm implemented
# The predictions for the testing data are provided in the TestingResults.txt as requested on the specification

import pandas

#read the training data using panda.read_csv
trainingData = pandas.read_csv('TrainingData.txt', header=None)

#print(trainingData)

# get binary value that indicates normal or abnormal and store in list
binary_values = trainingData[24].tolist()

# get training data by removing last column (binary value)
trainingData = trainingData.drop(24, axis=1)
# get the x values of each modeling curve
x_training = trainingData.values.tolist()
