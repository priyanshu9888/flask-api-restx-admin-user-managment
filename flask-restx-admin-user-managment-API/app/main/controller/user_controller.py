from flask import jsonify, request
from flask_restx import Resource, marshal
from app.main.model import user
from app.main.util.decorator import admin_token_required
from app.main.util.decorator import org_admin_token_required

from ..util.dto import UserDto
from ..service.user_service import *
from ..service.auth_helper import Auth
from typing import Dict, Tuple
import json

api = UserDto.api
_user = UserDto.user


@api.route('/organizations/')

class Organizations(Resource):
    @admin_token_required

    def get(self):
        """List of  all organizations"""

        orgalllist=[i[0] for i in all_organizations()]

        return jsonify(orgalllist)
 

@api.route('/organizations/<org_name>/users')
class org_list(Resource):
    @api.doc('get a organization ')
    @org_admin_token_required

    def get(self, org_name):
        data = Auth.get_logged_in_user(request)
        organization1 = data[0]['data']['org_name']

        """get a user given its identifier"""
       
        if organization1!=org_name:
            response_object = {
            'status': 'fail',
            'message': 'record not found.'
        }
            return response_object, 200
        result = get_all_orgname(org_name)            
        return marshal(result,_user)
@api.route('/')
class UserList(Resource):
    @api.doc('list_of_registered_users')
    @admin_token_required
    @api.marshal_list_with(_user, envelope='data')
    def get(self):
        """List all registered users"""
        data = Auth.get_logged_in_user(request)
        a=data[0]['data']
        print(data)
        if a['admin']:
            return get_all_users()
        else:
            if a['org_admin']:
                return get_all_orgname(a['org_name'])

    @api.expect(_user, validate=True)
    @api.response(201, 'User successfully created.')
    @api.doc('create a new user')
    def post(self) -> Tuple[Dict[str, str], int]:
        """Creates a new User """
        data = request.json
        return save_new_user(data=data)


@api.route('/<public_id>')
@api.param('public_id', 'The User identifier')
@api.response(404, 'User not found.')
class User(Resource):
    @api.doc('get a user')
    @api.marshal_with(_user)
    def get(self, public_id):
        """get a user given its identifier"""
        user = get_a_user(public_id)
        if not user:
            api.abort(404)
        else:
            return user
@api.route('search/<email>')
# @api.response(404,'email not found ')
class email_list(Resource):
    @api.doc('get a email')
    @admin_token_required

    def get(self, email):
        print(email)
        """get a user given its identifier"""
        # da=get_only_email(email)
        # print(da)
        result = get_only_email(email)
        print(result)
        if not result:
            response_object = {
            'status': 'fail',
            'message': 'record not found.'
        }
            return response_object, 200
        return marshal(result,_user)
# @api.route('/<public_id>')
# @api.param('public_id', 'The User identifier')
# @api.response(404, 'User not found.')
# class User(Resource):
@api.route('delete/<public_id>')
@api.response(404,'user not found')
class delete_user_list(Resource):
    @api.doc('get a public_id ')
    @api.marshal_with(_user)
    def delete(self,public_id):
        resu=delete_user(public_id)
       
        if not resu:
            api.abort(404)
        else:
            return resu

     
# @api.route('/update/<public_id>')
# @api.response(200,'user succesfully update')
# class update_user_list(Resource):
#     @api.doc('get a public_id ')
#     @api.marshal_with(_user)
#     def put(self,public_id):

    

#         return update_user



    
        # print(data) #-- type:tuple ({'status':34,'data':{'':''}})[0]['data']['email']



