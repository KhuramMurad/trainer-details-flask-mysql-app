# Trainer Details Flask MySQL App

A small Flask app that stores trainer details in a MySQL database.

## Project Setup

### System Dependencies

Before installing Python packages, you need to install system dependencies required for `Flask-MySQLdb` (which depends on `mysqlclient`).

#### On Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install build-essential python3-dev libmysqlclient-dev pkg-config
```

#### On Linux (RHEL/CentOS/Fedora):
```bash
sudo yum install gcc python3-devel mysql-devel redhat-rpm-config  # or dnf on newer versions
```

#### On Windows:
1. Download and install MySQL Connector/C from the official MySQL website: https://dev.mysql.com/downloads/connector/c/
2. Ensure the MySQL bin directory is in your PATH, or set environment variables:
   - `MYSQLCLIENT_CFLAGS` to include paths
   - `MYSQLCLIENT_LDFLAGS` to link libraries
   Alternatively, use a pre-compiled wheel or consider using `pymysql` instead of `mysqlclient` for easier installation.

If you encounter issues installing `mysqlclient`, you can modify `requirements.txt` to use `pymysql` instead:
- Replace `Flask-MySQLdb` with `Flask-MySQLdb[pymysql]` or use `pymysql` directly and update your Flask app configuration.

### Python Environment Setup

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## MySQL Server Setup on Ubuntu Server VM

This project expects a MySQL database to already exist. In this setup, MySQL runs on a separate Ubuntu Server VM, and the Flask app connects to that VM over the network.

### 1. Install MySQL Server on the Ubuntu VM

SSH into your Ubuntu Server VM:

```bash
ssh username@your-ubuntu-vm-ip
```

Install MySQL:

```bash
sudo apt update
sudo apt install mysql-server -y
```

Start and enable MySQL:

```bash
sudo systemctl start mysql
sudo systemctl enable mysql
sudo systemctl status mysql
```

Run the MySQL security setup:

```bash
sudo mysql_secure_installation
```

You can choose a strong root password and answer the prompts based on your needs. For beginners, it is usually safe to remove anonymous users, disallow remote root login, remove the test database, and reload privilege tables.

### 2. Allow MySQL to Accept Remote Connections

By default, MySQL often listens only on `localhost`. Because the Flask app may run outside the MySQL VM, update the MySQL bind address.

Open the MySQL config file:

```bash
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
```

Find this line:

```ini
bind-address = 127.0.0.1
```

Change it to:

```ini
bind-address = 0.0.0.0
```

Restart MySQL:

```bash
sudo systemctl restart mysql
```

If UFW firewall is enabled on the Ubuntu VM, allow MySQL traffic from the machine that runs the Flask app:

```bash
sudo ufw allow from YOUR_FLASK_APP_SERVER_IP to any port 3306
sudo ufw status
```

For a local lab only, you can allow port `3306` generally:

```bash
sudo ufw allow 3306/tcp
```

For production, avoid opening MySQL to the whole internet. Restrict access to trusted IP addresses only.

### 3. Create the Database, User, and Table

Log in to MySQL on the Ubuntu VM:

```bash
sudo mysql
```

Create the project database:

```sql
CREATE DATABASE alnafi;
```

Create a MySQL user for the Flask app. Replace `strong_password_here` with your own strong password.

If the Flask app runs from another server or your laptop, use `%` to allow network access:

```sql
CREATE USER 'mysql_user'@'%' IDENTIFIED BY 'strong_password_here';
```

If the Flask app runs on the same Ubuntu VM as MySQL, use `localhost` instead:

```sql
CREATE USER 'mysql_user'@'localhost' IDENTIFIED BY 'strong_password_here';
```

Grant the user access to the database:

```sql
GRANT ALL PRIVILEGES ON alnafi.* TO 'mysql_user'@'%';
FLUSH PRIVILEGES;
```

If you created the user with `localhost`, run this grant instead:

```sql
GRANT ALL PRIVILEGES ON alnafi.* TO 'mysql_user'@'localhost';
FLUSH PRIVILEGES;
```

Select the database:

```sql
USE alnafi;
```

Create the table used by the Flask form:

```sql
CREATE TABLE trainer_details (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fname VARCHAR(100) NOT NULL,
    lname VARCHAR(100) NOT NULL,
    design VARCHAR(100) NOT NULL,
    course VARCHAR(100) NOT NULL,
    datetime DATETIME NOT NULL
);
```

Check that the table exists:

```sql
SHOW TABLES;
DESCRIBE trainer_details;
```

Exit MySQL:

```sql
EXIT;
```

## Flask Environment Configuration

Create a local `.env` file in the project folder, or export these environment variables:

```bash
MYSQL_HOST=your-ubuntu-vm-ip
MYSQL_USER=mysql_user
MYSQL_PASSWORD=strong_password_here
MYSQL_DB=alnafi
```

If MySQL and Flask are running on the same VM, you can use:

```bash
MYSQL_HOST=localhost
```

The `.env` file should not be committed to GitHub because it contains your database password. Use `.env.example` as the public template.

## Run the App

Run the app:

```bash
python app.py
```

Open `http://127.0.0.1:5000/trainer`.

Because the app starts with `host='0.0.0.0'`, you can also open it from another machine on the same network:

```text
http://YOUR_FLASK_APP_SERVER_IP:5000/trainer
```

## Quick Troubleshooting

If the app cannot connect to MySQL, check these items:

- The MySQL VM is running.
- MySQL service is active: `sudo systemctl status mysql`.
- The `.env` values match the database host, username, password, and database name.
- Port `3306` is open only for the Flask app machine.
- MySQL `bind-address` is set correctly.
- The MySQL user host matches your setup, for example `'mysql_user'@'%'` for remote access or `'mysql_user'@'localhost'` for same-server access.
