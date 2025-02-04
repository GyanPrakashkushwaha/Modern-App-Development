import sys
from jinja2 import Template
import pandas as pd
import matplotlib.pyplot as plt

WRONG_INPUT = """<!DOCTYPE html>
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

STUDENT_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <title>Student data</title>
</head>
<body>
    <h1>Student Details</h1>
    <table border="1px solid">
        <tbody>
            <tr>
                {% for head in table_data.columns%}
                    <th>{{head}}</th>
                {% endfor %}
            </tr>
            
        {% for row in table_data.values%}
        <tr>
            {% for val in row%}
                <td>{{val}}</td>
            {% endfor %}
        </tr>
        {% endfor %}
            <tr>
                <td colspan="2">Total Marks</td>
                <td>{{submation}}</td>
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
                <td>{{avg_marks}}</td>
                <td>{{max_marks}}</td>
            </tr>
        </tbody>
    </table>
    <img src="lab_assi.png" alt="IMG">
</body>
</html>
"""

def main():
    df = pd.read_csv(r'data.csv')
    df.columns = df.columns.str.strip()
    if len(sys.argv) > 1:
        if sys.argv[1] == '-s':
            student_id = int(sys.argv[2])
            if student_id in list(df['Student id']):
                return student(df,student_id)
            else:
                error()
        elif sys.argv[1] == '-c':
            course_id = int(sys.argv[2])
            if course_id in list(df['Course id']):
                return course(df,course_id)
            else:
                error()
        else:
            error()
    else:
        return error()
            
def student(data,student_id):
    table_data = data[data['Student id'] == student_id]
    summation = table_data.iloc[:,-1].sum()
    template = Template(STUDENT_TEMPLATE)
    output = template.render(table_data=table_data,submation=summation)
    create_file(output)

    
def course(data,course_id):
    marks =  data[data['Course id'] == course_id]['Marks']
    max_marks = max(marks)
    avg_marks = marks.mean()
    
    plt.figure()
    plt.hist(marks, bins=10, color='blue', alpha=0.7, edgecolor='black')
    plt.xlabel('Marks')
    plt.ylabel('Frequency')
    plt.savefig('lab_assi.png')
    plt.close()
    
    template = Template(COURSE_TEMPLATE)
    output = template.render(avg_marks=avg_marks, max_marks=max_marks)
    
    create_file(output)

def error():
    template = Template(WRONG_INPUT)
    output = template.render()
    create_file(output)

        
def create_file(output):
    with open('output.html', 'w') as out_doc:
        out_doc.write(output)
        
if __name__ == "__main__":
    main()