from flask import Flask, render_template, request, redirect 
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, current_user, login_user, login_required, logout_user

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///auth_db.sqlite3"  # sqlite:///<db_name>.<extension>
app.config["SECRET_KEY"] = "this-is-secret-key"


db = SQLAlchemy(app)
# db.init_app(app)

# login_manager = LoginManager()
# login_manager.init_app(app)

with app.app_context():
    db.create_all()

# @login_manager.user_loader
# def load_user(user_id):
#     return User


class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key = True)
    user_name = db.Column(db.String, nullable = False, unique = True)
    password = db.Column(db.String, nullable = False)
    
    
@app.route('/login', methods = ['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(user_name = username).first()
        if user:
            if user.pass_word == password:
                return redirect(f'/dashboard/{str(user.user_id)}')
            else:
                return 'INCORRECT PASSWORD'
        else:
            return 'USER NOT FOUND'
        
    return render_template('login.html')

@app.route('/dashboard/<user_id>')
def dashboard(user_id):
    user = User.query.filter_by(user_id = user_id).first()
    # user = User.query.filter_by(user_id = user_id).all()
    return render_template('dashboard.html', user)
    
    

app.run(debug=True)