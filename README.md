# Trainer Details Flask MySQL App

A small Flask app that stores trainer details in a MySQL database.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a local `.env` file or export these environment variables:

```bash
MYSQL_HOST=localhost
MYSQL_USER=mysql_user
MYSQL_PASSWORD=your-password
MYSQL_DB=alnafi
```

Run the app:

```bash
python app.py
```

Open `http://127.0.0.1:5000/trainer`.
