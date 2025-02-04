from flask import Flask, render_template, request,redirect,url_for

app = Flask(__name__)

# @app.route("/me",methods = ["GET","POST"])
# def hello_world():
#     if request.method == "GET":
#         return render_template('form.html')
#     elif request.method == 'POST':
#         # get the value from form.
#         val = request.form['your_name']
#         return render_template('display_form.html',display_name= val)
#     else:
#         print('Encountered Error')

# if __name__ == "__main__":
#     app.debug = True
#     app.run()
    

@app.route('/home')
def index():
    return 'This is omepage content'

@app.route('/')
def homepage():
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.debug = True
    app.run()