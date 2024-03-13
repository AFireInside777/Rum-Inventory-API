from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import Rum, db, rum_schema, rums_schema, users_schema, User
import secrets

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/addrum', methods = ['POST'])
@token_required
def addrum(current_user_token):
    rum_company  = request.json['rum_company']
    rum_name  = request.json['rum_name']
    rum_age = request.json['rum_age']
    rum_stock_qty = request.json['rum_stock_qty']
    rum_price = request.json['rum_price']

    print(f'The current User Token is: '+ current_user_token.token)

    rum_user_token = current_user_token.token

    rum = Rum(rum_company, rum_name, rum_stock_qty, rum_price, rum_user_token, rum_age)

    db.session.add(rum)
    db.session.commit()

    response = rum_schema.dump(rum)
    return jsonify(response)


@api.route('/getrums', methods = ['GET'])
@token_required
def getrum(current_user_token):
    rums = Rum.query.filter_by(rum_user_token = current_user_token.token).all()
    response = rums_schema.dump(rums)
    return jsonify(response)

@api.route('/deleterum/<id>', methods = ['DELETE'])
@token_required
def deleterums(current_user_token, id):
    rumdelete = Rum.query.filter_by(rum_id = id).first()
    if rumdelete.rum_user_token == current_user_token.token:
        print(f'The following selection will be deleted: {rumdelete.rum_company} {rumdelete.rum_name} {rumdelete.rum_id}')
        db.session.delete(rumdelete)
        db.session.commit()

        response = rum_schema.dump(rumdelete)
        return jsonify(response)
    else:
        return jsonify({'message': 'The token is not correct.'})
    
@api.route('/editrum/<id>', methods = ['PUT'])
@token_required
def editrum(current_user_token, id):
    rumedit = Rum.query.filter_by(rum_id = id).first()
    if secrets.compare_digest(rumedit.rum_user_token, current_user_token.token):
        rumedit.rum_company  = request.json['rum_company']
        rumedit.rum_name  = request.json['rum_name']
        rumedit.rum_age = request.json['rum_age']
        rumedit.rum_stock_qty = request.json['rum_stock_qty']
        rumedit.rum_price = request.json['rum_price']
        rumedit.rum_user_token = current_user_token.token

        db.session.add(rumedit)
        db.session.commit()

        response = rum_schema.dump(rumedit)
        return jsonify ({'message': 'Here is the new rum entry: '}, response)
    else:
        return jsonify ({'message': "The token sent for this request does not match the rum item."})
    
@api.route('/getusers', methods = ['GET'])
@token_required
def getusers(current_user_token):
    users = User.query.all()
    response = users_schema.dump(users)
    return jsonify(response)