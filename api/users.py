from bson.errors import InvalidId
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, create_access_token
from config.mongo_db import mongo
from bson.json_util import dumps, loads
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash


users_api = Blueprint('users_api', __name__)


# route login
@users_api.route("/v1/login", methods=["POST"])
def login():
    _json = request.json
    _email = _json['email']
    _password = _json['pwd']
    _hashed_password = generate_password_hash(_password)
    user = mongo.db.user.find_one({"email": _email})
    if user:
        resp = dumps(user)
        encrypted = loads(resp)
        check_pwd = encrypted['pwd']
        if check_password_hash(check_pwd, _password):
            access_token = create_access_token(identity=_email)
            return jsonify(message="Login Succeeded!", access_token=access_token), 201
        else:
            return jsonify(message="Wrong Email or Password"), 401
    else:
        return jsonify(message="Email Not Found"), 401


# route add user
@users_api.route('/v1/register', methods=['POST'])
def add_user():
    _header = request.headers
    auth = _header.get("Register_Token")
    key = 'agfjhefy65dfs'
    if auth == key:
        _json = request.json
        _name = _json['name']
        _email = _json['email']
        _password = _json['pwd']

        # validate the received values
        if _name and _email and _password and request.method == 'POST':
            # do not save password as a plain text
            _hashed_password = generate_password_hash(_password)
            # save details
            mongo.db.user.insert({'name': _name, 'email': _email, 'pwd': _hashed_password})
            resp = jsonify('User added successfully!')
            resp.status_code = 200
            return resp
        else:
            return "not_found"
    else:
        return jsonify(message="Invalid Credential"), 401



# route for get all users
@users_api.route('/v1/users')
@jwt_required
def get_all_users():
    users = mongo.db.user.find()
    resp = dumps(users,indent=4, separators=(',', ': '), sort_keys=True)
    return resp
    mongo.cx.close()


# route for get one user
@users_api.route('/v1/users/<id>')
@jwt_required
def get_one_user(id):
    try:
        user = mongo.db.user.find_one({'_id': ObjectId(id)})
        resp = dumps(user, indent=4, separators=(',', ': '), sort_keys=True)
        if resp == 'null':
            message = {
                'status': 200,
                'message': 'oops user is not Found!!!'
            }
            resp = jsonify(message)
            resp.status_code = 200
            return resp
        else:
            return resp
        mongo.cx.close()
    except (InvalidId, TypeError):
        message = {
            'status': 400,
            'message': 'oops Your id format is not standard'
        }
        resp_err_get_one = jsonify(message)
        resp_err_get_one.status_code = 400

        return resp_err_get_one


# route for edit / update user
@users_api.route('/v1/edit_user', methods=['PUT'])
@jwt_required
def update_user():
    try:
        _json = request.json
        _id = _json['_id']
        _name = _json['name']
        _email = _json['email']
        _password = _json['pwd']
        # check user is exists or not?
        user = mongo.db.user.find_one({'_id': ObjectId(_id)})
        resp = dumps(user,indent=4, separators=(',', ': '), sort_keys=True)
        if resp == 'null':
            message = {
                'status': 400,
                'message': 'oops cannot edit user, user not Found !!!'
            }
            resp = jsonify(message)
            resp.status_code = 400
            return resp
        else:

            # validate the received values
            if _name and _email and _password and _id and request.method == 'PUT':
                # do not save password as a plain text
                _hashed_password = generate_password_hash(_password)
                # save edits
                mongo.db.user.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
                                         {'$set': {'name': _name, 'email': _email, 'pwd': _hashed_password}})
                resp = jsonify('User updated successfully!')
                resp.status_code = 200
                return resp
            else:
                return "not_found"

    except (InvalidId, TypeError):
        message = {
            'status': 400,
            'message': 'oops Your id format is not standard'
        }
        resp_err_edit = jsonify(message)
        resp_err_edit.status_code = 400
        return resp_err_edit


# route for delete a user
@users_api.route('/v1/delete_user', methods=['DELETE'])
@jwt_required
def delete():
    try:
        _json = request.json
        _id = _json['_id']
        # check user is exists or not?
        user = mongo.db.user.find_one({'_id': ObjectId(_id)})
        resp = dumps(user)
        if resp == 'null':
            message = {
                'status': 400,
                'message': 'oops cannot delete user, user not Found !!!'
            }
            resp = jsonify(message)
            resp.status_code = 400
            return resp
        else:
            mongo.db.user.delete_one({'_id': ObjectId(_id)})
            resp = jsonify('User deleted successfully!')
            resp.status_code = 200
            return resp

    except (InvalidId, TypeError):
        message = {
            'status': 400,
            'message': 'oops Your id format is not standard'
        }
        resp_err_del_one = jsonify(message)
        resp_err_del_one.status_code = 400
        return resp_err_del_one
