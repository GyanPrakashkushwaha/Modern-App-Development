from flask import Flask, render_template, redirect
import pandas as pd
import sys
import matplotlib.pyplot as plt


app = Flask(__name__)

def main():
    global df 
    df = pd.read_csv(r'data.csv')
    if len(sys.argv) >= 2:
        if sys.argv[1] == '-s':
            if sys.argv[2] in list(df['Student id']):
                return student(df)
        elif sys.argv[1] == '-c':
            if sys.argv[2] not in list(df[' Course id']):
                return error()
    else:
        return error()
    

@app.route('/error')
def error():
    return render_template(template_name_or_list='error.html')


@app.route('/student')
def student(df):
    student_id = int(sys.argv[2])
    table_data = df[df['Student id'] == int(sys.argv[2])]
    summation = sum(table_data.iloc[:,-1])
    return render_template(template_name_or_list='student.html',
                           table_data=table_data,
                           submation=summation)

@app.route('/course')
def course(df):
    course_id = int(sys.argv[2])
    marks =  df[df[' Course id'] == course_id][' Marks']

    max_marks = max(marks)
    avg_marks = marks.mean()
    
    # Generate the plot and save it
    plt.hist(marks, bins=10, color='blue', alpha=0.7, edgecolor='black')
    plt.xlabel('Marks')
    plt.ylabel('Frequency')
    plt.title(f'Marks Distribution for Course {course_id}')
    
    plt.savefig('static/lab_assi.png')  # Save inside static folder
    plt.close()  # Close the plot to prevent memory leaks
    
    return render_template(template_name_or_list='course.html',
                           avg_marks=avg_marks,
                           max_marks=max_marks)



if __name__ == '__main__':
    app.debug = True
    app.run()
    
    
    
import sys
from jinja2 import Template
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

# Use a non-GUI backend for Matplotlib (for headless servers)
matplotlib.use('Agg')

WRONG_INPUT = """
<!DOCTYPE html>
<html>
<head>
    <title>Something Went Wrong</title>
</head>
<body>
    <h1>Wrong Inputs</h1>
    <p>Something went wrong</p>
</body>
</html>
"""

STUDENT_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Student data</title>
</head>
<body>
    <h1>Student Details</h1>
    <table border="1px solid">
        <tbody>
            <tr>
                {% for head in table_data.columns %}
                    <th>{{ head }}</th>
                {% endfor %}
            </tr>
        {% for row in table_data.values %}
        <tr>
            {% for val in row %}
                <td>{{ val }}</td>
            {% endfor %}
        </tr>
        {% endfor %}
        <tr>
            <td colspan="2">Total Marks</td>
            <td>{{ summation }}</td>
        </tr>
        </tbody>
    </table>
</body>
</html>
"""

COURSE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Course Data</title>
</head>
<body>
    <h1>Course Details</h1>
    <table border="1px solid">
        <tbody>
            <tr>
                <th>Average Marks</th>
                <th>Maximum Marks</th>
            </tr>
            <tr>
                <td>{{ avg_marks }}</td>
                <td>{{ max_marks }}</td>
            </tr>
        </tbody>
    </table>
    <img src="lab_assi.png" alt="Histogram of Marks">
</body>
</html>
"""

def main():
    try:
        df = pd.read_csv('data.csv')
        df.columns = df.columns.str.strip()
        
        if len(sys.argv) > 2:
            option, value = sys.argv[1], sys.argv[2]
            if option == '-s':
                try:
                    student_id = int(value)
                    if student_id in df['Student id'].values:
                        return student(df, student_id)
                    else:
                        print(f"Error: Student ID {student_id} not found.")
                except ValueError:
                    print("Error: Student ID must be an integer.")
            elif option == '-c':
                try:
                    course_id = int(value)
                    if course_id in df['Course id'].values:
                        return course(df, course_id)
                    else:
                        print(f"Error: Course ID {course_id} not found.")
                except ValueError:
                    print("Error: Course ID must be an integer.")
        else:
            return error()
    except FileNotFoundError:
        print("Error: data.csv not found. Please ensure the file is in the correct directory.")
    except pd.errors.EmptyDataError:
        print("Error: data.csv is empty.")
    except pd.errors.ParserError:
        print("Error: data.csv contains invalid data format.")

def student(data, student_id):
    table_data = data[data['Student id'] == student_id]
    summation = table_data.iloc[:, -1].sum()
    template = Template(STUDENT_TEMPLATE)
    output = template.render(table_data=table_data, summation=summation)
    
    with open('out.html', 'w') as out_doc:
        out_doc.write(output)
    
    print("Student report generated: out.html")

def course(data, course_id):
    marks = data[data['Course id'] == course_id]['Marks']
    max_marks = marks.max()
    avg_marks = marks.mean()
    
    plt.figure()
    plt.hist(marks, bins=10, color='blue', alpha=0.7, edgecolor='black')
    plt.xlabel('Marks')
    plt.ylabel('Frequency')
    plt.title('Marks Distribution')
    plt.savefig('lab_assi.png')
    plt.close()
    
    template = Template(COURSE_TEMPLATE)
    output = template.render(avg_marks=avg_marks, max_marks=max_marks)
    
    with open('out.html', 'w') as out_doc:
        out_doc.write(output)
    
    print("Course report generated: out.html")

def error():
    template = Template(WRONG_INPUT)
    output = template.render()
    
    with open('out.html', 'w') as out_doc:
        out_doc.write(output)
    
    print("Error page generated: out.html")

if __name__ == "__main__":
    main()
