from datetime import datetime
from flask_sqlalchemy import SQLAlchemy 
from server import app

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db = SQLAlchemy(app)
from events import *
from all_user import *
from LoadUserFromCSV import *
def create_db():
    db.drop_all()
    db.create_all()
    loadcsv()