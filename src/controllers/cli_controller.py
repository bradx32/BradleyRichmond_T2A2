# CommandLineInterface_controllers

from flask import Blueprint

from init import db, bcrypt
from models.user import User

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

    db.session.commit()

    print("Tables seeded")