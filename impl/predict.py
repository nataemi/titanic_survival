import json
import numpy as np
from tensorflow.python.keras.models import model_from_json

sexMap = {
    'M' : 1,
    'F' : 0
}

ageMap = {
    'M' : 1,
    'F' : 0
}


class Predict:
    def __init__(self):
        with open('model/model.json', 'r') as infile:
            self.model = model_from_json(json.load(infile))
    def predict(self, userinput):
        sample_to_predict = np.array([float(userinput.pclass), float(userinput.sibsp), float(userinput.parch), float(sexMap[userinput.sex]), self.mapAge(int(userinput.age))])
        sample_to_predict = sample_to_predict.reshape([1, 5])
        print('Predicting: ', sample_to_predict)
        # Generate predictions for samples
        prediction = self.model.predict(sample_to_predict)
        print('Prediction', prediction)
        return self.survival(prediction)

    def mapAge(self, age):
        if (age < 16):
            return 0
        if (age < 20):
            return 1
        if (age < 30):
            return 2
        if (age < 40):
            return 3
        return 4

    def survival(self, prediction):
        if(prediction < 0.5):
            return 0
        else:
            return 1
