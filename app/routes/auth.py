from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.extensions import db
from app.models.user import User
from app.schemas import AuthDTO, validate_json

auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

@auth_bp.route('/register', methods=['POST'])
@validate_json(AuthDTO.validate_register)
def register():
    """
    Registro de nuevo usuario
    ---
    tags:
      - Autenticación
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - email
            - password
          properties:
            username:
              type: string
              example: pedro
            email:
              type: string
              example: usuario@campamento.com
            password:
              type: string
              example: password123
            role:
              type: string
              example: client
    responses:
      201:
        description: Usuario registrado exitosamente
      400:
        description: Error de validación en los datos
      409:
        description: El usuario ya existe
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    username = data.get('username')
    role = data.get('role', 'client')

    if User.query.filter_by(email=email).first():
        return jsonify({
            'error': 'Conflict',
            'message': 'El usuario con este correo electrónico ya existe.',
            'status_code': 409
        }), 409

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
    """
    Inicio de sesión de usuario
    ---
    tags:
      - Autenticación
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
              example: usuario@campamento.com
            password:
              type: string
              example: password123
    responses:
      200:
        description: Login exitoso y devolución del JWT Token
      400:
        description: Error de validación
      401:
        description: Credenciales inválidas
    """
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

    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={'role': user.role, 'email': user.email}
    )

    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'user': user.to_dict()
    }), 200