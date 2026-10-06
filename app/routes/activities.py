from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from app.extensions import db
from app.models.activity import Activity
from app.schemas import ActivityDTO, validate_json

activities_bp = Blueprint('activities', __name__, url_prefix='/api/v1/activities')

@activities_bp.route('', methods=['GET'])
def get_activities():
    """
    Obtener listado de actividades disponibles
    ---
    tags:
      - Actividades
    responses:
      200:
        description: Lista de actividades obtenida exitosamente
    """
    activities = Activity.query.all()
    return jsonify([activity.to_dict() for activity in activities]), 200


@activities_bp.route('', methods=['POST'])
@jwt_required()
@validate_json(ActivityDTO.validate_create)
def create_activity():
    """
    Crear una nueva actividad (Requiere rol admin)
    ---
    tags:
      - Actividades
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
            - capacity
            - price
          properties:
            name:
              type: string
              example: Senderismo y Montañismo
            description:
              type: string
              example: Ruta guiada por la montaña para principiantes.
            capacity:
              type: integer
              example: 15
            price:
              type: number
              example: 25.50
    responses:
      201:
        description: Actividad creada exitosamente
      400:
        description: Error en la validación de los datos
      403:
        description: Requiere privilegios de administrador
    """
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({
            'error': 'Forbidden',
            'message': 'Se requieren privilegios de administrador para realizar esta acción.',
            'status_code': 403
        }), 403

    data = request.get_json()
    activity = Activity(
        name=data['name'],
        description=data.get('description', ''),
        capacity=data['capacity'],
        price=data['price']
    )

    db.session.add(activity)
    db.session.commit()

    return jsonify({
        'message': 'Actividad creada exitosamente',
        'activity': activity.to_dict()
    }), 201