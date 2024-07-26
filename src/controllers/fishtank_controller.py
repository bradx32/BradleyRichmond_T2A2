from datetime import date

from flask import Blueprint, request

from init import db
from models.fishtank import Tank, tank_schema, tanks_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.maintenance_controller import maintenance_bp
from utils import authorise_as_admin

fishtanks_bp = Blueprint("fishtank", __name__, url_prefix="/fishtanks")
fishtanks_bp.register_blueprint(maintenance_bp, url_prefix="/<int:tank_id>/maintenance")

# /fishtanks - GET - fetch all fishtanks
# /fishtank/<id> - GET - fetch a single fishtank
# /fishtanks - POST - create a new fishtank
# /fishtanks/<id> - DELETE - delete a fishtank
# /fishtanks/<id> - PUT, PATCH - edit a fishtank

# /fishtanks - GET - fetch all fishtanks
@fishtanks_bp.route("/")
def get_all_fishtanks():
    stmt = db.select(Tank).order_by(Tank.date.desc()) # To order by date. Delete comment once date is added.
    fishtanks = db.session.scalars(stmt)
    return tanks_schema.dump(fishtanks)

# /cards/<id> - GET - fetch a single fishtank
@fishtanks_bp.route("/<int:tank_id>")
def get_fishtank(tank_id):
    stmt = db.select(Tank).filter_by(tank_id=tank_id)
    fishtank = db.session.scalar(stmt)
    if fishtank:
        return tank_schema.dump(fishtank)
    else:
        return {"error": f"Fishtank with id {tank_id} not found"}, 404
    
# /fishtanks - POST - create a new fishtank
@fishtanks_bp.route("/", methods=["POST"])
@jwt_required()
def create_fishtank():
    # get the data from the body of the request
    body_data = tank_schema.load(request.get_json())
    # create a new Tank model instance
    new_tank = Tank(
        tank_name=body_data.get("tank_name"),
        ideal_parameters=body_data.get("ideal_parameters"),
        room_location=body_data.get("room_location"),
        date=date.today(),
        created_by=get_jwt_identity()
    )
    # add and commit to DB
    db.session.add(new_tank)
    db.session.commit()
    # respond
    return tank_schema.dump(new_tank)


# /fishtanks/<id> - DELETE - delete a fishtank
@fishtanks_bp.route("/<int:tank_id>", methods=["DELETE"])
@jwt_required()
def delete_fishtank(tank_id):
    # check whether the user is an admin or not
    if not authorise_as_admin():
        return {"error": "Only an admin can perform this action."}, 403
    
    # fetch the fishtank from the database
    stmt = db.select(Tank).filter_by(tank_id=tank_id)
    tank = db.session.scalar(stmt)
    # if tank    
    if tank:

        # delete the fishtank
        db.session.delete(tank)
        db.session.commit()
        return {"message": f"Fishtank '{tank.tank_name}' deleted successfully"}
    # else
    else:
        # return error
        return {"error": f"Fishtank with id {tank_id} not found"}, 404



# /fishtanks/<id> - PUT, PATCH - edit a fishtank
@fishtanks_bp.route("/<int:tank_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_fishtank(tank_id):
    # get the data from the body of the request
    body_data = tank_schema.load(request.get_json(), partial=True)
    # get the tank from the database
    stmt = db.select(Tank).filter_by(tank_id=tank_id)
    tank = db.session.scalar(stmt)
    # if card
    if tank:
        # update the fields as required
        tank.tank_name = body_data.get("tank_name") or tank.tank_name
        tank.ideal_parameters =body_data.get("ideal_parameters") or tank.ideal_parameters
        tank.room_location = body_data.get("room_location") or tank.room_location
        tank.created_by = body_data.get("created_by") or tank.created_by
        # commit to the database
        db.session.commit()
        # return a response
        return tank_schema.dump(tank)
    # else
    else:
        # return an error
        return {"error": f"Fishtank with id {tank_id} not found"}, 404
    
