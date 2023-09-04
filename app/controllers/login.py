from flask import Blueprint, request, jsonify, current_app, session
from flask_jwt_extended import create_access_token
from datetime import timedelta
from app.models.user import User
from app.utils.password import encrypt_password

login_controller_blueprint = Blueprint('login', __name__)


@login_controller_blueprint.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        user = User.query.filter_by(
            email=email, password=encrypt_password(password)).first()
        if (user is None):
            return jsonify({'message': 'Invalid credentials'}), 401
        else:
            user = user.to_json()
            # Set session expiry time
            current_app.permanent_session_lifetime = timedelta(minutes=30)  # Set session expiry time

            # Generate an access token
            access_token = create_access_token(identity=user)

            # Store user_id in the session using pop()
            session.pop('user_id', None)  # Clear any previous session data
            session['user_id'] = user['id']

            return jsonify({'access_token': access_token,'user':user,'isAuthenticated':True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
