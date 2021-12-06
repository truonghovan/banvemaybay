from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:vantruong1705@localhost/banvemaybay?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.secret_key = "!@#$%^&*()(*&^%$#@#$%^&*("


db = SQLAlchemy(app=app)  #database in sql
admin = Admin(app=app, name="MANAGE TICKET", template_mode="bootstrap4") #tao page admin
my_login = LoginManager(app=app) #tao login


