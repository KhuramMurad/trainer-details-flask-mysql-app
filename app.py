import os
from datetime import datetime

from flask import Flask, render_template, request
from flask_mysqldb import MySQL
from dotenv import load_dotenv


# This line reads the .env file.
# The .env file keeps our database password out of the Python code.
load_dotenv()

# This creates our Flask website.
app = Flask(__name__)

# These lines tell Flask where the MySQL database is.
app.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST", "localhost")
app.config["MYSQL_USER"] = os.getenv("MYSQL_USER", "mysql_user")
app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD", "")
app.config["MYSQL_DB"] = os.getenv("MYSQL_DB", "alnafi")

# This connects our Flask website to MySQL.
mysql = MySQL(app)


@app.route("/")
def home():
    return "Welcome to the Trainer Details App"


@app.route("/trainer")
def trainer():
    # Show the HTML form.
    return render_template("trainer_details.html")


@app.route("/trainer_create", methods=["POST"])
def trainer_create():
    # Get the words typed by the user in the form.
    first_name = request.form["fname"]
    last_name = request.form["lname"]
    designation = request.form["design"]
    course = request.form["course"]

    # This is the MySQL command that saves one new trainer.
    sql = """
        INSERT INTO trainer_details (fname, lname, design, course, datetime)
        VALUES (%s, %s, %s, %s, %s)
    """

    # These values will go into the empty %s spaces above.
    data = (first_name, last_name, designation, course, datetime.now())

    # Send the command to MySQL.
    database = mysql.connection.cursor()
    database.execute(sql, data)
    mysql.connection.commit()
    database.close()

    return render_template("trainer_details.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
