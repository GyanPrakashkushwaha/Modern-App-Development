from flask import Flask, render_template, request
import matplotlib
import os
matplotlib.use('Agg')  # Use the Agg backend for non-GUI environments
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def get_value():
    if request.method == 'GET':
        return render_template(template_name_or_list='index.html')
    
    elif request.method == 'POST':
        obj = Data()
        
        id_name = request.form.get('ID')
        id_value = request.form.get('id_value')
        
        if id_name == None or id_value == '':
            return render_template('error.html')
        else:
            id_value = int(id_value)
        
        
        if id_name == 'student_id':
            id_students = obj.return_ids('student_id')
            print(id_students)
            if id_value in id_students:
                data, total = obj.student_data(id_value)
                return render_template('student.html', data=data, total=total)
            else:
                return render_template('error.html')
        else:
            id_course = obj.return_ids('other')
            if id_value in id_course:
                avg_marks, max_marks, marks = obj.course_data(id_value)
                create_plot(marks)
                return render_template('course.html',avg_marks=avg_marks,max_marks=max_marks)
            else:
                return render_template('error.html')
            
class Data:
    def __init__(self):
        with open('data.csv', 'r') as f:
            _ = f.readline()  # Skip header
            self.content = [line.strip().split(',') for line in f]
    
    def return_ids(self,input_id):
        if input_id == 'student_id':
            return [int(i[0].strip()) for i in self.content]
        else:
            return [int(i[1].strip()) for i in self.content]
        
    def student_data(self,stud_id):
        student_data = []
        total = 0
        for row in self.content:
            student_id = int(row[0].strip())
            if student_id == stud_id:
                student_data.append(row)
                total += int(row[2].strip())
        return student_data, total

    def course_data(self,cour_id):
        marks_lst = []
        for row in self.content:
            course_id = int(row[1].strip())
            if course_id == cour_id:
                marks_lst.append(int(row[2].strip()))

        avg_marks = sum(marks_lst) / len(marks_lst)
        max_marks = max(marks_lst)
        return avg_marks, max_marks, marks_lst
 

def create_plot(marks):
    
    # Ensure the static folder exists
    os.makedirs('static', exist_ok=True)

    # Plot and save histogram
    plt.figure()
    plt.hist(marks, color='blue', alpha=0.7, edgecolor='black')
    plt.xlabel('Marks')
    plt.ylabel('Frequency')
    plt.title('Marks Distribution')
    plt.savefig('static/lab_assi.png')
    plt.close()

if __name__ == '__main__':
    app.run(debug=True)

# 23f3004091