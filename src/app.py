"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

John = {
    "first_name": "John",
    "age": 33,
    "lucky_numbers": [7, 13, 22]
}

Jane = {
    "first_name": "Jane",
    "age": 35,
    "lucky_numbers": [10, 14, 3]
}

Jimmy = {
    "first_name": "Jimmy",
    "age": 5,
    "lucky_numbers": [1]
}

jackson_family.add_member(John)
jackson_family.add_member(Jane)
jackson_family.add_member(Jimmy)


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET']) # Get all family members
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "hello": "world",
        "family": members
    }
    return jsonify(response_body), 200

@app.route('/members/<int:member_id>', methods=['GET'])
def retrieve_one_member(member_id):
    member = jackson_family.get_member(member_id)
    if(member):
        return jsonify(member), 200
    return jsonify({"error":"No existe mimebro con ese id"}), 400
          


@app.route('/members', methods=['POST']) # Create new member
def new_member():
    new_member = request.json
    member = jackson_family.add_member(new_member)
    if(member):
        return jsonify({"message": "Se añadió el mimebro con éxito"}), 200
    return jsonify({"error":"Error al añadir miembro"}), 400
    
@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_one_member(member_id):
    member = jackson_family.delete_member(member_id)
    if(member):
        return jsonify({"message": "Se eliminó el miembro con éxito"}), 200
    return jsonify({"error":"No se borró ningún miembro con ese id"}), 400
          


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
