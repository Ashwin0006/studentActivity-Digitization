from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/view_details", methods=['POST', 'GET'])
def view_details():
    return render_template("view_details.html")

@app.route("/student_login", methods=['POST', 'GET'])
def student_login():
    return render_template("student_login.html")

@app.route("/faculty_login", methods=['POST', 'GET'])
def faculty_login():
    return render_template("faculty_login.html")

@app.route("/admin_login", methods=['POST', 'GET'])
def admin_login():
    return render_template("admin_login.html")

@app.route("/student", methods=['POST', 'GET'])
def student():
    return render_template("student.html")

@app.route("/faculty_home", methods=['POST', 'GET'])
def faculty_home():
    return render_template("faculty_home.html")

if __name__ == "__main__":
    app.run(debug=True)
