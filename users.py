# users.py

from flask import abort, make_response

from config import db
from models import User, Trail, user_schema, users_schema

def read_all():
	users = User.query.all()
	return users_schema.dump(users)

def read_one(UserID):
    user = User.query.get(UserID)

    if user is not None:
        return user_schema.dump(user)
    else:
        abort(
            404, f"User with ID {UserID} not found"
        )


def update(UserID, user):
    existing_user = User.query.get(UserID)

    if existing_user:
       update_user = user_schema.load(user, session=db.session)
       existing_user.Email_Address = update_user.Email_Address
       existing_user.Role = update_user.Role
        
       db.session.merge(existing_user)
       db.session.commit()
       return user_schema.dump(existing_user), 201
    else:
       abort(404, f"User with id {UserID} not found")
		

def delete(UserID):
    existing_user = User.query.get(UserID)
    if existing_user:
        db.session.delete(existing_user)
            
        db.session.commit()

        return make_response(f"User {UserID} successfully deleted", 200)
		
    else:
	    abort(404, f"User with id {UserID} not found")


def create(user): 
    user_id = user.get("UserID")
    existing_user = User.query.filter(User.UserID == user_id).one_or_none()
 
    if existing_user is None:
        new_user = user_schema.load(user, session=db.session)
        db.session.add(new_user)
        db.session.commit()
        return user_schema.dump(new_user), 201
    else:
        abort(406, f"User with id {user_id} already exists")