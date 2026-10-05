from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.extensions import db
from app.models.user import User
from app.schemas import AuthDTO, validate_json

auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')


@auth_bp.route('/register', methods=['POST'])
@validate_json(AuthDTO.validate_register)
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    username = data.get('username')
    role = data.get('role', 'client')

    # Verificar existencia del usuario en la base de datos
    if User.query.filter_by(email=email).first():
        return jsonify({
            'error': 'Conflict',
            'message': 'El usuario con este correo electrónico ya existe.',
            'status_code': 409
        }), 409

    # Si la entidad User no requiere username en BD, se ignora; si lo requiere, se le asigna
    user = User(email=email, role=role)
    if hasattr(user, 'username'):
        setattr(user, 'username', username)
        
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': 'User registered successfully',
        'user': user.to_dict()
    }), 201


@auth_bp.route('/login', methods=['POST'])
@validate_json(AuthDTO.validate_login)
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({
            'error': 'Unauthorized',
            'message': 'Invalid credentials',
            'status_code': 401
        }), 401

    if not user.is_active:
        return jsonify({
            'error': 'Forbidden',
            'message': 'User account is inactive',
            'status_code': 403
        }), 403

    # Generar Token JWT con identity como string
    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={'role': user.role, 'email': user.email}
    )

    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'user': user.to_dict()
    }), 200