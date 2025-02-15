

# app = Flask(__name__)

# @app.route('/home')
# @app.route('/work')
# def my_task():
#     return "<h1>Hello! Reporting for my task</h1>"

# app.run(debug=True)


##################################################################################################################
# from flask import Flask, url_for
# import pyhtml as h


# app = Flask(__name__)

# @app.route('/')
# # @app.route('/me')
# def index():
#     return str(h.html(h.body(h.h1('Mad-I welcomes you!'))))

# @app.route('/user/<username>')
# def profile(username):
#     return f'<h1> {username}\'s profile </h1>'

# with app.test_request_context():
#     print(url_for('index'))  # Expected Output: /home
#     print(url_for('profile', username='Harry'))  # Expected Output: /user/Harry
#     print(url_for('profile', username='Harry', next='course'))  # Expected: /user/Harry?next=course
#     print(url_for('index', username='Harry'))  # Expected Output: /home?username=Harry


# app.run(debug=True)
##################################################################################################################


# from flask import Flask
# app = Flask(__name__)

# @app.route('/')
# def generate1():
#     return "This is generate1"

# @app.route('//')
# def generate2():
#     return "This is generate2"

# @app.errorhandler(404)
# def page_not_found(e):
#     # setting 404 status explicitly
#     return 'page not found'

# app.run()




##################################################################################################################

from flask import Flask,request
app = Flask(__name__)

@app.route('/')


@app.route('/employee', methods = ['GET', 'POST'])
def show_details():
    det = request.args
    print(det,'\n\n')

    details = {
                'Department': det['dept'],
                'Id': det['id'],
                'Profession': det['prof'],
                'Endpoint' : det['endpoint']
            }
    print(details)
    return details

app.run(debug=True)