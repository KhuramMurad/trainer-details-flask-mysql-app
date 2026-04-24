import os
from datetime import datetime

from flask import Flask, render_template, request
from flask_mysqldb import MySQL


def load_env_file(file_path=".env"):
    """Read database settings from a .env file, if that file exists."""
    if not os.path.exists(file_path):
        return

    with open(file_path) as env_file:
        for line in env_file:
            clean_line = line.strip()

            # Skip empty lines and notes that start with #.
            if not clean_line or clean_line.startswith("#") or "=" not in clean_line:
                continue

            key, value = clean_line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


# Load settings like MYSQL_HOST and MYSQL_PASSWORD from the .env file.
load_env_file()

# Create the Flask app.
app = Flask(__name__)

# Tell Flask how to connect to the MySQL database.
# If a setting is missing from .env, Flask will use the default value.
app.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST", "localhost")
app.config["MYSQL_USER"] = os.getenv("MYSQL_USER", "mysql_user")
app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD", "")
app.config["MYSQL_DB"] = os.getenv("MYSQL_DB", "alnafi")

# Connect Flask to MySQL.
mysql = MySQL(app)

home_page_message = "Welcome to the Trainer Details App"


@app.route("/")
def home():
    """Show a simple home page message."""
    return home_page_message


@app.route("/trainer")
def show_trainer_form():
    """Show the form where a user can type trainer details."""
    return render_template("trainer_details.html")


@app.route("/trainer_create", methods=["POST"])
def save_trainer_details():
    """Save the trainer form data into the MySQL database."""
    first_name = request.form["fname"]
    last_name = request.form["lname"]
    designation = request.form["design"]
    course = request.form["course"]

    insert_query = """
        INSERT INTO trainer_details (fname, lname, design, course, datetime)
        VALUES (%s, %s, %s, %s, %s)
    """
    trainer_data = (
        first_name,
        last_name,
        designation,
        course,
        datetime.now(),
    )

    # A cursor is like a helper that sends commands to MySQL.
    cursor = mysql.connection.cursor()
    cursor.execute(insert_query, trainer_data)
    mysql.connection.commit()
    cursor.close()

    return render_template("trainer_details.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
