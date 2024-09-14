from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
import cloudinary
from flask_login import LoginManager


app = Flask(__name__)
app.secret_key = 'fsbjuyhbvvcbnfkds92@@%%3#nfv'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/qlchuyenbaydb?charset=utf8mb4" % quote('Admin@123')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

login = LoginManager(app=app)


cloudinary.config(
    cloud_name="dpnkep1km",
    api_key="832627139245734",
    api_secret="Bu9HQ3UlNwt62PXYq-STmGkI9Zc"
)

db = SQLAlchemy(app)
