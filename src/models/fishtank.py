from datetime import date

from init import db, ma
from marshmallow import fields

class Tank(db.Model):
    __tablename__ = "fishtank"

    tank_id = db.Column(db.Integer, primary_key=True)
    tank_name = db.Column(db.String, nullable=False)
    ideal_parameters = db.Column(db.String)
    room_location = db.Column(db.String)
    date = db.Column(db.Date, default=date.today)

    # Foreign Key 
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # This connects as a FK to the "users" table name from the user.py __tablename__ "users"

    # Define relationship with User model
    user = db.relationship("User", back_populates='fishtanks') # feature provided by SQLAlchemy - Lesson 2 week 5 35min
    mlogs = db.relationship("MLog", back_populates="tank", cascade="all, delete") # cascade will delete the maintenance log once the tank is deleted.


class TankSchema(ma.Schema):

    user = fields.Nested("UserSchema", only=["id", "username"])
    mlogs = fields.List(fields.Nested("MLogSchema", exclude=["tank"])) # Excludes tank to prevent loop

    class Meta:
        fields = ("tank_id", "tank_name", "ideal_parameters", "room_location", "created_by", "date", "mlogs")
        ordered = True # ensures data fields are in the above order ^

tank_schema = TankSchema()
tanks_schema = TankSchema(many=True)