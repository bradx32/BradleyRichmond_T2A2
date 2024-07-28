from init import db, ma
from marshmallow import fields, validates, ValidationError
from marshmallow.validate import Length, Range

class FishSpecies(db.Model):
    __tablename__ = "fishspecies"

    species_id = db.Column(db.Integer, primary_key=True)
    species_name = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    tank_id = db.Column(db.Integer, db.ForeignKey('fishtank.tank_id'), nullable=False)

    # Define relationship with Tank model
    tank = db.relationship("Tank", back_populates="fish_species")


class FishSpeciesSchema(ma.Schema):
    tank = fields.Nested("TankSchema", only=["tank_id", "tank_name"])

    species_name = fields.String(required=True, validate=Length(min=2, error="Species name must be at least 2 characters long"))
    quantity = fields.Integer(required=True, validate=Range(min=1, error="Quantity must be at least 1"))

    @validates("species_name")
    def validate_fish_species(self, value):
        tank_id = self.context.get('tank_id')
        if not tank_id:
            raise ValidationError("Tank ID is required to validate fish species.")
        
        # check whether there is an existing fish_species in other fishtanks
        stmt = db.select(db.func.count()).select_from(FishSpecies).where(FishSpecies.tank_id == tank_id, FishSpecies.species_name == value)
        count = db.session.scalar(stmt)
        if count > 0:
            raise ValidationError("You already have this fish species in the tank")

    class Meta:
        fields = ("species_id", "species_name", "quantity", "tank_id")
        ordered = True

fish_species_schema = FishSpeciesSchema()
fish_species_schemas = FishSpeciesSchema(many=True)