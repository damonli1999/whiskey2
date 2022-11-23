from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Contact, contact_schema, contacts_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'yee': 'haw'}

@api.route('/drinks', methods = ['POST'])
@token_required
def create_contact(current_user_token):
    name = request.json['name']
    type = request.json['type']
    price = request.json['price']
    ingredient = request.json['ingredient']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    contact = Contact(name, type, price, ingredient, user_token = user_token )

    db.session.add(contact)
    db.session.commit()

    response = contact_schema.dump(contact)
    return jsonify(response)

@api.route('/drinks', methods = ['GET'])
@token_required
def get_drink(current_user_token):
    a_drink = current_user_token.token
    contacts = Contact.query.filter_by(user_token = a_drink).all()
    response = contacts_schema.dump(contacts)
    return jsonify(response)

@api.route('/drinks/<id>', methods = ['GET'])
@token_required
def get_single_drink(current_user_token, id):
    contact = Contact.query.get(id)
    response = contact_schema.dump(contact)
    return jsonify(response)

@api.route('/drinks/<id>', methods = ['POST','PUT'])
@token_required
def update_drink(current_user_token,id):
    contact = Contact.query.get(id) 
    contact.name = request.json['name']
    contact.type = request.json['type']
    contact.price = request.json['price']
    contact.ingredient = request.json['ingredient']
    contact.user_token = current_user_token.token

    db.session.commit()
    response = contact_schema.dump(contact)
    return jsonify(response)

@api.route('/drinks/<id>', methods = ['DELETE'])
@token_required
def delete_drink(current_user_token, id):
    contact = Contact.query.get(id)
    db.session.delete(contact)
    db.session.commit()
    response = contact_schema.dump(contact)
    return jsonify(response)