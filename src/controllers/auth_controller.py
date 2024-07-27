from datetime import timedelta

from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from init import bcrypt, db
from models.user import User, user_schema, UserSchema

# the url_prefix provides the /auth prefix so it is added by default to the below auth_bp.route("/register"). 
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["POST"])
def register_user():
    try:
        # get the data from the body of the request
        body_data = UserSchema().load(request.get_json())

        # create an instance of the User model
        user = User(
            username=body_data.get("username"),
            role=body_data.get("role")
        )

        # extract the password from the body
        password = body_data.get("password")

        # hash the password
        if password: # user must input a password
            user.password = bcrypt.generate_password_hash(password).decode("utf-8")

        # add and commit the user to the DB
        db.session.add(user)
        db.session.commit()

        # respond back
        return user_schema.dump(user)
    
    # Error handling if violations occur
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": f"The column '{err.orig.diag.column_name}' is required"}, 409 # this will choose the column_name that is in violation eg. if no username provided it will say Username is required. Or password not required... etc.
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": "Username already in use"}, 409
        

@auth_bp.route("/login", methods=["POST"])
def login_user():
    # get the data from the body of the request
    body_data = request.get_json()
    # find the user in DB with that email address
    stmt = db.select(User).filter_by(username=body_data.get("username"))
    user = db.session.scalar(stmt)
    # if user exists and password is correct
    if user and bcrypt.check_password_hash(user.password, body_data.get("password")):
        # create jwt
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1)) # This will create the token and set expiry of the token as 1 day (24hrs).
        # respond back
        return {"username": user.username, "is_admin": user.is_admin, "token": token}
    
    # else
    else:
        # respond back with an error message
        return {"error": "Invalid username or password"}, 401
    

# /auth/users/users_id
@auth_bp.route("/users/<int:user_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_user(user_id):
    # get the fields from body of the request
    body_data = UserSchema().load(request.get_json(), partial=True)
    password = body_data.get("password")
    # Fetch the user from the database using the provided user ID
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    # if user exists
    if user:
        # update the fields
        user.username = body_data.get("username") or user.username
        # user.password = <hashed-password> or user.password
        if password:
            user.password = bcrypt.generate_password_hash(password).decode("utf-8")
        # commit to the DB
        db.session.commit()
        # return a response
        return user_schema.dump(user)
    # else
    else:
        # return an error
        return {"error": "user does not exist"}



# /auth/<username> - DELETE - delete a user and requires admin
@auth_bp.route("/<username>", methods=["DELETE"])
@jwt_required()
def delete_user(username):
    # Extract the identity of the current user
    current_user_id = get_jwt_identity()
    
    # Fetch the current user from the database
    stmt = db.select(User).filter_by(id=current_user_id)
    current_user = db.session.scalar(stmt)
    
    # Check if the current user is an admin
    if not current_user or not current_user.is_admin:
        return {"error": "Access forbidden: Only an admin can delete a username"}, 403
    
    # Fetch the user to be deleted
    stmt = db.select(User).filter_by(username=username)
    user = db.session.scalar(stmt)

    if user:
        # Delete the user
        db.session.delete(user)
        db.session.commit()
        return {"message": f"User '{username}' deleted successfully"}

    # If user does not exist
    return {"error": f"User with username '{username}' not found"}, 404