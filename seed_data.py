import os
from models import db, LocationSafety, PublicSafetyData, IncidentReport, EmergencyContact
from app import app
from datetime import datetime, timedelta

DELHI_LOCATIONS = [
    {"name": "Connaught Place Inner Circle", "lat": 28.6315, "lng": 77.2167, "lighting": 9.2, "crowd": 8.8, "police": 0.3, "incidents": 2, "category": "Safe"},
    {"name": "Hauz Khas Village Fort Area", "lat": 28.5529, "lng": 77.2062, "lighting": 6.1, "crowd": 7.5, "police": 1.8, "incidents": 11, "category": "Moderate"},
    {"name": "DLF Cyber Hub Gurgaon", "lat": 28.4950, "lng": 77.0895, "lighting": 9.5, "crowd": 9.0, "police": 0.5, "incidents": 1, "category": "Safe"},
    {"name": "Select CITYWALK Saket", "lat": 28.5283, "lng": 77.2192, "lighting": 9.0, "crowd": 8.5, "police": 0.8, "incidents": 3, "category": "Safe"},
    {"name": "Noida Sector 18 Market", "lat": 28.5708, "lng": 77.3261, "lighting": 8.8, "crowd": 8.2, "police": 0.6, "incidents": 4, "category": "Safe"},
    {"name": "Chandni Chowk Main Road", "lat": 28.6506, "lng": 77.2303, "lighting": 7.0, "crowd": 9.5, "police": 0.4, "incidents": 8, "category": "Moderate"},
    {"name": "Rajouri Garden Metro Junction", "lat": 28.6415, "lng": 77.1209, "lighting": 8.2, "crowd": 7.8, "police": 1.1, "incidents": 5, "category": "Safe"},
    {"name": "Karol Bagh Market", "lat": 28.6514, "lng": 77.1907, "lighting": 7.8, "crowd": 8.0, "police": 0.7, "incidents": 6, "category": "Moderate"},
    {"name": "Lajpat Nagar Central Market", "lat": 28.5677, "lng": 77.2433, "lighting": 8.5, "crowd": 8.6, "police": 0.9, "incidents": 3, "category": "Safe"},
    {"name": "Janakpuri West Interchange", "lat": 28.6295, "lng": 77.0778, "lighting": 8.0, "crowd": 7.2, "police": 1.2, "incidents": 4, "category": "Safe"},
    {"name": "Vasant Kunj Ambience Mall", "lat": 28.5412, "lng": 77.1558, "lighting": 9.1, "crowd": 8.0, "police": 1.0, "incidents": 2, "category": "Safe"},
    {"name": "Dwarka Sector 21 Metro Hub", "lat": 28.5522, "lng": 77.0583, "lighting": 7.2, "crowd": 6.5, "police": 1.4, "incidents": 7, "category": "Moderate"},
    {"name": "India Gate Hexagon", "lat": 28.6129, "lng": 77.2295, "lighting": 9.4, "crowd": 8.5, "police": 0.2, "incidents": 1, "category": "Safe"},
    {"name": "Khan Market Commercial Zone", "lat": 28.6002, "lng": 77.2272, "lighting": 9.3, "crowd": 7.8, "police": 0.4, "incidents": 1, "category": "Safe"},
    {"name": "Rohini Sector 10 DDA Park", "lat": 28.7180, "lng": 77.1189, "lighting": 4.5, "crowd": 3.2, "police": 2.8, "incidents": 18, "category": "High Risk"},
    {"name": "Gurgaon Golf Course Road", "lat": 28.4595, "lng": 77.0988, "lighting": 8.9, "crowd": 7.1, "police": 1.0, "incidents": 2, "category": "Safe"},
    {"name": "Noida Electronic City Metro", "lat": 28.6280, "lng": 77.3758, "lighting": 7.5, "crowd": 6.8, "police": 1.5, "incidents": 6, "category": "Moderate"},
    {"name": "Pari Chowk Greater Noida", "lat": 28.4671, "lng": 77.5138, "lighting": 5.8, "crowd": 5.0, "police": 2.1, "incidents": 14, "category": "High Risk"},
    {"name": "Faridabad Neelam Chowk", "lat": 28.3962, "lng": 77.3060, "lighting": 6.5, "crowd": 6.0, "police": 1.7, "incidents": 9, "category": "Moderate"},
    {"name": "Indirapuram Habitat Centre", "lat": 28.6369, "lng": 77.3712, "lighting": 8.0, "crowd": 7.4, "police": 1.2, "incidents": 4, "category": "Safe"},
    {"name": "Okhla Industrial Estate Phase 3", "lat": 28.5355, "lng": 77.2728, "lighting": 3.8, "crowd": 2.5, "police": 3.1, "incidents": 22, "category": "Critical"},
    {"name": "Mayur Vihar Phase 1 Metro", "lat": 28.6041, "lng": 77.2942, "lighting": 7.9, "crowd": 7.0, "police": 1.1, "incidents": 5, "category": "Safe"},
    {"name": "Kashmere Gate ISBT Complex", "lat": 28.6675, "lng": 77.2285, "lighting": 6.8, "crowd": 9.2, "police": 0.5, "incidents": 12, "category": "Moderate"},
    {"name": "Anand Vihar Railway Terminal", "lat": 28.6502, "lng": 77.3151, "lighting": 6.2, "crowd": 9.0, "police": 0.6, "incidents": 15, "category": "High Risk"},
    {"name": "ITO Crossing Footover Bridge", "lat": 28.6288, "lng": 77.2415, "lighting": 8.2, "crowd": 8.0, "police": 0.4, "incidents": 3, "category": "Safe"},
    {"name": "South Extension Part 2", "lat": 28.5689, "lng": 77.2208, "lighting": 8.7, "crowd": 8.1, "police": 0.8, "incidents": 2, "category": "Safe"},
    {"name": "Green Park Market", "lat": 28.5584, "lng": 77.2025, "lighting": 8.4, "crowd": 7.6, "police": 0.9, "incidents": 3, "category": "Safe"},
    {"name": "Kamla Nagar Market (DU North Campus)", "lat": 28.6826, "lng": 77.2038, "lighting": 8.6, "crowd": 8.9, "police": 0.7, "incidents": 4, "category": "Safe"},
    {"name": "Mukherjee Nagar Coaching Hub", "lat": 28.7090, "lng": 77.2155, "lighting": 6.9, "crowd": 8.4, "police": 1.2, "incidents": 8, "category": "Moderate"},
    {"name": "Civil Lines Heritage Belt", "lat": 28.6782, "lng": 77.2238, "lighting": 8.1, "crowd": 5.5, "police": 0.5, "incidents": 3, "category": "Safe"},
    {"name": "Pitampura TV Tower Circle", "lat": 28.6975, "lng": 77.1420, "lighting": 7.7, "crowd": 7.0, "police": 1.0, "incidents": 5, "category": "Safe"},
    {"name": "Dilshad Garden Metro", "lat": 28.6758, "lng": 77.3210, "lighting": 6.0, "crowd": 6.2, "police": 1.8, "incidents": 10, "category": "Moderate"},
    {"name": "Loni Border Crossing", "lat": 28.7380, "lng": 77.2880, "lighting": 3.2, "crowd": 4.1, "police": 3.5, "incidents": 25, "category": "Critical"},
    {"name": "Gurgaon Sector 29 Food Street", "lat": 28.4678, "lng": 77.0638, "lighting": 8.8, "crowd": 8.4, "police": 0.9, "incidents": 4, "category": "Safe"},
    {"name": "Gurgaon Sohna Road Corridor", "lat": 28.4120, "lng": 77.0420, "lighting": 6.8, "crowd": 6.1, "police": 2.2, "incidents": 9, "category": "Moderate"},
    {"name": "Noida Sector 62 IT Park", "lat": 28.6230, "lng": 77.3680, "lighting": 8.2, "crowd": 7.3, "police": 1.1, "incidents": 3, "category": "Safe"},
    {"name": "Noida Sector 137 Residential Complex", "lat": 28.5030, "lng": 77.4080, "lighting": 7.9, "crowd": 6.0, "police": 1.9, "incidents": 4, "category": "Safe"},
    {"name": "Ghaziabad Vaishali Sector 4", "lat": 28.6470, "lng": 77.3390, "lighting": 7.4, "crowd": 7.1, "police": 1.3, "incidents": 6, "category": "Moderate"},
    {"name": "Ghaziabad Kavi Nagar Market", "lat": 28.6720, "lng": 77.4420, "lighting": 7.1, "crowd": 6.8, "police": 1.0, "incidents": 5, "category": "Moderate"},
    {"name": "Faridabad NIT Bus Stand", "lat": 28.3840, "lng": 77.2980, "lighting": 5.9, "crowd": 7.2, "police": 1.6, "incidents": 11, "category": "Moderate"},
    {"name": "Dwarka Sector 10 Market", "lat": 28.5810, "lng": 77.0570, "lighting": 8.3, "crowd": 7.5, "police": 0.8, "incidents": 3, "category": "Safe"},
    {"name": "Uttam Nagar East Underpass", "lat": 28.6220, "lng": 77.0650, "lighting": 4.1, "crowd": 8.0, "police": 2.0, "incidents": 19, "category": "High Risk"},
    {"name": "Mehrauli Archaeological Park Road", "lat": 28.5200, "lng": 77.1850, "lighting": 3.5, "crowd": 2.0, "police": 2.5, "incidents": 21, "category": "Critical"},
    {"name": "Chattarpur Enclave Lane", "lat": 28.5020, "lng": 77.1820, "lighting": 5.2, "crowd": 4.8, "police": 2.3, "incidents": 13, "category": "High Risk"},
    {"name": "Badarpur Border Underpass", "lat": 28.4980, "lng": 77.3020, "lighting": 4.2, "crowd": 6.5, "police": 2.6, "incidents": 17, "category": "High Risk"},
    {"name": "Sarita Vihar Pocket A Park", "lat": 28.5290, "lng": 77.2880, "lighting": 7.6, "crowd": 6.2, "police": 1.2, "incidents": 4, "category": "Safe"},
    {"name": "Nizamuddin Railway Junction", "lat": 28.5890, "lng": 77.2530, "lighting": 6.7, "crowd": 8.8, "police": 0.5, "incidents": 8, "category": "Moderate"},
    {"name": "Nehru Place Computer Market", "lat": 28.5490, "lng": 77.2520, "lighting": 8.4, "crowd": 9.1, "police": 0.6, "incidents": 4, "category": "Safe"},
    {"name": "Kalkaji Mandir Metro Complex", "lat": 28.5480, "lng": 77.2590, "lighting": 8.6, "crowd": 8.7, "police": 0.7, "incidents": 3, "category": "Safe"},
    {"name": "Jasola District Centre", "lat": 28.5390, "lng": 77.2840, "lighting": 8.5, "crowd": 7.4, "police": 0.9, "incidents": 2, "category": "Safe"}
]

SAFE_ZONES = [
    {"name": "Connaught Place Police Station", "lat": 28.6328, "lng": 77.2195, "station": "CP Central Police HQ", "contact": "011-23361234", "type": "Police HQ"},
    {"name": "Hauz Khas Police Station", "lat": 28.5489, "lng": 77.2088, "station": "Hauz Khas PS", "contact": "011-26510011", "type": "Police Station"},
    {"name": "Gurgaon DLF Phase 2 Police Booth", "lat": 28.4912, "lng": 77.0871, "station": "Cyber City Police Post", "contact": "0124-2358100", "type": "24x7 Pink Booth"},
    {"name": "Saket Women Police Cell", "lat": 28.5250, "lng": 77.2150, "station": "South District Women Cell", "contact": "011-29561000", "type": "Women Safety Cell"},
    {"name": "Noida Sector 20 Police HQ", "lat": 28.5780, "lng": 77.3210, "station": "Noida Sector 20 PS", "contact": "0120-2521000", "type": "Police Station"},
    {"name": "Chandni Chowk Police Post", "lat": 28.6520, "lng": 77.2320, "station": "Kotwali Police Station", "contact": "011-23861234", "type": "Police Post"},
    {"name": "Janakpuri Pink Police Booth", "lat": 28.6280, "lng": 77.0790, "station": "West District Pink Booth", "contact": "011-25501000", "type": "24x7 Pink Booth"},
    {"name": "Kashmere Gate Metro Police", "lat": 28.6680, "lng": 77.2290, "station": "Metro Police Unit", "contact": "1511", "type": "Metro Safe Zone"}
]

SAMPLE_REPORTS = [
    {"type": "poor_lighting", "desc": "Street lights broken on back lane behind fort", "lat": 28.5520, "lng": 77.2050, "address": "Hauz Khas Lane 4", "lighting": 2, "crowd": 2},
    {"type": "harassment", "desc": "Drunk crowd near underpass passed inappropriate comments", "lat": 28.6210, "lng": 77.0640, "address": "Uttam Nagar Underpass", "lighting": 3, "crowd": 7},
    {"type": "stalking", "desc": "Unregistered vehicle slow following pedestrian", "lat": 28.7170, "lng": 77.1170, "address": "Rohini Sector 10 Park Outer", "lighting": 4, "crowd": 2},
    {"type": "isolated_area", "desc": "Deserted stretch after 9 PM with no security guard", "lat": 28.5340, "lng": 77.2710, "address": "Okhla Phase 3 Street 12", "lighting": 3, "crowd": 1},
    {"type": "suspicious_activity", "desc": "Group loitering near metro exit stairwell", "lat": 28.6490, "lng": 77.3140, "address": "Anand Vihar Exit 2", "lighting": 5, "crowd": 8}
]

def seed_database():
    with app.app_context():
        db.create_all()

        if LocationSafety.query.count() == 0:
            print("Seeding LocationSafety records...")
            for loc in DELHI_LOCATIONS:
                score = (loc["lighting"] * 4.5) + (loc["crowd"] * 2.5) + (max(0, 10 - loc["police"]) * 2.0) - (loc["incidents"] * 1.2)
                score = round(max(10.0, min(98.0, score)), 1)
                
                safety = LocationSafety(
                    location_name=loc["name"],
                    area_code="DEL-" + str(loc["lat"])[3:6],
                    latitude=loc["lat"],
                    longitude=loc["lng"],
                    lighting_score=loc["lighting"],
                    crowd_density=loc["crowd"],
                    police_distance_km=loc["police"],
                    historical_incidents=loc["incidents"],
                    safety_score=score,
                    risk_category=loc["category"]
                )
                db.session.add(safety)

        if PublicSafetyData.query.count() == 0:
            print("Seeding PublicSafetyData records...")
            for sz in SAFE_ZONES:
                p_data = PublicSafetyData(
                    location_name=sz["name"],
                    latitude=sz["lat"],
                    longitude=sz["lng"],
                    police_station_name=sz["station"],
                    police_contact=sz["contact"],
                    safe_zone_type=sz["type"],
                    opening_hours="24 Hours"
                )
                db.session.add(p_data)

        if IncidentReport.query.count() == 0:
            print("Seeding IncidentReport records...")
            for rep in SAMPLE_REPORTS:
                report = IncidentReport(
                    incident_type=rep["type"],
                    description=rep["desc"],
                    latitude=rep["lat"],
                    longitude=rep["lng"],
                    address=rep["address"],
                    lighting_score=rep["lighting"],
                    crowd_density=rep["crowd"],
                    confidence_score=91.0,
                    is_verified=True,
                    status='ACTIVE'
                )
                db.session.add(report)

        if EmergencyContact.query.count() == 0:
            c1 = EmergencyContact(user_name="Anonymous User", contact_name="Mom (Sunita)", phone_number="+91-9811223344", relationship="Mother")
            c2 = EmergencyContact(user_name="Anonymous User", contact_name="Rahul (Brother)", phone_number="+91-9899887766", relationship="Brother")
            db.session.add(c1)
            db.session.add(c2)

        db.session.commit()
        print("Database seeding completed successfully! Total locations:", LocationSafety.query.count())

if __name__ == '__main__':
    seed_database()
