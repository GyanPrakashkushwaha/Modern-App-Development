from flask import Flask, url_for, request

app = Flask(__name__)

@app.route('/home')
def index():
    return 'Mad-I welcomes you!'

@app.route('/user')
def profile(username):
    return f'{username}\'s profile'

@app.route('/employee', methods = ['GET', 'POST'])
def show_details():
    det = request.args
    details = {
                'Department': det['dept'],
                'Id': det['id'],
                'Profession': det['prof']
            }
    return details

with app.test_request_context():
    # print(url_for('index'))
    # print(url_for('profile', username='Harry', next='me', hey='bol be'))
    print(url_for('show_details', dept='cs', id='CS233', prof='GyanPrakash'))

app.run(debug=True)
    
# @app.err