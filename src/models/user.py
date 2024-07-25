from init import db, ma
from marshmallow import fields
from marshmallow.validate import Regexp, And, Length

class User(db.Model):
    # name of the table
    __tablename__ = "users"

    # attributes of the table
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # Foreign Key relationship bonding
    fishtanks = db.relationship('Tank', back_populates="user") # needs to have matching names with the same fields in fishtank.py, class Tank.
    mlogs = db.relationship("MLog", back_populates="user")


class UserSchema(ma.Schema):
    fishtank = fields.List(fields.Nested("TankSchema", exclude=["user"]))
    MLog = fields.List(fields.Nested('MLogSchema', exclude=["user"]))

    username = fields.String(required=True, validate=And(
        Length(min=3, error="Username must be atleast 3 characters long"),
        Regexp('^[A-Za-z0-9 ]+$', error="Username must have alphanumeric characters only")        
    ))

    # Password minimum eight characters, at least one letter and one number
    password = fields.String(required=True, validate=Regexp("^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$", error="Minimum six characters, at least one letter and one number"))

    class Meta:
        fields = ("id", "username", "password", "role", "is_admin")
        ordered = True



# to handle a single user object
user_schema = UserSchema()


# to handle a list of user objects
users_schema = UserSchema()