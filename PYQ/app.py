from flask import Flask, render_template, url_for, redirect, request
app = Flask(__name__)

# @app.route("/choice/if")
# def ifelse():
#     user = "MAD I"
#     return render_template("if_example.html", name=user)

# @app.route("/for")
# def for_loop():
#     list_of_courses = ['Java', 'Python', 'DBMS', 'PDSA']
#     return render_template("for_example.html", courses=list_of_courses)

# @app.route("/choice/<pick>")
# def choice(pick):
#     if pick == 'if':
#         return redirect(url_for('ifelse'))
#     if pick == 'for':
#         return url_for('for_loop')


@app.route("/get_value")
def ifelse():
    val1 = request.args.get('val1')
    return "This value is " + val1

if __name__ == "__main__":
    app.run(debug=True)
