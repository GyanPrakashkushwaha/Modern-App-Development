from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///api_database.sqlite3'
db = SQLAlchemy(app)
api = Api(app)

class Course(db.Model):
    course_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    course_name = db.Column(db.String, nullable = False)
    course_code = db.Column(db.String, unique = True, nullable = False)
    course_description = db.Column(db.String)
    

with app.app_context():
    # db.session.add(Course(course_id = 2, course_name = 'Mad3',course_code = 'CS2003',course_description= 'Hey There its mad 1 course.'))
    # db.session.commit()
    print('hey there')
    db.create_all()
    

class CourseAPI(Resource):
    def get(self, course_id):
        course = Course.query.get(course_id)
        if not course:
            return 'not found'
        
        print(course)
        
        return jsonify({"id": course.course_id, "name": course.course_name, "code": course.course_code, "desc" : course.course_description})


api.add_resource(CourseAPI, '/api/course/<int:course_id>')

if __name__ == "__main__":
    app.run(debug=True)