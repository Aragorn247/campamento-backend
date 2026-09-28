from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from app.extensions import db
from app.models.activity import Activity

activities_bp = Blueprint('activities', __name__, url_prefix='/api/v1/activities')

# GET /api/v1/activities - Pública o protegida según convenga (lista todas las actividades)
@activities_bp.route('', methods=['GET'])
def get_activities():
    activities = Activity.query.all()
    return jsonify([activity.to_dict() for activity in activities]), 200

# POST /api/v1/activities - Solo Administradores
@activities_bp.route('', methods=['POST'])
@jwt_required()
def create_activity():
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({'error': 'Admin access required'}), 403

    data = request.get_json() or {}
    name = data.get('name')
    description = data.get('description', '')
    capacity = data.get('capacity')
    price = data.get('price')

    if not name or capacity is None or price is None:
        return jsonify({'error': 'Name, capacity, and price are required'}), 400

    activity = Activity(
        name=name,
        description=description,
        capacity=capacity,
        price=price
    )
    db.session.add(activity)
    db.session.commit()

    return jsonify({
        'message': 'Activity created successfully',
        'activity': activity.to_dict()
    }), 201