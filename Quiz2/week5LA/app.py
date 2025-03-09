from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
db = SQLAlchemy(app)

# Create Models
class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    roll_number = db.Column(db.String, unique = True, nullable = False)
    first_name = db.Column(db.String, nullable = False)
    last_name = db.Column(db.String)

class Course(db.Model):
    courses = {'course_1': 1, 'course_2': 2, 'course_3': 3, 'course_4': 4}
    course_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    course_code = db.Column(db.String, unique = True, nullable = False)
    course_name = db.Column(db.String, nullable = False)
    course_description = db.Column(db.String)


class Enrollments(db.Model):
    enrollment_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    estudent_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable = False)
    ecourse_id = db.Column(db.Integer, db.ForeignKey('course.course_id'), nullable = False)


with app.app_context():
    db.create_all()
    

@app.route('/', methods = ['GET', 'POST'])
def home():
    student = Student.query.all()
    # print(student)
    return render_template('home.html', student = student)


@app.route('/student/create', methods = ['GET', 'POST'])
def create():
    if request.method == 'POST':
        roll_no = request.form.get('roll_no')
        # check if the student exists or not.
        exists = Student.query.filter_by(roll_number = roll_no).first()
        
        if not exists:
            # then add the student.
            f_name = request.form.get('f_name')
            l_name = request.form.get('l_name')
            stud = Student(roll_number = roll_no, first_name = f_name, last_name = l_name)
            db.session.add(stud)
            db.session.commit()
            # It's time to add entry to Enrollments Table.
            # For that I have to fetch the courses
            courses = request.form.getlist('courses')
            # print(courses)
            
            for course in courses:
                # print('Hey Im  Here Do you remember? for')
                student = Student.query.filter_by(roll_number = roll_no).first()
                course_id = Course.courses.get(course)
                # print(f'Student id {student.student_id} , course id : {course_id}')
                if student.student_id and course_id:
                    # print('Hey Im  Here Do you remember?')
                    db.session.add(Enrollments(estudent_id = student.student_id, ecourse_id = course_id))
                    db.session.commit()
                    
            return redirect(url_for('home'))
        
        else:
            return '<p> STudent already exists. Please use different Roll Number</p>'
                    
                    
    return render_template('create.html')


@app.route('/student/<int:stud_id>/update', methods = ['GET', 'POST'])
def update(stud_id):
    # print(stud_id)
        
            
    if request.method == 'POST':
        stud = Student.query.filter_by(student_id = stud_id).first() # Got student details.
        print(stud)
        # simply overrid them.
        stud.first_name = request.form.get('first_name')
        stud.last_name = request.form.get('l_name')
        # print(request.form.get('l_name'))
        # print(request.form.get('first_name'))
        
        # delete all the relationship with enrollments. then add them again.
        Enrollments.query.filter_by(estudent_id = stud.student_id).delete()
        courses = request.form.getlist('courses')
        
        for course in courses:
            enroll_data = Enrollments(estudent_id = stud.student_id, ecourse_id = Course.courses.get(course))
            db.session.add(enroll_data)
            db.session.commit()
            
        return redirect('/')
        
    try:
        stud = Student.query.filter_by(student_id = stud_id).first()
        # print(stud)
        enrolls = Enrollments.query.filter_by(estudent_id = stud_id)
        # print(Enrollments.query.filter_by(estudent_id = stud_id).first())
        # print('============================= without first =============================')
        # print(Enrollments.query.filter_by(estudent_id = stud_id))
        # print('enrolls is here -=========================================================== \n',enrolls)
        cid = [enroll.ecourse_id for enroll in enrolls]
        # print(cid)
        return render_template('update.html', stud = stud, cid = cid)
    except:
        print('something went wrong.')
    return 'here there'


@app.route('/student/<int:stud_id>/delete', methods = ['GET'])
def delete(stud_id):
    stud = Student.query.filter_by(student_id = stud_id).first()
    if stud:
        db.session.delete(stud)  
        db.session.commit()
        Enrollments.query.filter_by(estudent_id=stud_id).delete()
        db.session.commit()

    return redirect(url_for('home'))
    
if __name__ == '__main__':
    app.run(debug=True)













