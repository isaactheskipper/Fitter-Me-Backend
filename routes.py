from flask import Flask, request, jsonify, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from config import db
from models import User, UserDetail, Role, Level, Achievement, Gender, Workout, WorkoutDone


routes_bp = Blueprint('routes', __name__)

# Create a new user
@routes_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    new_user = User(username=data['username'], email=data['email'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201

# Get all users
@routes_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{ "id": user.id, "username": user.username, "email": user.email } for user in users])

# Get a single user by ID
@routes_bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({ "id": user.id, "username": user.username, "email": user.email })

# Update a user
@routes_bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    data = request.get_json()
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    if 'password' in data:
        user.password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    db.session.commit()
    return jsonify({"message": "User updated successfully"})

# Delete a user
@routes_bp.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"})

@routes_bp.route('/user-details', methods=['POST'])
def add_user_details():
    data = request.get_json()
    if not User.query.get(data["user_id"]):
        return jsonify({"error": "User not found"}), 404

    new_details = UserDetail(
        user_id=data["user_id"],
        first_name=data["first_name"],
        last_name=data["last_name"],
        birthdate=data["birthdate"],
        current_weight=data["current_weight"],
        target_weight=data["target_weight"],
        height=data["height"],
        program_duration=data["program_duration"],
        role_id=data["role_id"],
        achievement_id=data.get("achievement_id"),
        gender_id=data["gender_id"],
    )
    db.session.add(new_details)
    db.session.commit()
    return jsonify({"message": "User details added successfully"}), 201

@routes_bp.route('/user-details', methods=['GET'])
def get_all_user_details():
    details = UserDetail.query.all()
    return jsonify([
        {
            "user_id": d.user_id,
            "first_name": d.first_name,
            "last_name": d.last_name,
            "birthdate": str(d.birthdate),
            "current_weight": float(d.current_weight),
            "target_weight": float(d.target_weight),
            "height": float(d.height),
            "program_duration": d.program_duration,
            "role_id": d.role_id,
            "achievement_id": d.achievement_id,
            "gender_id": d.gender_id
        } for d in details
    ])


### ROLES ###
@routes_bp.route('/roles', methods=['POST'])
def create_role():
    data = request.get_json()
    new_role = Role(name=data["name"])
    db.session.add(new_role)
    db.session.commit()
    return jsonify({"message": "Role created successfully", "role_id": new_role.id}), 201

@routes_bp.route('/roles', methods=['GET'])
def get_roles():
    roles = Role.query.all()
    return jsonify([{ "id": role.id, "name": role.name } for role in roles])


### LEVELS ###
@routes_bp.route('/levels', methods=['POST'])
def create_level():
    data = request.get_json()
    new_level = Level(name=data["name"])
    db.session.add(new_level)
    db.session.commit()
    return jsonify({"message": "Level created successfully", "level_id": new_level.id}), 201

@routes_bp.route('/levels', methods=['GET'])
def get_levels():
    levels = Level.query.all()
    return jsonify([{ "id": level.id, "name": level.name } for level in levels])


### ACHIEVEMENTS ###
@routes_bp.route('/achievements', methods=['POST'])
def create_achievement():
    data = request.get_json()
    new_achievement = Achievement(star_number=data["star_number"], number_of_videos=data["number_of_videos"])
    db.session.add(new_achievement)
    db.session.commit()
    return jsonify({"message": "Achievement created successfully", "achievement_id": new_achievement.id}), 201

@routes_bp.route('/achievements', methods=['GET'])
def get_achievements():
    achievements = Achievement.query.all()
    return jsonify([
        { "id": a.id, "star_number": a.star_number, "number_of_videos": a.number_of_videos } for a in achievements
    ])


### GENDERS ###
@routes_bp.route('/genders', methods=['POST'])
def create_gender():
    data = request.get_json()
    new_gender = Gender(name=data["name"])
    db.session.add(new_gender)
    db.session.commit()
    return jsonify({"message": "Gender created successfully", "gender_id": new_gender.id}), 201

@routes_bp.route('/genders', methods=['GET'])
def get_genders():
    genders = Gender.query.all()
    return jsonify([{ "id": gender.id, "name": gender.name } for gender in genders])


### WORKOUTS ###
@routes_bp.route('/workouts', methods=['POST'])
def create_workout():
    data = request.get_json()
    new_workout = Workout(
        name=data["name"],
        duration=data["duration"],
        calories_burned=data["calories_burned"],
        description=data["description"],
        level_id=data["level_id"],
        sets=data["sets"]
    )
    db.session.add(new_workout)
    db.session.commit()
    return jsonify({"message": "Workout created successfully", "workout_id": new_workout.id}), 201

@routes_bp.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return jsonify([
        { "id": w.id, "name": w.name, "duration": w.duration, "calories_burned": float(w.calories_burned), "description": w.description, "level_id": w.level_id, "sets": w.sets }
        for w in workouts
    ])


### WORKOUTS DONE ###
@routes_bp.route('/workouts-done', methods=['POST'])
def create_workout_done():
    data = request.get_json()
    new_workout_done = WorkoutDone(
        user_id=data["user_id"],
        workout_id=data["workout_id"],
        video_path=data.get("video_path"),
        workout_date=data["workout_date"]
    )
    db.session.add(new_workout_done)
    db.session.commit()
    return jsonify({"message": "Workout done added successfully", "workout_done_id": new_workout_done.id}), 201

@routes_bp.route('/workouts-done', methods=['GET'])
def get_workouts_done():
    workouts_done = WorkoutDone.query.all()
    return jsonify([
        {
            "id": wd.id,
            "user_id": wd.user_id,
            "workout_id": wd.workout_id,
            "video_path": wd.video_path,
            "workout_date": str(wd.workout_date)
        } for wd in workouts_done
    ])

# if __name__ == '__main__':
#     app.run(debug=True)