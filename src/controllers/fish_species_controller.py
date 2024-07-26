from flask import Blueprint, request

from init import db
from models.fish_species import FishSpecies, fish_species_schema, fish_species_schemas
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from utils import authorise_as_admin


fish_species_bp = Blueprint("fish_species", __name__, url_prefix="/fish_species")

# /fish_species - GET - all fish species
@fish_species_bp.route("/")
@jwt_required()
def get_all_fish_species():
    stmt = db.select(FishSpecies)
    species = db.session.scalars(stmt).all()
    return fish_species_schemas.dump(species)

# /fish_species/<id> - GET - fish species by id
@fish_species_bp.route("/<int:species_id>")
@jwt_required()
def get_fish_species(species_id):
    stmt = db.select(FishSpecies).filter_by(species_id=species_id)
    species = db.session.scalar(stmt)
    if species:
        return fish_species_schema.dump(species)
    else:
        return {"error": f"Fish species with id {species_id} not found"}, 404

# /fish_species - POST - Create a new fish species
@fish_species_bp.route("/", methods=["POST"])
@jwt_required()
def create_fish_species():
    try:
        # get the data from the body of the request
        body_data = fish_species_schema.load(request.get_json())

        # create a new Tank model instance
        species = FishSpecies(
            species_name=body_data.get("species_name"),
            quantity=body_data.get("quantity"),
            tank_id=body_data.get("tank_id")
        )
        # add and commit to DB
        db.session.add(species)
        db.session.commit()

        # Return the newly created species data as a response
        return fish_species_schema.dump(species)
    
    # Handle integrity errors if foreign key violation occurs
    except IntegrityError as err:
        # Check if the error is due to a foreign key violation
        if err.orig.pgcode == errorcodes.FOREIGN_KEY_VIOLATION:
            # Return a 409 'conflict' error with a message
            return {"error": f"Invalid foreign key value for tank_id: {body_data.get('tank_id')}"}, 409
        
        # Handle any other types of integrity errors
        else:
            # Return a generic 500 Internal Server Error message
            return {"error": "An error occurred while creating the fish species"}, 500



# /fish_species - PUT/PATCH - Update a fish species
@fish_species_bp.route("/<int:species_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_fish_species(species_id):
    # get the data from the body of the request
    body_data = fish_species_schema.load(request.get_json(), partial=True)

    # get the fishspecies from the database
    stmt = db.select(FishSpecies).filter_by(species_id=species_id)
    species = db.session.scalar(stmt)
    if species:
        species.species_name = body_data.get("species_name") or species.species_name
        species.quantity = body_data.get("quantity") or species.quantity
        species.tank_id = body_data.get("tank_id") or species.tank_id

        # commit to the database
        db.session.commit()

        # return a response
        return fish_species_schema.dump(species)
    else:
        # return an error
        return {"error": f"Fish species with id {species_id} not found"}, 404


# /fish_species/<id> - DELETE - Delete a fish species
@fish_species_bp.route("/<int:species_id>", methods=["DELETE"])
@jwt_required()
def delete_fish_species(species_id):
    # Check whether the user is an admin
    if not authorise_as_admin():
        return {"error": "Only an admin can perform this action."}, 403

    stmt = db.select(FishSpecies).filter_by(species_id=species_id)
    species = db.session.scalar(stmt)

    if species:
        db.session.delete(species)
        db.session.commit()

        return {"message": f"Fish species '{species.species_name}' deleted successfully"}
    else:
        return {"error": f"Fish species with id {species_id} not found"}, 404