from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class IncidentReport(db.Model):
    __tablename__ = 'incident_reports'
    id = db.Column(db.Integer, primary_key=True)
    incident_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(255), nullable=True)
    lighting_score = db.Column(db.Integer, default=5)
    crowd_density = db.Column(db.Integer, default=5)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    is_verified = db.Column(db.Boolean, default=True)
    confidence_score = db.Column(db.Float, default=85.0)
    status = db.Column(db.String(20), default='ACTIVE')

    def to_dict(self):
        return {
            'id': self.id,
            'incident_type': self.incident_type,
            'description': self.description,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'address': self.address,
            'lighting_score': self.lighting_score,
            'crowd_density': self.crowd_density,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'is_verified': self.is_verified,
            'confidence_score': self.confidence_score,
            'status': self.status
        }

class LocationSafety(db.Model):
    __tablename__ = 'location_safety'
    id = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String(150), nullable=False)
    area_code = db.Column(db.String(50), nullable=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    lighting_score = db.Column(db.Float, default=7.0)
    crowd_density = db.Column(db.Float, default=6.0)
    police_distance_km = db.Column(db.Float, default=1.5)
    historical_incidents = db.Column(db.Integer, default=2)
    safety_score = db.Column(db.Float, default=75.0)
    risk_category = db.Column(db.String(30), default='Safe')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'location_name': self.location_name,
            'area_code': self.area_code,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'lighting_score': self.lighting_score,
            'crowd_density': self.crowd_density,
            'police_distance_km': self.police_distance_km,
            'historical_incidents': self.historical_incidents,
            'safety_score': self.safety_score,
            'risk_category': self.risk_category,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class PublicSafetyData(db.Model):
    __tablename__ = 'public_safety_data'
    id = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String(150), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    police_station_name = db.Column(db.String(150), nullable=False)
    police_contact = db.Column(db.String(30), default='112')
    safe_zone_type = db.Column(db.String(50), default='Police Station')
    opening_hours = db.Column(db.String(50), default='24 Hours')

    def to_dict(self):
        return {
            'id': self.id,
            'location_name': self.location_name,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'police_station_name': self.police_station_name,
            'police_contact': self.police_contact,
            'safe_zone_type': self.safe_zone_type,
            'opening_hours': self.opening_hours
        }

class JourneySession(db.Model):
    __tablename__ = 'journey_sessions'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), default='Anonymous User')
    start_lat = db.Column(db.Float, nullable=False)
    start_lng = db.Column(db.Float, nullable=False)
    dest_lat = db.Column(db.Float, nullable=False)
    dest_lng = db.Column(db.Float, nullable=False)
    current_lat = db.Column(db.Float, nullable=True)
    current_lng = db.Column(db.Float, nullable=True)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    expected_eta = db.Column(db.Integer, default=20)
    last_heartbeat = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(30), default='ACTIVE')
    route_path = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_name': self.user_name,
            'start_lat': self.start_lat,
            'start_lng': self.start_lng,
            'dest_lat': self.dest_lat,
            'dest_lng': self.dest_lng,
            'current_lat': self.current_lat or self.start_lat,
            'current_lng': self.current_lng or self.start_lng,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'expected_eta': self.expected_eta,
            'last_heartbeat': self.last_heartbeat.isoformat() if self.last_heartbeat else None,
            'status': self.status,
            'route_path': json.loads(self.route_path) if self.route_path else []
        }

class RiskAssessment(db.Model):
    __tablename__ = 'risk_assessments'
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    score = db.Column(db.Float, nullable=False)
    risk_level = db.Column(db.String(30), nullable=False)
    confidence = db.Column(db.Float, default=92.5)
    lighting_score = db.Column(db.Float, default=6.0)
    crowd_density = db.Column(db.Float, default=5.0)
    time_factor = db.Column(db.Float, default=1.0)
    reasoning_json = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'score': self.score,
            'risk_level': self.risk_level,
            'confidence': self.confidence,
            'lighting_score': self.lighting_score,
            'crowd_density': self.crowd_density,
            'time_factor': self.time_factor,
            'reasoning': json.loads(self.reasoning_json) if self.reasoning_json else [],
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class EmergencyContact(db.Model):
    __tablename__ = 'emergency_contacts'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), default='Anonymous User')
    contact_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    relationship = db.Column(db.String(50), default='Guardian')

    def to_dict(self):
        return {
            'id': self.id,
            'user_name': self.user_name,
            'contact_name': self.contact_name,
            'phone_number': self.phone_number,
            'relationship': self.relationship
        }
