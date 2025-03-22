from flask import Flask, abort, request

app = Flask(__name__)

# @app.route('/login/<user_id>')
# def login(user_id):
#     print(request.args.get('user_id'))
#     # print(isalpha())
#     if user_id:
#         if user_id.isalpha():
#             abort(400, 'bad request: invalid ID')
#         return f'<h1> your id is {user_id} <h1>'
    
#     return f'Invalid id'

# app.run(debug=True)

@app.route('/greet/<name>')
def me(name):
    val = request.args.get('val')
    if name:
        return f'Name {name, val}'
    else:
        return 'unknown'
    
@app.route('/hey/<me>')
def new(me):
    args = request.args
    val2 = request.args.get('key')
    # if val2:
    #     return f'<h1>The val of key is {val2}</h1>'
    
    return f'<h1> Arguments {args} </h1>'

@app.route('/process')
def process():
    username = request.args.get('uname', 'Mad-1')
    print('================================== \n',type(username), len(username), '\n', '==================================')
    if username.isnumeric():
        abort(400, 'Bad request: Numeric username provided')
    return f'Valid one {username}'
    
app.run(debug=True)
