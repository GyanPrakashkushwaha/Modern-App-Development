from flask import Flask, render_template, request, redirect, url_for, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, fields, marshal_with, reqparse
from werkzeug.exceptions import HTTPException
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./api_database.sqlite3'

db = SQLAlchemy()
db.init_app(app)
# app.app_context().push()
api = Api(app)


# Models
class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    roll_number = db.Column(db.String, unique = True, nullable = False)
    first_name = db.Column(db.String, nullable = True)
    last_name = db.Column(db.String)
    courses = db.relationship('Course', backref = 'student', secondary = 'enrollment', cascade = 'all,delete')


class Course(db.Model):
    course_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    course_name = db.Column(db.String, nullable = False)
    course_code = db.Column(db.String, unique = True, nullable = False)
    course_description = db.Column(db.String)
    

class Enrollment(db.Model):
    enrollment_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable = False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'), nullable = False)
    
    

with app.app_context():
    db.create_all()
    

# Exception Handling # IF the API's calls get's fails then we need to handel them that's why we are doing this.
class NotFoundError(HTTPException):
    def __init__(self, status_code, message = ''):
        self.response = make_response(message, status_code)
    
class NotGivenError(HTTPException):
    def __init__(self, status_code, error_code,error_message):
        message = {
            "error_code" : error_code,
            "error_message" : error_message}
        self.response = make_response(json.dumps(message), status_code)


# Output Fields
# This is for marshal_with (should be same as database fields)
student_fields = {
    "student_id" : fields.Integer,
    "first_name" : fields.String,
    "last_name" : fields.String,
    "roll_number" : fields.String,
}

course_fields = {
    "course_id" : fields.Integer,
    "course_name" : fields.String,
    "course_code" : fields.String,
    "course_description" : fields.String,
}


# Parser
# This works for retrieving the data like `request.form.get('id')`

course_parser = reqparse.RequestParser()
course_parser.add_argument('course_name')
course_parser.add_argument('course_code')
course_parser.add_argument('course_description')

student_parser = reqparse.RequestParser()
student_parser.add_argument('first_name')
student_parser.add_argument('last_name')
student_parser.add_argument('roll_number')

enrollment_parser = reqparse.RequestParser()
student_parser.add_argument('course_id')



# ------------------------- API -----------------------------------
class CourseAPI(Resource):
    """ Because of the inheritance of "Recourse" I can define all HTTP methods like get put post delete.
    @marshal_with(course_fields) ensures that only the defined fields in course_fields are included in the API response.
    If course is found, marshal_with ensures that only course_id, name, and description are included in the response.
    """
    @marshal_with(course_fields)
    def get(self, course_id):
        course = Course.query.filter(Course.course_id == course_id).first()
        if course:
            return course
        else:
            raise NotFoundError(status_code=404)
        
        
    @marshal_with(course_fields)
    def post(self):
        args = course_parser.parse_args()
        course_name = args.get('course_name', None)
        course_code = args.get('course_code', None)
        course_description = args.get('course_description', None)
        if not course_name:
            raise NotGivenError(status_code=400, error_code= 'COURSE001', error_message= 'Course Name is required')
        if not course_code:
            raise NotGivenError(status_code=400, error_code= 'COURSE002', error_message= 'Course Code is required')
        
        course = Course.query.filter(Course.course_code == course_code).first()
        if course is None:
            course = Course(course_name = course_name, course_code = course_code, course_description = course_description)
            db.session.add(course)
            db.session.commit()
            return course, 201
        else:
            raise NotFoundError(status_code=400)
        
        
    @marshal_with(course_fields)
    def put(self, course_id):
        course = Course.query.filter(Course.course_id == course_id).first()
        if not course:
            raise NotFoundError(status_code=404)
        args = course_parser.parse_args()
        course_name = args.get('course_name', None)
        course_code = args.get('course_code', None)
        course_description = args.get('course_description', None)
        
        if not course_name:
            raise NotGivenError(status_code=400, error_code= 'COURSE001', error_message= 'Course Name is required')
        elif not course_code:
            raise NotGivenError(status_code=400, error_code= 'COURSE002', error_message= 'Course Code is required')
        else: # Updating Here.
            course.course_name = course_name            
            course.course_code = course_code
            course.course_description = course_description            
            db.session.add(course)
            db.session.commit()            
            
            return course

    @marshal_with(course_fields)
    def delete(self, course_id):
        course = Course.query.filter(Course.course_id == course_id).scalar()
        if not course:
            raise NotFoundError(404)
        db.session.delete(course)
        db.session.commit()
        
        return "", 200
    
    
class StudentAPI(Resource):
    @marshal_with(student_fields)
    def get(self, student_id):
        student = Student.query.filter(Course.course_id == student_id).first()
        if student:
            return student
        else:
            raise NotFoundError(status_code=404)
        
    @marshal_with(student_fields)
    def post(self):
        args = student_parser.parse_args()
        first_name = args.get('first_name', None)
        last_name = args.get('last_name', None)
        roll_number = args.get('roll_number', None)
        if not roll_number:
            raise NotGivenError(status_code=400, error_code= 'STUDENT001', error_message= 'Roll Number required')
        if not first_name:
            raise NotGivenError(status_code=400, error_code= 'STUDENT002', error_message= 'First Name is required')
        
        student = Student.query.filter(Student.roll_number == roll_number).first()
        if student is None:
            student = Student(first_name = first_name, last_name = last_name, roll_number = roll_number)
            db.session.add(student)
            db.session.commit()
            return student, 201
        else:
            raise NotFoundError(status_code=409)
        

    @marshal_with(student_fields)
    def put(self, student_id):
        student = Student.query.filter(Student.student_id == student_id).first()
        if not student:
            raise NotFoundError(status_code=404)
        args = student_parser.parse_args()
        first_name = args.get('first_name', None)
        last_name = args.get('last_name', None)
        roll_number = args.get('roll_number', None)
        
        if not roll_number:
            raise NotGivenError(status_code=400, error_code= 'STUDENT001', error_message= 'Roll Number required')
        elif not first_name:
            raise NotGivenError(status_code=400, error_code= 'STUDENT002', error_message= 'First Name is required')
        else: # Updating Here.
            student.first_name = first_name            
            student.last_name = last_name
            student.roll_number = roll_number            
            db.session.add(student)
            db.session.commit()
            
            return student

    @marshal_with(student_fields)
    def delete(self, student_id):
        student = Student.query.filter(Student.student_id == student_id).scalar()
        if not student:
            raise NotFoundError(404)
        db.session.delete(student)
        db.session.commit()
        
        return "", 200


class EnrollmentAPI(Resource):
    def get(self, student_id):
        student = Student.query.filter(Student.student_id == student_id).first()
        
        if not student:
            raise NotGivenError(status_code=400, error_code= 'ENROLLMENT002', error_message= 'Student does not exist.')
        
        enrollments = Enrollment.query.filter(Enrollment.student_id == student_id).all()
        
        if enrollments:
            enrolls = []
            for enroll in enrollments:
                enrolls.append({'enrollment_id': enroll.enrollment_id, 
                                'student_id': enroll.student_id,
                                'course_id': enroll.course_id})

            return enrolls
        else:
            raise NotFoundError(404)
        
    
    def post(self, student_id):
        student = Student.query.filter(Student.student_id == student_id).first()
        if student:
            args = enrollment_parser.parse_args()
            course_id = args.get('course_id', None)
            course = Course.query.filter(Course.course_id == course_id).first()
            
            if course:
                enroll = Enrollment(student_id = student_id, course_id = course_id)
                db.session.add(enroll)
                db.session.commit()
            else:
                raise NotGivenError(status_code=400, error_code= 'ENROLLMENT001', error_message= 'Course does not exist')
            
            return [{'enrollment_id': enroll.enrollment_id, 'student_id': enroll.student_id, 'course_id': enroll.course_id}]
        
        else:
            raise NotFoundError(404)
        
    
    def delete(self, student_id, course_id):
        course = Course.query.filter(Course.course_id == course_id).first()
        if not course:
            raise NotGivenError(status_code=400, error_code= 'ENROLLMENT001', error_message= 'Course does not exist')
        
        student = Student.query.filter(Student.student_id == student_id).first()     
        if not student:
            raise NotGivenError(status_code=400, error_code= 'ENROLLMENT002', error_message= 'Student does not exist.')
        
        enrollments = Enrollment.query.filter(Enrollment.student_id == student_id).all()
        if enrollments:
            for enroll in enrollments:
                if enroll.course_id == course_id:
                    db.session.delete(enroll)
            db.session.commit()
        else:
            raise NotFoundError(404)
        



# Recourses (URL to fetch the content).
api.add_resource(CourseAPI,'/api/course/<int:course_id>', '/api/course')
api.add_resource(StudentAPI,'/api/student/<int:student_id>', '/api/student')
api.add_resource(EnrollmentAPI, '/api/student/<int:student_id>/course')


if __name__ == '__main__':
    app.run(debug=True)

































