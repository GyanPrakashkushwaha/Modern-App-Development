from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./database.sqlite3'
db = SQLAlchemy(app)

class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    roll_number = db.Column(db.String, unique = True, nullable = False)
    first_name = db.Column(db.String, nullable = True)
    last_name = db.Column(db.String)
    
class Course(db.Model):
    courses = {'Mad 1': 1, 'DBMS': 2, 'PDSA': 3, 'BDM': 4}
    course_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    course_code = db.Column(db.String, unique = True, nullable = False)
    course_name = db.Column(db.String, nullable = False)
    last_name = db.Column(db.String)
    
class Enrollments(db.Model):
    enrollment_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    estudent_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable = False)
    ecourse_id = db.Column(db.Integer, db.ForeignKey('course.course_id'), nullable = False)
    
with app.app_context():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def home():
    students = {1001: 'hey'}
    return render_template('home.html',student = students)

@app.route('/student/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('create.html')
    elif request.method == 'POST':
        roll_no = request.form.get('roll')
        f_name = request.form.get('f_name')
        l_name = request.form.get('l_name')
        exists = Student.query.filter_by(roll_number = roll_no).first()
        
        
        if not exists:
            tdata = Student(roll_number = roll_no, first_name = f_name, last_name = l_name)
            db.session.add(tdata)
            db.session.commit()
            courses = request.form.getlist('courses')
            
            for course in courses:
                stud_id = exists.student_id if exists else None
                course_id = Course.courses.get(course)
                if stud_id and course_id:
                    db.session.add(Enrollments(estudent_id = stud_id, ecourse_id = course_id))
                    db.session.commit()
                    
            return redirect(url_for('home'))
            
        return render_template('exists.html')



if __name__ == '__main__':
    app.run(debug=True)