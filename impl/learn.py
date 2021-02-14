from keras.models import Sequential
from keras.layers import Dense

import json
import numpy as np
import pandas as pd

#load data to dataframe
with open('data/train.csv') as f:
    train_data_csv = pd.read_csv(f)

print('Head after read csv')
print(train_data_csv.head())

#delete unwanted columns
train_data = train_data_csv.drop(['PassengerId', 'Name', 'Cabin', 'Fare', 'Ticket', 'Embarked'], axis = 1)

print('Head after delete columns')
print(train_data.head())

#seperate x and y
y_train_data = train_data['Survived']
x_train_data = train_data.drop('Survived', axis =1)

print('Head of x and y')
print(x_train_data.head())
print(y_train_data.head())

#map sex to numbers
x_train_data['SexNum'] = pd.Categorical(x_train_data.Sex, ordered=True).codes
print(x_train_data.head()) #1 male 0 female
x_train_data = x_train_data.drop('Sex', axis =1)

#map age to groups
print(x_train_data.describe())
# 0-16 - 0
#16-20 - 1
#20-30 - 2
#30-40 - 3
#40+ - 4
bins = [0, 16, 20, 30, 40, 80]
labels = [0, 1, 2, 3, 4]
x_train_data['AgeNm'] = pd.cut(x_train_data.Age, bins, labels = labels,include_lowest = True)
x_train_data = x_train_data.drop('Age', axis =1)

print(x_train_data.head())


# input has 5 input features Pclass SexNm AgeNm SibSp Parch
input_dim = 5
output_nodes = 2

#create model - in Dense the frst arg is the amount of Nodes
model = Sequential()
model.add(Dense(12, input_dim = input_dim, activation='relu')) # input layer and frst hidden layer
model.add(Dense(8, activation='relu'))
model.add(Dense(1, activation='sigmoid')) # output layer

#cross entropy as the loss argument , used for binary classifaction
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

x_train_data = np.asarray(x_train_data).astype('float32')
y_train_data = np.asarray(y_train_data).astype('float32')
model.fit(x_train_data, y_train_data, epochs=150, batch_size=10)

#model loss and accuracy
print(model.evaluate(x_train_data,y_train_data))

#save model to json
with open('model/model.json', 'w') as outfile:
    json.dump(model.to_json(),outfile)

    #Because the output layer node uses sigmoid activation,
    # the single output node will hold a value between 0.0 and 1.0
    # which represents the probability that the item is the class encoded as 1 in the data (forgery).
    # Put another way, if the prediction value is less than 0.5 then the prediction is class = 0 = "authentic," otherwise the prediction is class = 1 = "forgery."