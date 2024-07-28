# CommandLineInterface_controllers
from datetime import date

from flask import Blueprint

from init import db, bcrypt
from models.user import User
from models.fishtank import Tank
from models.maintenance_log import MLog
from models.fish_species import FishSpecies

db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_tables():
    db.create_all()
    print("Tables created")

@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables dropped")


@db_commands.cli.command("seed")
def seed_tables():
    # create a list of User instances
    users = [
        User(
            username="aquariumadmin",
            password=bcrypt.generate_password_hash("123456789").decode("utf-8"),
            role="admin",
            is_admin=True
        ),
        User(
            username="User 1",
            password=bcrypt.generate_password_hash("123456").decode("utf-8"),
            role="standard_user"
        )
    ]

    db.session.add_all(users)

    # Create a list of Tank instances
    fishtank = [
        Tank(
            tank_name="Australian Local Freshwater Fish",
            ideal_parameters="pH: 7, Ammonia: 0ppm, Nitrate: 0.20ppm, GH: 3-4 drops",
            room_location="Living room",
            user=users[0] # this makes the first User in the seed which is the 'aquariumadmin', the creator of the 'fishtank'.
        ),
        Tank(
            tank_name="Australian North Queensland Freshwater Fish",
            ideal_parameters="pH: 6-7.5, Ammonia: 0ppm, Nitrate: 0.20ppm, GH: 3 drops",
            room_location="Living room",
            user=users[0]
        ),
        Tank(
            tank_name="Australian Northbrook Creek Freshwater Fish",
            ideal_parameters="pH: 6-7.5, Ammonia: 0ppm, Nitrate: 0.10ppm, GH: 2 drops",
            room_location="Garage",
            user=users[1]
        ),
        Tank(
            tank_name="Australian Tin Can Bay Freshwater Fish",
            ideal_parameters="pH: 6-6.5, Ammonia: 0ppm, Nitrate: 0.10ppm, GH: 2 drops",
            room_location="Garage",
            user=users[1]
        )
    ]

    db.session.add_all(fishtank)

    db.session.commit()

    # Create a list of MLog instances
    maintenance = [
        MLog(
            description="Tank cleaned and water tested",
            notes="Results of tests: pH: 7.0, Ammonia: 0.05ppm",
            date=date.today(),
            user=users[1],
            tank=fishtank[0]
        ),
        MLog(
            description="Protein feed",
            notes="1 x Bloodworms Block, all fish fed",
            date=date.today(),
            user=users[0],
            tank=fishtank[1]
        ),
    ]

    db.session.add_all(maintenance)

    db.session.commit()
    
    # Create a list of FishSpecies instances
    fish_species = [
        FishSpecies(
            species_name="Crimson Spot Rainbow - Kangaroo Creek",
            quantity=21,
            tank_id=fishtank[0].tank_id
        ),
        FishSpecies(
            species_name="Pacific Blue Eye - Coombabah Creek",
            quantity=12,
            tank_id=fishtank[1].tank_id
        )
    ]

    db.session.add_all(fish_species)

    db.session.commit()

    print("Tables seeded")