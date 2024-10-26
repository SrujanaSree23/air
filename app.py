from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://YOUR_USERNAME:YOUR_PASSWORD@localhost/air_quality_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)

class AirQuality(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    aqi = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'location': self.location,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'aqi': self.aqi
        }

with app.app_context():
    db.create_all()

@app.route('/api/airquality', methods=['GET'])
def get_air_quality():
    air_quality_data = AirQuality.query.all()
    return jsonify([data.to_dict() for data in air_quality_data])

@app.route('/api/airquality', methods=['POST'])
def add_air_quality():
    data = request.get_json()
    new_entry = AirQuality(
        location=data['location'],
        latitude=data['latitude'],
        longitude=data['longitude'],
        aqi=data['aqi']
    )
    db.session.add(new_entry)
    db.session.commit()
    return jsonify(new_entry.to_dict()), 201

if _name_ == '_main_':
    app.run(debug=True)