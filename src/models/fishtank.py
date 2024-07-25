from datetime import date

from init import db, ma
from marshmallow import fields, validates
from marshmallow.validate import Length, And, Regexp, OneOf # Regexp (regular expression), very handy tool for validation.
from marshmallow.exceptions import ValidationError

# VALID_PARAMETERS = ( "pH", "Ammonia", "Nitrite", "Nitrate", "GH", "KH") - Maybe delete as not needed anymore. See TankSchema

VALID_FISH_SPECIES = ( "Crimson Spot Rainbowfish", "Ornate Rainbowfish", "Empire Gudgeon", "Glass Fish", "Smelt", "Firetail Gudgeon")

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

    tank_name = fields.String(required=True, validate=And(
        Length(min=2, error="Tank name must be atleast 2 characters long"),
        Regexp('^[A-Za-z0-9 ]+$', error="Tank name must have alphanumeric characters only")        
    ))

    ideal_parameters = fields.String(required=True, validate=And(
        Length(min=3, error="Ideal paramaters must be atleast 3 character long"), # prevents short ideal parameters being input, user must atleast place 3 characters.
        Regexp('^[A-Za-z0-9 ]+$', error="Ideal paramaters must have alphanumeric characters only")        
    ))

    # ideal_parameters = fields.String(validate=OneOf(VALID_PARAMETERS))

    # Add tis to fish_species.py model
    # Fish species must be unique per tank, not able to split the same species to multiple tanks. This avoids cross breading into Hybrid fish species which are less desirable.
    @validates("fish_species")
    def validate_fish_species(self, value):
        # if trying to set the value of fish species into fishtank
        if value == VALID_FISH_SPECIES [1]:
            # check whether there is an existing fish_species in other fishtanks
            stmt = db.select(db.func.count()).select_from(Tank).filter_by(fish_species=VALID_FISH_SPECIES[1])
            count = db.session.scalar(stmt)
            # if it exists
            if count > 0:
                # throw error
                raise ValidationError("You already have this fish species")

    class Meta:
        fields = ("tank_id", "tank_name", "ideal_parameters", "room_location", "created_by", "date", "mlogs")
        ordered = True # ensures data fields are in the above order ^

tank_schema = TankSchema()
tanks_schema = TankSchema(many=True)