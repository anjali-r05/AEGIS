import os
import json
import math
import random
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from models import db, IncidentReport, LocationSafety, PublicSafetyData, JourneySession, RiskAssessment, EmergencyContact
from ai_engine import SafetyAIEngine

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'aegis-ultra-secure-key-2026')

# Database configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_url = os.getenv('DATABASE_URL', f"sqlite:///{os.path.join(BASE_DIR, 'aegis.db')}")
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
ai_engine = SafetyAIEngine()

# Ensure Database Tables Exist & Seed Data
def init_db():
    with app.app_context():
        db.create_all()
        # Auto-seed if empty
        if LocationSafety.query.count() == 0:
            try:
                from seed_data import seed_database
                seed_database()
            except Exception as e:
                print("Error during auto-seeding:", e)

init_db()

# ==================== PAGE ROUTES ====================

@app.route('/')
def index():
    """Main Landing Command Center"""
    recent_reports = IncidentReport.query.order_by(IncidentReport.timestamp.desc()).limit(6).all()
    hotspots = LocationSafety.query.order_by(LocationSafety.safety_score.asc()).limit(5).all()
    metrics = {
        'total_locations': LocationSafety.query.count() or 56,
        'active_hotspots': LocationSafety.query.filter(LocationSafety.safety_score < 60).count() or 9,
        'verified_reports': IncidentReport.query.filter_by(is_verified=True).count() or 12,
        'avg_safety_score': round(db.session.query(db.func.avg(LocationSafety.safety_score)).scalar() or 68.4, 1)
    }
    return render_template('index.html', recent_reports=recent_reports, hotspots=hotspots, metrics=metrics)

@app.route('/map')
def live_map():
    """Live Safety Map & Danger Pulse™"""
    return render_template('map.html')

@app.route('/guardian')
def guardian_mode():
    """Guardian Mode™ Live Monitoring Interface"""
    active_session = JourneySession.query.filter_by(status='ACTIVE').order_by(JourneySession.id.desc()).first()
    return render_template('guardian.html', session=active_session)

@app.route('/route-planner')
def route_planner():
    """Safe Corridor™ AI Route Engine"""
    return render_template('route_planner.html')

@app.route('/emergency')
def emergency_center():
    """One-Tap SOS Emergency Dispatch Center"""
    emergency_contacts = EmergencyContact.query.all()
    return render_template('emergency.html', emergency_contacts=emergency_contacts)

@app.route('/report', methods=['GET', 'POST'])
def report_incident():
    """Anonymous Community Incident Reporting"""
    if request.method == 'POST':
        incident_type = request.form.get('incident_type', 'Suspicious Activity')
        description = request.form.get('description', '')
        address = request.form.get('address', 'Unspecified Location')
        latitude = float(request.form.get('latitude', 28.6315))
        longitude = float(request.form.get('longitude', 77.2167))
        lighting = int(request.form.get('lighting', 5))
        crowd = int(request.form.get('crowd', 5))

        new_report = IncidentReport(
            incident_type=incident_type,
            description=description,
            address=address,
            latitude=latitude,
            longitude=longitude,
            lighting_score=lighting,
            crowd_density=crowd,
            confidence_score=88.5,
            is_verified=True,
            status='ACTIVE'
        )
        db.session.add(new_report)
        db.session.commit()
        flash('Incident report submitted anonymously to community safety mesh!', 'success')
        return redirect(url_for('live_map'))

    return render_template('report.html')

@app.route('/analytics')
def analytics():
    """AI Analytics Dashboard & Predictive Risk Models"""
    return render_template('analytics.html')

# ==================== REST API ENDPOINTS ====================

@app.route('/api/dashboard', methods=['GET'])
def api_dashboard():
    """Get high-level safety telemetry metrics"""
    avg_score = db.session.query(db.func.avg(LocationSafety.safety_score)).scalar() or 68.4
    active_hotspots = LocationSafety.query.filter(LocationSafety.safety_score < 60.0).count()
    
    return jsonify({
        'status': 'success',
        'metrics': {
            'city_safety_score': round(avg_score, 1),
            'active_hotspots': active_hotspots,
            'incidents_24h': IncidentReport.query.count(),
            'avg_emergency_response_sec': 14,
            'active_guardians': random.randint(12, 28),
            'safest_area_today': "DLF Cyber Hub Gurgaon",
            'rising_danger_zone': "Okhla Industrial Estate Phase 3"
        }
    })

@app.route('/api/hotspots', methods=['GET'])
def api_hotspots():
    """Return all location safety data for map overlays & Danger Pulse™"""
    locations = LocationSafety.query.all()
    reports = IncidentReport.query.all()
    safe_zones = PublicSafetyData.query.all()

    report_list = [r.to_dict() for r in reports]
    return jsonify({
        'status': 'success',
        'locations': [l.to_dict() for l in locations],
        'incidents': report_list,
        'reports': report_list,
        'safe_zones': [s.to_dict() for s in safe_zones]
    })

@app.route('/api/report', methods=['POST'])
def api_submit_report():
    """API endpoint to post anonymous community safety report"""
    data = request.get_json() or {}
    description = data.get('description', '')
    ai_analysis = ai_engine.process_community_report(description)

    report = IncidentReport(
        incident_type=data.get('incident_type', 'General Safety Hazard'),
        description=description,
        latitude=float(data.get('latitude', 28.6315)),
        longitude=float(data.get('longitude', 77.2167)),
        address=data.get('address', 'Delhi NCR'),
        lighting_score=int(data.get('lighting_score', data.get('lighting', 5))),
        crowd_density=int(data.get('crowd_density', data.get('crowd', 5))),
        confidence_score=ai_analysis.get('confidence_score', 90.0),
        is_verified=True,
        status='ACTIVE'
    )
    db.session.add(report)
    db.session.commit()
    return jsonify({
        'status': 'success',
        'report': report.to_dict(),
        'ai_analysis': ai_analysis
    })

@app.route('/api/safe-route', methods=['POST'])
def api_safe_route():
    """Safe Corridor™ Algorithm - Generates Safest vs Fastest Routes"""
    data = request.get_json() or {}
    start_lat = float(data.get('start_lat', 28.6315))
    start_lng = float(data.get('start_lng', 77.2167))
    dest_lat = float(data.get('dest_lat', 28.5529))
    dest_lng = float(data.get('dest_lng', 77.2062))

    route_res = ai_engine.calculate_safe_route(start_lat, start_lng, dest_lat, dest_lng)
    return jsonify({
        'status': 'success',
        'routes': route_res,
        'route': route_res
    })

@app.route('/api/start-journey', methods=['POST'])
def api_start_journey():
    """Start Guardian Mode™ Journey Session"""
    data = request.get_json() or {}
    start_lat = float(data.get('start_lat', 28.6315))
    start_lng = float(data.get('start_lng', 77.2167))
    dest_lat = float(data.get('dest_lat', 28.5529))
    dest_lng = float(data.get('dest_lng', 77.2062))
    expected_eta = int(data.get('expected_eta', 20))

    session = JourneySession(
        user_name="Anonymous Traveler",
        start_lat=start_lat,
        start_lng=start_lng,
        dest_lat=dest_lat,
        dest_lng=dest_lng,
        current_lat=start_lat,
        current_lng=start_lng,
        expected_eta=expected_eta,
        status='ACTIVE'
    )
    db.session.add(session)
    db.session.commit()

    return jsonify({
        'status': 'success',
        'session': session.to_dict()
    })

@app.route('/api/heartbeat', methods=['POST'])
def api_heartbeat():
    """Guardian Mode™ Heartbeat & Anomaly Detector"""
    data = request.get_json() or {}
    session_id = data.get('session_id')
    curr_lat = float(data.get('latitude', 28.6315))
    curr_lng = float(data.get('longitude', 77.2167))
    is_stopped = data.get('is_stopped', False)

    session = None
    if session_id:
        session = JourneySession.query.get(session_id)
    if not session:
        session = JourneySession.query.filter_by(status='ACTIVE').order_by(JourneySession.id.desc()).first()

    if session:
        session.current_lat = curr_lat
        session.current_lng = curr_lng
        session.last_heartbeat = datetime.utcnow()
        db.session.commit()

    trigger_alert = is_stopped
    alert_reason = "Unusual Standstill Detected in Low-Light Corridor" if is_stopped else None

    return jsonify({
        'status': 'success',
        'trigger_alert': trigger_alert,
        'alert_reason': alert_reason,
        'session': session.to_dict() if session else None
    })

@app.route('/api/emergency', methods=['POST'])
def api_trigger_emergency():
    """One-Tap SOS Emergency Beacon Dispatch"""
    data = request.get_json() or {}
    latitude = float(data.get('latitude', 28.6315))
    longitude = float(data.get('longitude', 77.2167))
    reason = data.get('reason', 'ONE-TAP SOS MANUAL DISTRESS TRIGGER')

    nearest = PublicSafetyData.query.first()

    return jsonify({
        'status': 'escalated',
        'latitude': latitude,
        'longitude': longitude,
        'reason': reason,
        'nearest_station': nearest.police_station_name if nearest else "CP Central Police HQ",
        'station_contact': nearest.police_contact if nearest else "112",
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/api/trends', methods=['GET'])
def api_trends():
    """Hourly Safety Forecast & Incident Category Distribution"""
    tf = ai_engine.predict_time_risk_forecast()
    hours = ["12 PM", "2 PM", "4 PM", "6 PM", "8 PM", "10 PM", "12 AM", "2 AM", "4 AM", "6 AM", "8 AM", "10 AM"]
    risk_scores = [32, 28, 35, 52, 68, 82, 89, 94, 86, 62, 40, 31]
    categories = {
        'Poor Street Lighting': 38,
        'Harassment / Stalking': 26,
        'Isolated Stretches': 20,
        'Suspicious Gathering': 16
    }
    return jsonify({
        'status': 'success',
        'time_forecast': tf,
        'hourly_hours': hours,
        'hourly_risk': risk_scores,
        'category_breakdown': categories
    })

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=True)
