from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

class MyApi(Resource):
    def get(self):
        return {'greet': 'Hello from GET api'}
    
    def put(self):
        return {'greet': 'hello from PUT api'}
    
    def post(self):
        return {'greet': 'hello from POST api'}

class TestApi(Resource):
    def get(self):
        return {
            "val1": "value1",
            "val2": "value2",
            "val3": "value3"
        }
    
    def delete(self, val):
        return {
            "message": "Value deleted successfully",
            "value": val
        }, 200
    
    def put(self, val):
        return {
            "message": "Value updated successfully",
            "value": val
        }, 200

api.add_resource(TestApi, '/delete', '/get_values', '/delete/<val>', '/update/<val>')
# api.add_resource(MyApi, '/api/get', '/api/put', '/api/post')

app.run()

    

