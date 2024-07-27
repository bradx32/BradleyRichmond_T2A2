# BradleyRichmond_T2A2

### Requirements

## R1 Explain the problem that this app will solve, and explain how this app solves or addresses the problem.

#### Maintaining an aquarium or multiple fishtanks in a business or household can involve many tasks such as keeping track of the fish, managing the maintenance of each fishtank and ensuring the ideal water parameters for specific aquatic life. 

#### Whether you are an aquarium enthusiast, hobbyist or professional, keeping track of aquarium details manually can be cumbersome and time consuming. Small to large aquariums can benefit from a system to manage the information, reducing the risk of mismanagement which can lead to unhealthy living conditions, increased maintenance costs and potentially loss of aquatic life. 

#### The application provides a structured and efficient way to manage fishtanks or 'Aquarium' related data. It offers a centralised platform where users can Create, Read, Update and Delete data. The main features of the app are:

#### Fishtank Information tracking:
- Users can create, read, update, and delete fishtank records. Each fishtank record includes details such as the tank's name and its associated fish species.

#### Manage Fish Species:
- The app allows users to maintain a list of fish species within each tank, specifying attributes like species name and quantity. It also ensures that species are not mixed across multiple tanks, preventing cross breading between two similar species, removing the risk of undesired hybrid species.

#### Maintenance Logs:
- Users can keep detailed maintenance logs for each fishtank. These logs help track regular maintenance tasks, ensuring that all necessary care actions are performed timely and properly.

#### User Authentication and Authorization:
- The app includes a robust user authentication system with role-based access control. Admin users have privileges to manage all aspects of the system, including deleting users, which enhances security and ensures that only authorised persons can perform critical actions.

#### Data Validation and Integrity:
- The application enforces data validation rules to ensure the integrity and correctness of the information stored. For instance, it validates that the fish species names are not reused across tanks and that all required fields are correctly filled out.

### How does the app solve the problem?
#### The app provides a centralised system for managing fishtank data, enhancing the accuracy and efficiency by automating data entry and validation. It allows users to log maintenance activities and track fish species, promoting regular upkeep and a healthy aquatic environment. With security measures like user authentication and role based access control, the app ensures data integrity and system security. The API based architecture supports easy integration and scalability, making it suitable for both small and large fishtank/aquarium setups.



## R2 Describe the way tasks are allocated and tracked in your project.

### Trello Link: https://trello.com/b/mEjKnbcw/bradleyrichmondt2a2
- Visibility: Public

#### Trello has been used in the project to allocate and track tasks in the project. See the below screenshots for a snapshot of the progression and tasks planned for completion. The board is setup as a solo project although for a group it would have members assigned to different tasks, working on different branches and then pushing online, pulling to the main branch once approved. 

#### Trello Home
![Trello Board Home](Trello_Home.jpg)
#### Project Brief
![Project Brief](Trello_brief.jpg)
#### Project ERD with 2nd image update as ERD progressed.
![Project ERD](Trello_ERD.jpg)
#### Completed Checklist 1
![Checklist 1](Trello_Checklist1.jpg)
#### Models checklist
![Models Checklist](Trello_models.jpg)
#### Controllers checklist
![Controllers checklist](Trello_controllers.jpg)
#### Controller CRUD operations
![Controller CRUD](Trello_controller_CRUD.jpg)
#### Authorisation and Validation
![Auth & Validation](Trello_Auth_Validation.jpg)

#### The tasks are allocated and tracked by a structured API system. Each task corresponding to a specific endpoint and operation such as the CRUD operations for records in the database. 

#### Endpoints: Each task is assigned a specific endpoint in the API. For example, tasks related to managing users are handled by endpoints under /auth, while tasks related to fishtanks and fish species are managed under /fishtanks and /fishspecies.

#### HTTP Methods: Tasks are tracked by the HTTP methods used in the endpoints. For example, GET requests are used to retrieve the data, POST requests to create new records in the database, PUT or PATCH requests to update existing records, and a DELETE requests to remove records.

#### Blueprints and Routing: The project uses Flask Blueprints to organise related endpoints. For example, all of the authentication related tasks are grouped under the auth_bp Blueprint, which includes endpoints for users registration, login, and deletion.

#### Database Interactions: Tasks interact with the database using SQLAlchemy. For example, creating a new user involves adding a record to the User table, while deleting a user involves removing a record from the same table. Each operation is contained in a function that handles the required database transaction and commits the update.

#### Error Handling: The project includes error handling mechanisms to track and respond to issues. For example, attempts to create a user with a duplicate username are tracked and handled by checking for IntegrityError exceptions and returning appropriate error messages.

#### JWT Authentication: Tasks related to user authentication and authorisation are tracked using JWT tokens. This ensures that only authorised users (admin user), can perform certain actions, such as deleting a user or accessing specific data.

#### Validation and Security: Tasks also include validating input data and ensuring security. For example, user passwords are hashed before storage, and input data is validated using Marshmallow schemas to ensure it meets the required criteria.



## R3 List and explain the third-party services, packages and dependencies used in this app.

### The third-party services, packages and dependencies used in the application are Flask, SQLAlchemy, Mashmallow, Flask-JWT-Extended, Bcrypt, Psycopg2 and Trello (project management). These services collectively provide the essential functionalities needed to build and maintain the API.

#### Flask: The web application framework used to create the API. It provides the necessary tools and libraries to build the web application, handle the routing and request/response handling.

#### SQLAlchemy: An SQL toolkit and Object-Relational Mapping (ORM) library for Python. It allows for the manipulation of database records using Python objects, making the database interactions easier to manage.

#### Example of the SQLAlchemy used in the project user.py model. 
``` 
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False, default='standard')
    is_admin = db.Column(db.Boolean, default=False) 
```
#### Example of the SQLAlchemy used in the create_fish_species POST endpoint 
``` 
@fish_species_bp.route("/", methods=["POST"])
@jwt_required()
def create_fish_species():
    try:
        body_data = fish_species_schema.load(request.get_json())
        species = FishSpecies(
            species_name=body_data.get("species_name"),
            quantity=body_data.get("quantity"),
            tank_id=body_data.get("tank_id")
        )
        db.session.add(species)
        db.session.commit()
        return fish_species_schema.dump(species), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.FOREIGN_KEY_VIOLATION:
            return {"error": f"Invalid foreign key value for tank_id: {body_data.get('tank_id')}"}, 409
        else:
            return {"error": "An error occurred while creating the fish species"}, 500
```

#### Marshmallow: A library for object serialization and deserialization. It helps convert complex data types, such as objects, into native Python data types and vice versa. This is useful for validating and transforming input data for the API. See examples below of how Marshmallow is used in the project.

#### Marshmallow is used to define the schemas for the models, specifying how they should be serialised and deserialised. 
#### UserSchema
```
class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "role", "is_admin")
        ordered = True

user_schema = UserSchema()
users_schema = UserSchema(many=True)
```
#### FishTankSchema
```
class FishTankSchema(ma.Schema):
    user = fields.Nested("UserSchema", only=["id", "username"])

    class Meta:
        fields = ("tank_id", "tank_name", "user_id", "user")
        ordered = True

fishtank_schema = FishTankSchema()
fishtanks_schema = FishTankSchema(many=True)

```

#### Flask-JWT-Extended: A Flask extension for working with JSON Web Tokens (JWT). It facilitates the implementation of token-based authentication, allowing the user to securely access the API endpoints. 

#### As seen in the below code example from the API project, the route is protected by requiring a valid JWT token (@jwt_required()), while also requiring get_jwt_identity() to determine which user is making the request, eventually resulting in needing the admin token.

```
# /auth/<username> - DELETE - delete a user and requires admin
@auth_bp.route("/<username>", methods=["DELETE"])
@jwt_required()
def delete_user(username):
    # Extract the identity of the current user
    current_user_id = get_jwt_identity()
    
    # Fetch the current user from the database
    stmt = db.select(User).filter_by(id=current_user_id)
    current_user = db.session.scalar(stmt)
    
    # Check if the current user is an admin
    if not current_user or not current_user.is_admin:
        return {"error": "Access forbidden: Only an admin can delete a username"}, 403
    
    # Fetch the user to be deleted
    stmt = db.select(User).filter_by(username=username)
    user = db.session.scalar(stmt)

    if user:
        # Delete the user
        db.session.delete(user)
        db.session.commit()
        return {"message": f"User '{username}' deleted successfully"}

    # If user does not exist
    return {"error": f"User with username '{username}' not found"}, 404
```

#### Bcrypt: Is the password hashing library used to securely hash and check passwords. It ensures that user passwords are securely stored, reducing the risk of password related security breaches. See below how Bcrypt is used within the project

#### When a user registers, their password is hashed before being stored in the database. "bcrypt.generate_password_hash(password).decode("utf-8")". 
```
@auth_bp.route("/register", methods=["POST"])
def register_user():
    try:
        # get the data from the body of the request
        body_data = UserSchema().load(request.get_json())

        # create an instance of the User model
        user = User(
            username=body_data.get("username"),
            role=body_data.get("role")
        )

        # extract the password from the body
        password = body_data.get("password")

        # hash the password
        if password: # user must input a password
            user.password = bcrypt.generate_password_hash(password).decode("utf-8")

```

#### Psycopg2: A PostgreSQL database adapter for Python. It allows the API to interact with a PostgreSQL database, enabling the storage and retrieval of data.

#### Psycopg2 is used to catch and handle database integrity errors during user registration. Specifically, the IntegrityError and errorcodes from Psycopg2 are used to handle cases where a unique constraint is violated or a required field is missing:

#### The user registration error handling via integrity error and errorcodes.NOT_NULL_VIOLATION:
```
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

    # Error handling if violations occur
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": f"The column '{err.orig.diag.column_name}' is required"}, 409 # this will choose the column_name that is in violation eg. if no username provided it will say Username is required. Or password not required... etc.
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": "Username already in use"}, 409
```

#### Trello: Used as the project management tool to allocate and track tasks. Although a solo project, Trello has helped view what is needed to be completed in order, choose the next task in line and improve efficiency overall.


### R4 Explain the benefits and drawbacks of this app’s underlying database system.



### R5 Explain the features, purpose and functionalities of the object-relational mapping system (ORM) used in this app.



### R6 Design an entity relationship diagram (ERD) for this app’s database, and explain how the relations between the diagrammed models will aid the database design. 
#### This should focus on the database design BEFORE coding has begun, eg. during the project planning or design phase.




### R7 Explain the implemented models and their relationships, including how the relationships aid the database implementation.
#### This should focus on the database implementation AFTER coding has begun, eg. during the project development phase.




### R8 Explain how to use this application’s API endpoints. Each endpoint should be explained, including the following data for each endpoint:

- HTTP verb
- Path or route
- Any required body or header data
- Response
 



Design Requirements


The web server must:
function as intended
store data in a persistent data storage medium (eg. a relational database)
appropriately validate & sanitise any data it interacts with
use appropriate HTTP web request verbs - following REST conventions -  for various types of data manipulation 
cover the full range of CRUD functionality for data within the database
The database manipulated by the web server must accurately reflect the entity relationship diagram created for the Documentation Requirements.
The database tables or documents must be normalised
API endpoints must be documented in your readme
Endpoint documentation should include
HTTP request verbs
Required data where applicable 
Expected response data 
Authentication methods where applicable
 

Code Requirements

The web server must:
use appropriate functionalities or libraries from the relevant programming language in its construction
use appropriate model methods to query the database
catch errors and handle them gracefully 
returns appropriate error codes and messages to malformed requests
use appropriate functions or methods to sanitise & validate data
use D.R.Y coding principles
All queries to the database must be commented with an explanation of how they work and the data they are intended to retrieve