from flask import Flask, abort, request

app = Flask(__name__)
data = {'PDSA': 'CS2003',
        'DBMS': 'CS2004',
        'JAVA': 'CS2005'}

@app.route('/course/<course_name>')
def course(course_name):
    # if course_name:
    #     return f'<h1> {course_name}</h1>'
    course_id = request.args.get('id')
    if course_name in data and course_id == data[course_name]:
        return f'<h1> The course ID for {course_name} is: {course_id}'
    else:
        abort(400,'Bad Request : Invalid Data')

# @app.route('/login/<id>')
# def login(id):
#     if id:
#         if id.isalnum():
#             abort(400, 'Bad Request: Invalid ID')
#         return f'<h1>Your id is {id}</h1>'
#     return f'Invalid ID'


@app.route('/login/<id>')
def login(id):
    if id:
        if id.isalnum():
            abort(400, "Bad Request: Invalid ID")
        return f'<h1>Your ID is: {id}</h1>'
    return f'<h1>Invalid ID</h1>'

app.run(debug=True)
app.run(debug=True)















