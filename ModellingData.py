# This class implements a model to train the testing data based on the training data provided
# Its purpose is to provide the predicted binary values (0 or 1) based on the training algorithm implemented
# The predictions for the testing data are provided in the TestingResults.txt as requested on the specification

import pandas
import numpy as np
from sklearn.model_selection import train_test_split, RepeatedStratifiedKFold, cross_val_score
from sklearn import preprocessing
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis


# this method reads the training data
# returns the x and y values
def read_training_data():
    # read the training data using panda.read_csv
    training_data_df = pandas.read_csv('TrainingData.txt', header=None)
    # get training data dataframe by removing last column (binary value)
    training_data = training_data_df.drop(24, axis=1)
    # get the x values of each modeling curve
    x_values = training_data.values.tolist()
    # get binary value (our y values) that indicates normal or abnormal and store in list
    y_values = training_data_df[24].tolist()
    x_values = np.array(x_values)
    y_values = np.array(y_values)
    return x_values, y_values


# read the testing data
test_data_df = pandas.read_csv('TestingData.txt', header=None)
# store testing values
x_classify = test_data_df.values.tolist()

# split the training data using sklearn train_test_split
# train_test_split = splits arrays or matrices into random train and test subsets
x_train, x_test, y_train, y_test = train_test_split(read_training_data()[0], read_training_data()[1], test_size=0.2,
                                                    random_state=0)

# scale data to make it easy for model to learn and understand the problem
# simple way is to use sklearn preprocessing to use MinMaxScaler()
scale_data = preprocessing.MinMaxScaler()
x_train = scale_data.fit_transform(x_train)
x_test = scale_data.fit_transform(x_test)
x_classify = scale_data.fit_transform(x_classify)
x_all = scale_data.fit_transform(read_training_data()[0])

# Fit the LDA model
model = LinearDiscriminantAnalysis()
model.fit(x_train, y_train)
y_pred = model.predict(x_classify)
y_pred = [int(x) for x in y_pred]
# Define method to evaluate model
cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)
# evaluate model
scores = cross_val_score(model, x_all, read_training_data()[1], scoring='accuracy', cv=cv, n_jobs=-1)
print('Mean Accuracy: %.3f (%.3f)' % (np.mean(scores), np.std(scores)))

# Print to file "TestingResults.txt"
predictions_df = pandas.DataFrame({'Prediction': y_pred})
test_data_df = test_data_df.join(predictions_df)
test_data_df.to_csv("TestingResults.txt", header=None, index=None)
