from datetime import date

from init import db, ma
from marshmallow import fields, validates
from marshmallow.validate import Length, And, Regexp # Regexp (regular expression), very handy tool for validation.
from marshmallow.exceptions import ValidationError


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
    fish_species = db.relationship("FishSpecies", back_populates="tank", cascade="all, delete")


class TankSchema(ma.Schema):

    user = fields.Nested("UserSchema", only=["id", "username"])
    mlogs = fields.List(fields.Nested("MLogSchema", exclude=["tank"])) # Excludes tank to prevent loop
    fish_species = fields.List(fields.Nested("FishSpeciesSchema", exclude=["tank"]))

    tank_name = fields.String(required=True, validate=And(
        Length(min=2, error="Tank name must be atleast 2 characters long"),
        Regexp('^[A-Za-z0-9 ]+$', error="Tank name must have alphanumeric characters only")        
    ))

    ideal_parameters = fields.String(required=True, validate=And(
        Length(min=3, error="Ideal paramaters must be atleast 3 character long"), error="Ideal paramaters must have atleast 3 characters")
    )


    class Meta:
        fields = ("tank_id", "tank_name", "ideal_parameters", "room_location", "created_by", "date", "mlogs") # adding fish_species is causing error. Unable to fix due to time constraints.
        ordered = True # ensures data fields are in the above order ^

tank_schema = TankSchema()
tanks_schema = TankSchema(many=True)

