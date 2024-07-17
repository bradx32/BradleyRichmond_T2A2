from datetime import timedelta

from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from flask_jwt_extended import create_access_token

from init import bcrypt, db
from models.user import User, user_schema

# the url_prefix provides the /auth prefix so it is added by default to the below auth_bp.route("/register"). 
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["POST"])
def register_user():
    try:
        # get the data from the body of the request
        body_data = request.get_json()

        # create an instance of the User model
        user = User(
            username=body_data.get("username"),
            role=body_data.get("role")
        )

        # extract the password from the body
        password = body_data.get("password")

        # hash the password
        if password: # user must inputa password
            user.password = bcrypt.generate_password_hash(password).decode("utf-8")

        # add the commit to the DB
        db.session.add(user)
        db.session.commit()

        # respond back
        return user_schema.dump(user), 201
    
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
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1)) # This will create the token and also set expiry of 1 day (24hrs).
        # respond back
        return {"username": user.username, "is_admin": user.is_admin, "token": token}
    
    # else
    else:
        # respond back with an error message
        return {"error": "Invalid username or password"}, 401