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

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_all_members():
    try: 
        members = jackson_family.get_all_members()
        if not members:
            return jsonify({"error": "No members found"}), 400

        response_body = {
            "family": members
        }
        return jsonify(response_body), 200

    except Exception as e:  
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


    
@app.route('/member/<int:member_id>', methods=['GET'])
def get_member_id(member_id):
    try:
        member = jackson_family.get_member(member_id)
        if not member:
            return jsonify({"error": "No member found"}), 400
        
        response_body = {
            "id": member["id"], 
            "first_name": member["first_name"],  
            "age": member["age"], 
            "lucky_numbers": member["lucky_numbers"] 
        }
        return jsonify(response_body), 200
        
    except Exception as e: 
        return jsonify({"error": "Internal server error", "message": str(e)}), 500



@app.route('/member', methods=['POST'])
def new_member():
    try:
        new_member = request.get_json()
        datos_necesarios = {
            'first_name',
            'age',
            'lucky_numbers'
        }
        for dato in datos_necesarios:
            if dato not in new_member: 
                return jsonify({"error": f"Missing required field: {dato}"}), 400
        

        jackson_family.add_member(new_member)
        return jsonify(new_member), 200
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500
            


@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    try:
        result = jackson_family.delete_member(member_id)

        if result==False:
            return jsonify({"error": "Member not found"}), 400

        return jsonify({"done": True}), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    jackson_family.add_member({
        "first_name": "John Jackson",
        "age": 33,
        "lucky_numbers": [7, 13, 22]
    })

    jackson_family.add_member({
        "first_name": "Jane Jackson",
        "age": 35,
        "lucky_numbers": [10, 14, 3]
    })

    jackson_family.add_member({
        "first_name": "Jimmy Jackson",
        "age": 5,
        "lucky_numbers": [1]
    })
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
