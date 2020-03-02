from flask import Flask
from flask_cors import CORS
from flask import request, json, jsonify

# use flask library
app = Flask(__name__)
CORS(app)

# index URL Route
@app.route('/')
def index():
    return jsonify({"message": "OK: Hello World"}), 200

# Call Main Program
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0',port=8080)	
