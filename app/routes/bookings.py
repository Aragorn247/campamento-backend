from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.booking import Booking
from app.models.activity import Activity
from app.schemas import BookingDTO, validate_json

bookings_bp = Blueprint('bookings', __name__, url_prefix='/api/v1/bookings')

@bookings_bp.route('', methods=['POST'])
@jwt_required()
@validate_json(BookingDTO.validate_create)
def create_booking():
    """
    Crear una reserva para una actividad
    ---
    tags:
      - Reservas
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - activity_id
          properties:
            activity_id:
              type: integer
              example: 1
    responses:
      201:
        description: Reserva creada exitosamente
      400:
        description: Error de validación o sin cupos disponibles
      404:
        description: Actividad no encontrada
    """
    user_id = int(get_jwt_identity())
    data = request.get_json()
    activity_id = data.get('activity_id')

    activity = Activity.query.get(activity_id)
    if not activity:
        return jsonify({
            'error': 'Not Found',
            'message': 'La actividad especificada no existe.',
            'status_code': 404
        }), 404

    # Verificar cupos
    current_bookings = Booking.query.filter_by(activity_id=activity_id).count()
    if current_bookings >= activity.capacity:
        return jsonify({
            'error': 'Bad Request',
            'message': 'No hay cupos disponibles para esta actividad.',
            'status_code': 400
        }), 400

    booking = Booking(user_id=user_id, activity_id=activity_id)
    db.session.add(booking)
    db.session.commit()

    return jsonify({
        'message': 'Reserva realizada exitosamente',
        'booking': booking.to_dict()
    }), 201


@bookings_bp.route('/my-bookings', methods=['GET'])
@jwt_required()
def get_user_bookings():
    """
    Obtener las reservas del usuario autenticado
    ---
    tags:
      - Reservas
    security:
      - Bearer: []
    responses:
      200:
        description: Lista de reservas del usuario obtenida exitosamente
    """
    user_id = int(get_jwt_identity())
    bookings = Booking.query.filter_by(user_id=user_id).all()
    return jsonify([booking.to_dict() for booking in bookings]), 200