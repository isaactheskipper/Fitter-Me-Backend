from config import db
from flask_sqlalchemy import SQLAlchemy
# import bcrypt



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    # def set_password(self, password):
    #     self.password = bcrypt.generate_password_hash(password).decode('utf-8')
