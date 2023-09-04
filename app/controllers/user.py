from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models.user import User
from app import db
from app.utils.password import encrypt_password

user_controller_blueprint = Blueprint('user_controller', __name__)


@user_controller_blueprint.route('/create', methods=['POST'])
@jwt_required()
def create_user():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({'error': 'Invalid JSON data'}), 400
        data['password'] = encrypt_password(data['password'])
        new_user = User(**data)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201
    except IntegrityError as e:
        db.session.rollback()  # Rollback the transaction
        error = str(e.orig)
        if (error.startswith("duplicate key value")):
            return jsonify({'error': 'Duplicate email conflict'}), 409
        else:
            return jsonify({'error': error.split('DETAIL:')[0]}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user_controller_blueprint.route('/list', methods=['GET'])
@jwt_required()
def get_users_list():
    try:
        us = get_jwt_identity()
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)

        first_name = request.args.get('first_name', type=str)
        email = request.args.get('email', type=str)

        users_query = User.query

        if first_name:
            users_query = users_query.filter(
                User.first_name.ilike(f'%{first_name}%'))

        if email:
            users_query = users_query.filter(User.email.ilike(f'%{email}%'))

        total_count = users_query.count()
        users_query = users_query.paginate(page=page, per_page=per_page)
        users = users_query.items
        total_pages = users_query.pages
        users_list = [user.to_json() for user in users]

        response = {
            "users": users_list,
            "page": page,
            "per_page": per_page,
            "total_count": total_count,
            "total_pages": total_pages
        }

        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
