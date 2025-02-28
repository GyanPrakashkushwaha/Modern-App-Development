from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./users.sqlite3'
db = SQLAlchemy(app)
api = Api(app)

# Schema for the project.
class User(db.Model):
    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    name = db.Column(db.String, nullable = False, unique = True)
    email = db.Column(db.String)
    
# This is to create the database    
with app.app_context(): # `app_context` -> The DB needs application level access to give that we use it. [If we put the db.create_all() in a route then it will be not required.]
    db.create_all()
    
# API
class UserAPI(Resource): # As I have to pass HTTP methods and make it a API I have to inherit Rources[This let the class act as a API(OR gives functionality of http methods like-[GET, PUT, POST.....])]
    # Define GEt method
    def get(self, user_id):
        # have to query to the database and then fetch.
        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "user not found"})
        
        return jsonify({"id": user.id, "name": user.name, "email": user.email})
    
    def post(self, user_id):
        # First take the data.
        data = request.get_json()
        if data:
            new_user = User(id = user_id, name = data['name'], email = data['email'])
            db.session.add(new_user)
            db.session.commit()
            return jsonify({"message": "User Added", "data" : data})

    def put(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({"message" : "User Not Found"})
        data = request.get_json()
        user.name = data['name']
        user.email = data['email']
        db.session.commit()
        return jsonify({"message": "User updated", "data": {"name": user.name, "email": user.email}})
    
    def delete(self, user_id):
        user = User.query.get(user_id)
        user_name = user.name
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify({"message": f" {user_name} user delted "})
        
        return jsonify({"message": "user not found."})

        

# adding URL
api.add_resource(UserAPI, '/user/', '/user/<int:user_id>')




if __name__ == '__main__':
    app.run(debug=True)






