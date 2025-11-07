"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def handle_hello():
    # This is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {"hello": "world",
                     "family": members}
    return jsonify(response_body), 200


@app.route('/members', methods=['POST'])
def add_new():
    # This is how you can use the Family datastructure by calling its methods
    body = request.get_json()
    required_list = {"first_name", "lucky_numbers", "age"}
    if required_list.issubset(body):

        if not isinstance(body["first_name"], str):
            return "error, first_name debe ser str", 400
        if not isinstance(body["age"], int):
            return "error, age debe ser un número", 400
        if not isinstance(body["lucky_numbers"], list):
            return "error, lucky_numbers debe ser una lista de números", 400
        if not all(isinstance(num, int) for num in body["lucky_numbers"]):
            return "error, La lista 'lucky_numbers' debe contener solo números enteros", 400
        jackson_family.add_member(body)

        return jsonify(jackson_family.get_all_members()), 200
    
    missing_keys = required_list - body.keys()
    return f"error, Faltan las siguientes claves: {missing_keys}", 400


@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    jackson_family.delete_member(id)

    return jsonify(jackson_family.get_all_members()), 200


@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):

    return jsonify(jackson_family.get_member(id)), 200


# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
