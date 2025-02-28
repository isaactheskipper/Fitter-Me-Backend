from config import db
from flask_sqlalchemy import SQLAlchemy
# import bcrypt



class UserDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    current_weight = db.Column(db.Numeric(5,2), nullable=False)
    target_weight = db.Column(db.Numeric(5,2), nullable=False)
    height = db.Column(db.Numeric(5,2), nullable=False)
    program_duration = db.Column(db.Integer, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    achievement_id = db.Column(db.Integer, db.ForeignKey('achievement.id'), nullable=True)
    gender_id = db.Column(db.Integer, db.ForeignKey('gender.id'), nullable=False)
    created_when = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    user = db.relationship('User', back_populates='user_details')
    role = db.relationship('Role', back_populates='users')
    achievement = db.relationship('Achievement', back_populates='users')
    gender = db.relationship('Gender', back_populates='users')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    user_details = db.relationship('UserDetail', back_populates='user', uselist=False)
    workouts_done = db.relationship('WorkoutDone', back_populates='user')

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    users = db.relationship('UserDetail', back_populates='role')

class Level(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    workouts = db.relationship('Workout', back_populates='level')

class Achievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    star_number = db.Column(db.Integer, nullable=False)
    number_of_videos = db.Column(db.Integer, nullable=False)
    users = db.relationship('UserDetail', back_populates='achievement')

class Gender(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    users = db.relationship('UserDetail', back_populates='gender')



class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    calories_burned = db.Column(db.Numeric(6,2), nullable=False)
    description = db.Column(db.Text, nullable=False)
    level_id = db.Column(db.Integer, db.ForeignKey('level.id'), nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    level = db.relationship('Level', back_populates='workouts')
    workouts_done = db.relationship('WorkoutDone', back_populates='workout')

class WorkoutDone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'), nullable=False)
    video_path = db.Column(db.String(255), nullable=True)
    workout_date = db.Column(db.Date, nullable=True)
    user = db.relationship('User', back_populates='workouts_done')
    workout = db.relationship('Workout', back_populates='workouts_done')
