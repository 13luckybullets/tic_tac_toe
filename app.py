from flask import Flask
from config import Configuration
from flask_sqlalchemy import SQLAlchemy

# Creating Flsk app and connect to database

app = Flask(__name__, static_url_path='/static')
app.secret_key = "super secret key"

app.config.from_object(Configuration)
db = SQLAlchemy(app)