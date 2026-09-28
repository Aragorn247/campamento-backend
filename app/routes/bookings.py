from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.booking import Booking
from app.models.activity import Activity

bookings_bp = Blueprint('bookings', __name__, url_prefix='/api/v1/bookings')

# GET /api/v1/bookings - Lista las reservas del usuario autenticado
@bookings_bp.route('', methods=['GET'])
@jwt_required()
def get_user_bookings():
    user_id = int(get_jwt_identity())
    bookings = Booking.query.filter_by(user_id=user_id).all()
    return jsonify([booking.to_dict() for booking in bookings]), 200

# POST /api/v1/bookings - Crear una nueva reserva
@bookings_bp.route('', methods=['POST'])
@jwt_required()
def create_booking():
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}
    activity_id = data.get('activity_id')

    if not activity_id:
        return jsonify({'error': 'activity_id is required'}), 400

    activity = Activity.query.get(activity_id)
    if not activity:
        return jsonify({'error': 'Activity not found'}), 404

    booking = Booking(user_id=user_id, activity_id=activity_id)
    db.session.add(booking)
    db.session.commit()

    return jsonify({
        'message': 'Booking created successfully',
        'booking': booking.to_dict()
    }), 201