from init import db, ma
from marshmallow import fields

class Tank(db.Model):
    __tablename__ = "fishtank"

    tank_id = db.Column(db.Integer, primary_key=True)
    tank_name = db.Column(db.String, nullable=False)
    ideal_parameters = db.Column(db.String)
    room_location = db.Column(db.String)
    
    # Foreign Key
    created_by = db.Column(db.String, db.ForeignKey("users_id"), nullable=False) # This connects as a FK to the "users" table name from the user.py __tablename__ "users"

    user = db.relationship("User", back_populates='fishtank') # feature provided by SQLAlchemy - Lesson 2 week 5 35min


class TankSchema(ma.Schema):

    user = fields.Nested("UserSchema", only=["tank_id", "tank_name"] )

    class Meta:
        fields = ("id", "tank_name" "ideal_parameters", "room_location", "created_by")

tank_schema = TankSchema()
tank_schema = TankSchema(many=True)