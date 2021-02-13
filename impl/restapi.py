from flask import Flask
from flask_restful import Resource, Api, reqparse
import json
from pandas import DataFrame

from impl.database import DataBaseConnector
from impl.userinput import UserInput


class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return super().default(obj)
        except TypeError:
            return str(obj)


class UserInputData(Resource):
    def get(self):
        data_base_connector = DataBaseConnector()
        result = data_base_connector.select_all_data()
        print(result)
        return {'data': json.dumps(result, cls=DatetimeEncoder)}, 200  # return data and 200 OK code

    def post(self):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('pclass', required=True)  # add args
        parser.add_argument('age', required=True)
        parser.add_argument('sex', required=True)
        parser.add_argument('sibsp', required=True)
        parser.add_argument('parch', required=True)
        args = parser.parse_args()  # parse arguments to dictionary
        user_input = UserInput(args['pclass'], args['age'], args['sex'], args['sibsp'], args['parch'], 1) # ostatni argument to wyliczenie survival
        data_base_connector = DataBaseConnector()
        data_base_connector.insert_data(user_input)
        return 1, 200

class Stats(Resource):
    def get(self):
        data_base_connector = DataBaseConnector()
        result = data_base_connector.select_all_data()
        df = DataFrame(result, columns=['DbId', 'Pclass', 'Age', 'Sex', 'SibSp', 'Parch', 'DtCret', 'Survival'])
        print(df)
        sex_stats = (df['Sex'].value_counts(normalize=True) * 100)
        pclass_stats = (df['Pclass'].value_counts(normalize=True) * 100)
        return { 'sex_stats' : sex_stats.to_json(), 'pclass_stats' : pclass_stats.to_json()}, 200


app = Flask(__name__)
api = Api(app)
api.add_resource(UserInputData, '/user_input_data')  # '/users' is our entry point for Users
api.add_resource(Stats, '/stats')  # '/users' is our entry point for Users


if __name__ == '__main__':
    app.run()  # run our Flask app