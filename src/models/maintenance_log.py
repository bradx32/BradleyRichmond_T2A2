from init import db, ma
from marshmallow import fields

class MLog(db.Model):
    __tablename__ = "mlog"

    log_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    notes = db.Column(db.String)
    date = db.Column(db.Date) # Created Date

    tank_id = db.Column(db.Integer, db.ForeignKey("fishtank.tank_id"), nullable=False)
    performed_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("User", back_populates="mlogs")
    tank = db.relationship("Tank", back_populates="mlogs")


class MLogSchema(ma.Schema):
    user = fields.Nested("UserSchema", only=["id", "username"])
    tank = fields.Nested("TankSchema", exclude=["mlogs"])

    class Meta:
        fields = ("log_id", "description", "notes", "date", "tank", "performed_by")
        ordered = True # ensures data fields are in the above order ^

mlog_schema = MLogSchema()
mlogs_schema = MLogSchema(many=True)