# -*- coding: utf-8 -*-
"""Neural Network Model for Regression.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/11KRrSo2Jf3YMo-vVT7VktTMytbNw7tYb

# Neural Network Model for Regression.

## Assignment-1

1. Modifying the model in lab 3.2 to do Regression (+5 pts)

1. Implementing the Learning Algorithm

1.1 Importing Packages
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""1.2 Parameter Initialization"""

"""
nx is the number of neurons in the input layer (i.e., the number of features in the dataset)
nh is the number of neurons in the hidden layer
ny is the number of neurons in the output layer (For this example we are using one nueron in the output layer so ny=1)
"""
def initialize_parameters(nx,nh,ny):
    #set the random seed so the same random values are generated every time you run this function
    np.random.seed(1)


    #initialize weights to small random numbers and biases to zeros for each layer
    W1=np.random.uniform(size=(nh,nx), low=-0.01, high=0.01)
    b1=np.zeros((nh,1))
    W2=np.random.uniform(size=(ny,nh), low=-0.01, high=0.01)
    b2=np.zeros((ny,1))

    #create a dictionary of network parameters
    parameters = {"W1": W1,
                  "b1": b1,
                  "W2": W2,
                  "b2": b2}

    return parameters

"""1.3 Forward Pass"""

#relu activation
def relu(z):
    return np.maximum(0,z)

"""
In forward pass we do the computations in the computational graph. We cache the intermediate nodes we will later need in the backward pass
"""
def forward_pass(parameters,X):
    Z1= np.dot(parameters["W1"],X)+parameters["b1"] # b1 is broadcasted n times before it is added to np.dpt(W1,X1)
    A1=relu(Z1)
    Z2=np.dot(parameters["W2"],A1)+parameters["b2"] #b2 is broadcasted n times before it is added to np.dpt(W2,A1)
    Yhat=(Z2)

    cache = {"A1": A1,
             "Z1":Z1,
             "Z2": Z2}
    return Yhat,cache

"""Let's also write a utility method to compute the loss

Use Mean Squared Error for the loss function (slide 21). The gradient of Mean Squared Error with respect to the network output 𝑌𝑌� for each training example is computed as follows:
"""

"""
n is the number of examples, y is a vector of actual/observed outputs and yhat is a vector of predicted outputs
"""
def compute_loss(Y, Yhat):

    n=Y.shape[1]
    loss = (1 / n) * (np.sum((Y - Yhat) * (Y - Yhat)))
    return loss

"""1.4 Backward Pass"""

def dMeanSquareLoss(Y,Yhat):
    return (Yhat - Y)


def drelu(Z):
    """
np.where(condition, x, y) for each element of the array returns x if condition is true otherwise returns y.
In this case for each element Z drelu=1 if the element is greater than 0 otherwise drelu=0
"""
    drelu=np.where(Z>0, 1.0, 0.0)
    return drelu

def backward_pass(parameters, cache, X, Y, Yhat):
    n=X.shape[1]
    dZ2=dMeanSquareLoss(Y, Yhat )*1
    dW2=(1/n)*np.dot(dZ2,cache["A1"].T)
    db2=(1/n)*np.sum(dZ2, axis=1, keepdims=True)
    dA1=np.dot(parameters["W2"].T,dZ2)
    dZ1=dA1*drelu(cache["Z1"])
    dW1=(1/n)*np.dot(dZ1,X.T)
    db1=(1/n)*np.sum(dZ1, axis=1, keepdims=True)
    gradients={"dW1": dW1,
             "db1": db1,
             "dW2":dW2,
              "db2":db2
              }
    return gradients

"""1.4 Using Gradient Descent To update the parameters"""

def update_parameters(parameters, gradients, learning_rate):
    parameters["W1"]=parameters["W1"]-learning_rate*gradients["dW1"]
    parameters["W2"]=parameters["W2"]-learning_rate*gradients["dW2"]
    parameters["b1"]=parameters["b1"]-learning_rate*gradients["db1"]
    parameters["b2"]=parameters["b2"]-learning_rate*gradients["db2"]
    return parameters

"""1.5 Putting it all together, Creating the NN Model"""

"""
Arguments: train_X: is the training dataset (features)
           train_Y: is the vector of labels for training_X
           val_X: is the vector of validation dataset (features)
           val_y: is the vector of labels for val_X
           nh: is the number of neurons in the hidden layer
           num_iterations: The number of iterations of gradient descent
"""
def create_nn_model(train_X,train_Y,nh, val_X, val_Y, num_iterations, learning_rate):
    """
    Do some safety check on the data before proceeding.
    train_X and val_X must have the same number of features (i.e., same number of rows)
    train_X must have the same number of examples as train_Y (i.e., same number of columns )
    val_X must have the same number of examples as Val_Y
    """
    assert(train_X.shape[0]==val_X.shape[0]), "train_X and val_X must have the same number of features"
    assert(train_X.shape[1]==train_Y.size), "train_X and train_Y must have the same number of examples"
    assert(val_X.shape[1]==val_Y.size), "val_X and val_Y must have the same number of examples"


    #getting the number of features
    nx=train_X.shape[0]

     # We want to use this network for binary classification, so we have only one neuron in the output layer with a sigmoid activation
    ny=1

    # initializing the parameteres
    parameters=initialize_parameters(nx,nh,ny)


    #initialize lists to store the training and valideation losses for each iteration.
    val_loss=[]
    train_loss=[]

    #run num_iterations of gradient descent
    for i in range (0, num_iterations):
        #run the forward pass on train_X
        Yhat_train, train_cache= forward_pass(parameters,train_X)

        #run the forward pass on val_X
        Yhat_val,val_cache= forward_pass(parameters,val_X)

        #compute the loss on the train and val datasets
        train_loss.append(compute_loss(train_Y,Yhat_train))
        val_loss.append(compute_loss(val_Y,Yhat_val))


        """
        run the backward pass. Note that the backward pass is only run on the training data not the validation data
        Because the learning must be only done on the training data and hence, validation data is not used to update
        the model parameters.
        """
        gradients=backward_pass(parameters, train_cache, train_X, train_Y,Yhat_train)


        # update the parameters
        parameters=update_parameters(parameters, gradients, learning_rate)

        #print the trianing loss and validation loss for each iteration.
        print("iteration {} :train_loss:{} val_loss{}".format(i,train_loss[i],val_loss[i]))

    #create a dictionary history and put train_loss and validaiton_loss in it
    history={"val_loss": val_loss,
             "train_loss": train_loss}


        #return the parameters and the history
    return parameters, history

"""1.5 predicting and evaluating the NN model"""

def predict(parameters,X, prob_threshold=0.5):
    Yhat,cache=forward_pass(parameters, X)
    # predict class 1 if the output is greater than prob_threshold; otherwise, predict zero
    #predicted_label=np.where(Yhat>prob_threshold, 1, 0)
    return Yhat

"""**2. Preparing California Housing Data (+6pts)**"""

import pandas as pd
import numpy as np

cal_df1=pd.read_csv("sample_data/california_housing_train.csv", header=0)

cal_df2=pd.read_csv("sample_data/california_housing_test.csv")

"""Split the training data into 80% training and 20% validation. There are several ways to do this; for instance, you can use dataframe sample method"""

train_cal1 = cal_df1.sample(frac=0.8)
val_cal1 = cal_df1.drop(train_cal1.index)

"""Convert the train/validation/and test data into numpy arrays using to_numpy method"""

train_cal_2 = train_cal1.to_numpy()
val_cal_2 = val_cal1.to_numpy()

train_cal = np.transpose (train_cal_2)
val_cal = np.transpose(val_cal_2)

test_cal1 = cal_df2.to_numpy()
test_cal = np.transpose(test_cal1)

print(train_cal.shape)
print(val_cal.shape)
print(test_cal.shape)

#everything minus the last row is X
train_cal_X=train_cal[:-1,]
#the last row (at index -1) is Y
train_cal_Y=train_cal[-1,:]

# the labels train_Y and val_Y have to be reshaped to a 2D array for the matrix operations to work in the forward and backward passes
train_cal_Y=np.reshape(train_cal_Y, (1,train_cal_Y.size))


#The mean function calculates the mean of the elements along a given axis (in this case axis=1 indicates calculation along the rows) and the keepdims argument ensures that the mean is returned as a 2D array with a single column,
#even if the input array is 1D. The std function calculates the standard deviation in the same way.
mean_cal_train = train_cal_X.mean(axis=1, keepdims=True)
sdv_cal_train = train_cal_X.std(axis=1, keepdims=True)

val_cal_X=val_cal[:-1,]
val_cal_Y=val_cal[-1,]
val_cal_Y=np.reshape(val_cal_Y, (1,val_cal_Y.size))

test_cal_X=test_cal[:-1,]
test_cal_Y=test_cal[-1,]
test_cal_Y=np.reshape(test_cal_Y, (1,test_cal_Y.size))

"""subtracting the mean and normalizing the data,By dividing the features with their standard deviation, the features are scaled to unit variance."""

traincalX = train_cal_X - mean_cal_train
traincalX = traincalX/sdv_cal_train

valcalX = val_cal_X - mean_cal_train
valcalX = valcalX/sdv_cal_train

testcalX = test_cal_X - mean_cal_train
testcalX = testcalX/sdv_cal_train

"""Let’s divide the median_house_values by 100K to scale them down."""

traincalY = train_cal_Y/100000
valcalY = val_cal_Y/100000
testcalY = test_cal_Y/100000

train_X = traincalX
val_X = valcalX
test_X = testcalX

train_Y = traincalY
val_Y = valcalY
test_Y = testcalY

print(train_X.shape)
print(val_X.shape)
print(test_X.shape)
print(train_Y.shape)
print(val_Y.shape)
print(val_Y.shape)

iterations=1000
parameters, history=create_nn_model(train_X,train_Y,60, val_X,val_Y, iterations,0.08)

