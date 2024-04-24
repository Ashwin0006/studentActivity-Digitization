from flask import Flask, render_template, request, redirect
import mysql.connector

# Initialize the database!
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Ash123',
    'database': 'digitization',
    'auth_plugin': 'mysql_native_password' 
}
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/view_details", methods=['POST', 'GET'])
def view_details():
    # Latest Achievements!
    cursor.execute("""SELECT student_name, award_name, event_name, month, year, competition_level 
                   FROM awards
                   WHERE year is not null 
                   ORDER BY year desc
                   LIMIT 2""")
    data_latest = cursor.fetchall()
    latest_1 = f"{data_latest[0][0]} has won {data_latest[0][1]} in the event {data_latest[0][2]} on {data_latest[0][3]}, {data_latest[0][4]} which is a {data_latest[0][5]} competition!"
    latest_2 = f"{data_latest[1][0]} has won {data_latest[1][1]} in the event {data_latest[1][2]} on {data_latest[1][3]}, {data_latest[1][4]} which is a {data_latest[1][5]} competition!"

    cursor.execute("""SELECT student_name, award_name, event_name, month, year, competition_level 
                   FROM awards 
                   ORDER BY year
                   LIMIT 10""")
    data_acheivements = cursor.fetchall()

    return render_template("view_details.html", latest_1 = latest_1, latest_2 = latest_2, data_rows = data_acheivements)

@app.route("/search", methods=["POST", "GET"])
def search():
    data = request.form
    print(data)
    # Extract search criteria from the JSON object
    student_name = data.get("student_name")
    award_name = data.get("award_name")
    keyword = data.get("keyword")
    year = data.get("year")
    competition_level = data.get("level")
    tech = data.get("tech")

    
    if keyword:
        query = "SELECT * FROM awards WHERE 1=0"
        query += f" OR student_name LIKE '%{keyword}%'"
        query += f" OR award_name LIKE '%{keyword}%'"
        query += f" OR tech LIKE '%{keyword}%'"
        query += f" OR event_name LIKE '%{keyword}%'"
        if isinstance(keyword, int):
            query += f" OR event_name = {keyword}"

    else:
        query = "SELECT * FROM awards WHERE 1=1"
        if student_name:
            query += f" AND student_name LIKE '%{student_name}%'"
        if award_name:
            query += f" AND award_name LIKE '%{award_name}%'"
        if year:
            query += f" AND year = {year}"
        if competition_level:
            query += f" AND competition_level LIKE '%{competition_level}%'"
        if tech:
            if tech == "Non Tech":    
                query += f" AND tech = 'Non Tech'"
            else:
                query += f" AND tech = 'Tech'"

    print(query)
    cursor.execute(query)
    data_table = cursor.fetchall()
    data_table.insert(0, ("AWARD NAME", "TEAM/INDIVIDUAL", "STUDENT NAME", "LEVEL", "COMPETITION NAME", "MONTH", "YEAR", "PROOF", "AVAILABILITY", "CATEGORY"))

    return render_template("display_data.html", table_data=data_table)

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
    user_name = request.form["username"]
    password = request.form["password"]

    cursor.execute("SELECT * FROM users")
    data_pairs = cursor.fetchall()

    for data in data_pairs:
        if(data[0] == user_name and data[1] == password):
            return render_template("faculty_home.html")
    
    return render_template("error.html", error_message = "Invalid Login")

@app.route("/admin_home", methods=["POST", "GET"])
def admin_home():
    cursor.execute("SELECT * FROM ADMIN_USERS")
    data_admin = cursor.fetchall()

    username = request.form["username"]
    password = request.form["password"]

    for data in data_admin:
        if(data[0] == username and data[1] == password):
            return render_template("admin_home.html")
    return render_template("error.html", error_message = "Invalid Login")

@app.route("/add_faculty", methods=['POST', 'GET'])
def add_faculty():
    return render_template("add_faculty.html")

@app.route("/faculty_added", methods=["POST", "GET"])
def faculty_added():
    username = request.form["username"]
    password = request.form["password"]

    cursor.execute(f"INSERT INTO USERS VALUES ('{username}', '{password}')")
    cursor.execute("commit")
    return render_template("admin_home.html")
    
if __name__ == "__main__":
    app.run(debug=True)
