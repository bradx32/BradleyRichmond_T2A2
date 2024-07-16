from init import db, ma

class User(db.Model):
    # name of the table
    __tablename__ = "users"

    # attributes of the table
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "password", "role", "is_admin")



# to handle a single user object
user_schema = UserSchema(exclude=["password"])

# to handle a list of user objects
users_schema = UserSchema(many=True, exclude=["password"])