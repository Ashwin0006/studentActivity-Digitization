from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("welcome.html")

@app.route("/front", methods=['POST', 'GET'])
def front():
    return render_template("front.html")

@app.route("/student", methods=['POST', 'GET'])
def student():
    return render_template("student.html")

if __name__ == "__main__":
    app.run(debug=True)
