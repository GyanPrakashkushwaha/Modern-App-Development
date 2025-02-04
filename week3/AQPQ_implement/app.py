from flask import Flask, render_template

# List of users
users = [
    {"id": 1, "name": "user_1", "role": "manager"},
    {"id": 2, "name": "user_2", "role": "manager"},
    {"id": 3, "name": "user_3", "role": "manager"},
]

app = Flask(__name__)


@app.route('/me')
def main():
    return render_template('index.html', users=users)  # Pass users correctly

if __name__ == "__main__":
    app.debug = True
    app.run()
