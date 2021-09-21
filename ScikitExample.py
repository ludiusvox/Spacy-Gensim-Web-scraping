# AIA SciKitExample.py
# @copyright: Collin Lynch
#
# The Scikit learn package is a basic machine learning package
# that provides wrappers for standard ML tools.  We will introduce
# it briefly in this workshop and then return to the package in
# the next workshop for analysis.
#
# Scikit-learn builds heavily on the numpy and scipy packages
# particularly in its use of modules.  To show how it works we
# will draw on a basic ML example for function regression.
#
# The code below with comments is based on an example by
# Jaques Grobler and is licensed under BSD 3 clause


# For this code we will be using the matplotlib, numpy
# and scikit learn libraries.  

import sklearn, sklearn.datasets, sklearn.linear_model
import numpy
import matplotlib.pyplot as plt


# Scikit-learn like the NLTK and some others comes with preexisting
# datasets that we can use for execution.  In this case we will
# load a simple numeric dataset that represents the relationship
# between 10 baseline variables and the chance of someone having
# diabetes.
#
# This call returns two numpy arrays, one with the independent or
# predictive variables (Independent) and one with the dependent or
# output variable (DependentVar)
# https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_diabetes.html
IndependentVars, DependentVar = sklearn.datasets.load_diabetes(return_X_y=True)
print(IndependentVars)
print(DependentVar)


# Here we will illustrate with a single feature.  You are encouraged
# to try each of the features one at a time to see which is most
# predictive or turns out different results.  What we are doing in
# this code is taking the existing feature
#
# Try changing this value to explore different input variables.
SingleIndependentVar = IndependentVars[:, numpy.newaxis, 2]
#print(SingleIndependentVar)
#print(len(SingleIndependentVar))


# Since this is a supervised learning application we will separate
# our data into training and testing code.  This is done with
# simple slices though we could also do it through a random sample.
# This is a simple 80/20 split.
Independent_TrainingSet = SingleIndependentVar[20:]
Independent_TestingSet  = SingleIndependentVar[:20]


# We have to use the same split for our output variable to ensure
# that they match.
Dependent_TrainingSet = DependentVar[20:]
Dependent_TestingSet  = DependentVar[:20]


# We now load and save the linear regression model for use.
RegressionModel = sklearn.linear_model.LinearRegression()


# Now train the weights for the model using our training sets.
RegressionModel.fit(Independent_TrainingSet, Dependent_TrainingSet)


# Having done that we can now use it to make predictions for our test cases.
Dependent_TestPredictions = RegressionModel.predict(Independent_TestingSet)


# Now that we have done that we can print out information about the model
# coefficients themselves, as well as the error and prediction determination.
# The mean squared error indicates how far "off" the model is, i.s. how much
# it guesses wrong in general while the coefficient of determination gives
# a general success measure with 1 being "perfect".
print("Coefficients: \n", RegressionModel.coef_) #slope

MeanSquaredErr = sklearn.metrics.mean_squared_error(
    Dependent_TestingSet, Dependent_TestPredictions)

print("Mean squared error: {}".format(MeanSquaredErr)) #squared diff

DeterminationCoeff = sklearn.metrics.r2_score(
        Dependent_TestingSet, Dependent_TestPredictions)

print("Coefficient of determination: {}".format(DeterminationCoeff)) #1 is perfect prediction


# Just for readability we can also plot the data on a scatterplot along
# with a fitted line to give an idea of the potential values. The first
# two lines generate the plot while the later three set tick markers and
# show it.
plt.scatter(Independent_TestingSet, Dependent_TestingSet,  color='black')
plt.plot(Independent_TestingSet, Dependent_TestPredictions,
         color='blue', linewidth=3)

plt.xticks(())
plt.yticks(())

plt.show()
