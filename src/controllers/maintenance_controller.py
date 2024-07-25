from datetime import date

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.maintenance_log import MLog, mlog_schema, mlogs_schema
from models.fishtank import Tank  # Import the 'Tank' fishtank model to work with POST method to ensure tank_id exists.


maintenance_bp = Blueprint("maintenance", __name__, url_prefix="/<int:tank_id>/maintenance")


# /maintenance - GET - fetch all maintenance logs
@maintenance_bp.route("/", methods=["GET"])
def get_all_maintenance_logs():
    stmt = db.select(MLog).order_by(MLog.date.desc())
    maintenance_logs = db.session.scalars(stmt)
    return mlogs_schema.dump(maintenance_logs)

# /maintenance/<log_id> - GET - fetch a single maintenance log
@maintenance_bp.route("/<int:log_id>", methods=["GET"])
def get_maintenance_log(log_id):
    stmt = db.select(MLog).filter_by(log_id=log_id)
    maintenance_log = db.session.scalar(stmt)
    if maintenance_log:
        return mlog_schema.dump(maintenance_log)
    else:
        return {"error": f"Maintenance log with id {log_id} not found"}, 404




# /fishtanks/<int:tank_id>/maintenance - POST - create a new maintenance log
@maintenance_bp.route("/", methods=["POST"])
@jwt_required()
def create_maintenance_log(tank_id):
    # Get the data from the body of the request
    body_data = request.get_json()

    # Fetch the fishtank with the provided tank_id to ensure it exists
    stmt = db.select(Tank).filter_by(tank_id=tank_id) # Uses tank_id from URL
    tank = db.session.scalar(stmt)

    # if the tank exists
    if tank:
    # create a new MLog model instance
        new_log = MLog(
            description=body_data.get("description"),
            notes=body_data.get("notes"),
            date=date.today(),
            tank=tank, # Links the maintenance log to the fishtank object
            performed_by=get_jwt_identity()
        )
        # add and commit the session to DB
        db.session.add(new_log)
        db.session.commit()
        # return the created commit
        return mlog_schema.dump(new_log), 201
    #else 
    else:
        # return error that the tank does not exist. Use the same body_data.get as stmt.
        return {"error": f"Fishtank with id {tank_id} not found"}, 404
    


# /fishtanks/<int:tank_id>/maintenance/<int:log_id> - DELETE - delete a maintenance log
@maintenance_bp.route("/<int:log_id>", methods=["DELETE"])
@jwt_required()
def delete_maintenance_log(tank_id, log_id):
    # fetch the maintenance log from the database
    stmt = db.select(MLog).filter_by(log_id=log_id)
    maintenance_log = db.session.scalar(stmt)
    # if log exists
    if maintenance_log:
        # delete the maintenance log
        db.session.delete(maintenance_log)
        db.session.commit()
        # return some message
        return {"message": f"Maintenance log '{log_id}' deleted successfully"}
    else:
        # return error
        return {"error": f"Maintenance log with id {log_id} not found"}, 404



# /maintenance/<log_id> - PUT, PATCH - edit a maintenance log
@maintenance_bp.route("/<int:log_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_maintenance_log(tank_id, log_id):
    # get the data from the body of the request
    body_data = request.get_json()

    # get the maintenance log from the database
    stmt = db.select(MLog).filter_by(log_id=log_id)
    maintenance_log = db.session.scalar(stmt)
    
    # if log exists
    if maintenance_log:
        # update the fields as required
        maintenance_log.description = body_data.get("description") or maintenance_log.description
        maintenance_log.notes = body_data.get("notes") or maintenance_log.notes
        maintenance_log.date = body_data.get("date") or maintenance_log.date
        maintenance_log.tank_id = body_data.get("tank_id") or maintenance_log.tank_id
        maintenance_log.performed_by = body_data.get("performed_by") or maintenance_log.performed_by

        # commit to the database
        db.session.commit()

        # return a response
        return mlog_schema.dump(maintenance_log)
    else:
        # return an error
        return {"error": f"Maintenance log with id {log_id} not found"}, 404