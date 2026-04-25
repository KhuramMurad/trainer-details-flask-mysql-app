"""
Trainer Details Flask MySQL App - Building Blocks

REQUIRED BUILDING BLOCKS:
1. Imports - Essential libraries for Flask, MySQL, and environment management
2. Environment Configuration - Loading .env file for secure database credentials
3. Flask App Initialization - Creating the Flask application instance
4. MySQL Configuration - Setting up database connection parameters
5. MySQL Connection - Establishing connection to the database
6. Routes - URL endpoints for handling requests (home, form display, form submission)

OPTIONAL BUILDING BLOCKS:
1. Debug Mode - Enables detailed error messages during development
2. Host Binding - Allows access from other machines on the network
3. Template Rendering - Using Jinja2 templates for HTML responses
4. Form Handling - Processing POST requests with user input validation
"""

# REQUIRED: Imports - Essential libraries
import os
from datetime import datetime

from flask import Flask, render_template, request, url_for
from flask_mysqldb import MySQL
from dotenv import load_dotenv


# REQUIRED: Environment Configuration
# This line reads the .env file.
# The .env file keeps our database password out of the Python code.
load_dotenv()

# REQUIRED: Flask App Initialization
# This creates our Flask website.
app = Flask(__name__)

# REQUIRED: MySQL Configuration
# These lines tell Flask where the MySQL database is.
app.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST", "localhost")
app.config["MYSQL_USER"] = os.getenv("MYSQL_USER", "mysql_user")
app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD", "")
app.config["MYSQL_DB"] = os.getenv("MYSQL_DB", "alnafi")

# REQUIRED: MySQL Connection
# This connects our Flask website to MySQL.
mysql = MySQL(app)


# REQUIRED: Routes - Home page
@app.route("/")
def home():
    return "Welcome to the Trainer Details App"


# REQUIRED: Routes - Form display
@app.route("/trainer")
def trainer():
    # Show the HTML form.
    return render_template("trainer_details.html")


# REQUIRED: Routes - Form submission and database insertion
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


# OPTIONAL: App Runner with debug mode and host binding
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
# This line reads the .env file.
# The .env file keeps our database password out of the Python code.
load_dotenv()

# REQUIRED: Flask App Initialization
# This creates our Flask website.
app = Flask(__name__)

# REQUIRED: MySQL Configuration
# These lines tell Flask where the MySQL database is.
app.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST", "localhost")
app.config["MYSQL_USER"] = os.getenv("MYSQL_USER", "mysql_user")
app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD", "")
app.config["MYSQL_DB"] = os.getenv("MYSQL_DB", "alnafi")

# REQUIRED: MySQL Connection
# This connects our Flask website to MySQL.
mysql = MySQL(app)


# REQUIRED: Routes - Home page
@app.route("/")
def home():
    return "Welcome to the Trainer Details App"


# REQUIRED: Routes - Form display
@app.route("/trainer")
def trainer():
    # Show the HTML form.
    return render_template("trainer_details.html")


# REQUIRED: Routes - Form submission and database insertion
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


# OPTIONAL: App Runner with debug mode and host binding
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
