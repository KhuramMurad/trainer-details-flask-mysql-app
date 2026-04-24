
import os

from flask import Flask, render_template, request, url_for
from flask_mysqldb import MySQL
from datetime import datetime
from datetime import *
import time as t

def load_env_file(path=".env"):
    if not os.path.exists(path):
        return

    with open(path) as env_file:
        for line in env_file:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))

load_env_file()

app = Flask(__name__)
app.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST", "localhost")
app.config["MYSQL_USER"] = os.getenv("MYSQL_USER", "mysql_user")
app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD", "")
app.config["MYSQL_DB"] = os.getenv("MYSQL_DB", "alnafi")  

mysql = MySQL(app)

myhomepage = '!!!!!!!!!!!!!!!Landing Page!!!!!!!!!!!!!!!'

@app.route("/")
def get_home(): 
    return myhomepage

@app.route("/trainer")
def trainer():
    return render_template("trainer_details.html")

@app.route("/trainer_create", methods=["POST"])
def trainer_create():
    fname_data = request.form["fname"]
    lname_data = request.form["lname"]
    design_data = request.form["design"]
    course_data = request.form["course"]
    sql = "INSERT INTO trainer_details (fname, lname, design, course, datetime) VALUES (%s, %s, %s, %s, %s)"
    val = (fname_data, lname_data, design_data, course_data, datetime.now())

    cur = mysql.connection.cursor()
    cur.execute(sql, val)
    mysql.connection.commit()
    cur.close()

    return render_template("trainer_details.html")
    

 

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
