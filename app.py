from flask import Flask, request, jsonify
from flask_cors import CORS
from api.users import users_blueprint
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

# use flask library
app = Flask(__name__)
# define token
jwt = JWTManager(app)

app.config["JWT_SECRET_KEY"] = "dr2711hp"

# prevent CORS issue
CORS(app)

# call route here
app.register_blueprint(users_blueprint)


# error not found url handler
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message':   'This URL => ' + request.url + ' is Not Found'
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


# Call Main Program
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8080)