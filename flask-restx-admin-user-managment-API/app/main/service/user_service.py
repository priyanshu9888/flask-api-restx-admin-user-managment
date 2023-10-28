import re

import uuid
import datetime

from flask import Response, request


from app.main import db
from app.main.model import user
from app.main.model.user import User
from typing import Dict, Tuple


def save_new_user(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    user = User.query.filter_by(email=data['email']).first()
    print(data)
    if not user:
        new_user = User(
            public_id=str(uuid.uuid4()),
            email=data['email'],
            username=data['username'],
            password=data['password'],
            org_name=data['org_name'],
            registered_on=datetime.datetime.utcnow()
        )
        save_changes(new_user)
        return generate_token(new_user)
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return response_object, 409



def get_all_users():
    return User.query.all()

def all_organizations():
    print("dgfkgjhdgk")
    print()
    return User.query.with_entities(User.org_name).distinct().all()


def get_all_orgname(org_name):
    return User.query.filter(User.org_name.contains(org_name)).all()

def get_a_user(public_id):
    return User.query.filter_by(public_id=public_id).first()



def get_only_email(email):
    print(email)
    result= User.query.filter(User.email.contains(email)).all()
    print(result,"dgfdg")
    
    return result

    
def delete_user(public_id):
        # User.query.filter_by(public_id)
        # db.session.delete(public_id)
        # db.session.commit()
        # return '', 204
    result = User.query.filter_by(public_id =public_id).first()
    # return result
    print(result)
    if  result:
        db.session.delete(result)
        db.session.commit()
        return { "msg":"user deleted"},200
    else:
        return {"msg":"user not found "}, 404


def update_user(public_id,email,username):
        req = request.get_json()
        result = User.query.filter_by(public_id=public_id).first()
        
        if 'email' in req:
            req.email = req['email']
        if 'username' in req:
            req.username = req['username']
        
        db.session.add(result)
        db.session.commit()

        return result

 






  


def generate_token(user: User) -> Tuple[Dict[str, str], int]:
    try:
        # generate the auth token
        auth_token = User.encode_auth_token(user.id)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401


def save_changes(data: User) -> None:
    db.session.add(data)
    # db.session.delete()
    db.session.commit()



 # "admiin@gmail.com" ["admin","gmail.com"][1]['gmail','com'][0]
    # domain = email.split("@")[-1].split('.')[0]
    # result= User.query.filter(User.email.contains(domain)).all()

    # def get_all_users(email):
#     # "admiin@gmail.com" ["admin","gmail.com"][1]['gmail','com'][0]
#     domain = email.split("@")[-1].split('.')[0]
#     result= User.query.filter(User.email.contains(domain)).all()

#     return result