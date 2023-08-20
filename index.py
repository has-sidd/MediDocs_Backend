from flask import Flask,request, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, login_manager, current_user
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from datetime import datetime
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, unset_jwt_cookies
from itertools import groupby

from flask_cors import CORS
import cv2
from image_to_text import *
from contour_detection import *

app = Flask(__name__)

# app.config['JWT_SECRET_KEY'] = '4705'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/ehr'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
# jwt = JWTManager(app)
login_manager = LoginManager()
login_manager.init_app(app)

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    number = db.Column(db.String(20), nullable=False)
    cnic = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    medical_data = db.relationship('UserMedicalData', backref='user', lazy=True)

    def __init__(self, name, email, number, cnic, password):
        self.name = name
        self.email = email
        self.number = number
        self.cnic = cnic
        self.password = password

class MedicalTerm(db.Model):
    term_id = db.Column(db.Integer, primary_key=True)
    term_name = db.Column(db.String(100))
    medical_data = db.relationship('UserMedicalData', backref='term', lazy=True)

    def __init__(self, term_name):
        self.term_name = term_name

class UserMedicalData(db.Model):
    data_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    term_id = db.Column(db.Integer, db.ForeignKey('medical_term.term_id'), nullable=False)
    value = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.now() )

    def __init__(self, user_id, term_id, value):
        self.user_id = user_id
        self.term_id = term_id
        self.value = value

class Report(db.Model):
    report_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    image = db.Column(db.Text, nullable=True)  # Base64 encoded image
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, name, image, user_id):
        self.name = name
        self.image = image
        self.user_id = user_id

CORS(app, resources={r'/*': {'origins': '*'}})

class RegisterSchema(ma.Schema):
    class Meta:
        fields = ('name', 'email', 'number', 'cnic', 'password')
register_schema = RegisterSchema()

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/register', methods=['POST'])
def register():
    name = request.json['name']
    email = request.json['email']
    number = request.json['number']
    cnic = request.json['cnic']
    password = request.json['password']

    existing_user = Users.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"success": False, "message": "Email already registered"}), 400
    
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    user = Users(name=name, email=email, number=number, cnic=cnic, password=hashed_password)
    
    db.session.add(user)
    db.session.commit()
        
    return jsonify({"success": True, "message": "Registered successfully!"})

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    user = Users.query.filter_by(email=email).first()
    
    if user and bcrypt.check_password_hash(user.password, password):
        login_user(user)
        access_token = str(user.name) + str(user.id)
        return jsonify({"success": True, "message": "Logged in successfully!", "token": access_token})
    
    return jsonify({"success": False, "message": "Invalid email or password"}), 401

@app.route('/logout', methods=['POST'])
@login_required
# @jwt_required()
def logout():
    logout_user()
    response = jsonify({"success": True, "message": "Logged out successfully!"})
    # unset_jwt_cookies(response)
    return response



@app.route('/Ocr', methods=["POST"],strict_slashes=False)
def Image_to_text():
    Input_image = request.get_json(force=True)['data']
    Input_image = Input_image[22:]

    text = scanned_img(Input_image)

    return text

@app.route('/store_medical_data', methods=['POST'])
@login_required
def store_medical_data_endpoint():
    user_id = current_user.id 
    data = request.json
    
    # Check if the data is a list directly or wrapped inside a dictionary
    if isinstance(data, list):
        medical_data_array = data
    else:
        medical_data_array = data.get('medical_data', [])


    try:
        for data in medical_data_array:
            term_name = data.get('key')
            value = data.get('value')

            # Check if the medical term already exists
            term = MedicalTerm.query.filter_by(term_name=term_name).first()

            # If the term doesn't exist, create a new one
            if not term:
                term = MedicalTerm(term_name=term_name)
                db.session.add(term)
                db.session.commit()

            # Now, store the user's medical data
            user_medical_data = UserMedicalData(
                user_id=user_id,
                term_id=term.term_id,
                value=value,
            )
            db.session.add(user_medical_data)
            db.session.commit()

        return jsonify({"success": True, "message": "Data stored successfully!"})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)})
    
@app.route('/get_medical_data', methods=['GET'])
@login_required
def get_medical_data():
    try:
        results = db.session.query(UserMedicalData, MedicalTerm.term_name)\
            .join(MedicalTerm, UserMedicalData.term_id == MedicalTerm.term_id)\
            .filter(UserMedicalData.user_id == current_user.id)\
            .order_by(MedicalTerm.term_name, UserMedicalData.timestamp.desc())\
            .all()

        # Extract and structure the data
        medical_data = [{"term_name": term, "value": data.value, "timestamp": data.timestamp} for data, term in results]

        return jsonify({"success": True, "medical_data": medical_data})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)})
    
@app.route('/save_report', methods=['POST'])
@login_required
def save_report():
    try:
        data = request.json
        report_name = data['name']
        image_base64 = data['image']

        # Create a new report instance
        new_report = Report(name=report_name, image=image_base64, user_id=current_user.id)
        db.session.add(new_report)
        db.session.commit()

        return jsonify({"success": True, "message": "Report saved successfully!"})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400
    
@app.route('/get_reports', methods=['GET'])
@login_required
def get_reports():
    try:
        # Fetch reports for the logged-in user
        reports = Report.query.filter_by(user_id=current_user.id).all()

        # Convert reports to a list of dictionaries
        report_data = [{"id": report.report_id, "name": report.name, "image": report.image} for report in reports]

        return jsonify({"success": True, "reports": report_data})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)})
    
@app.route('/delete_report/<int:report_id>', methods=['DELETE'])
@login_required
def delete_report(report_id):
    try:
        report = Report.query.get(report_id)
        if not report:
            return jsonify({"success": False, "message": "Report not found!"}), 404

        if report.user_id != current_user.id:
            return jsonify({"success": False, "message": "Unauthorized!"}), 403

        db.session.delete(report)
        db.session.commit()

        return jsonify({"success": True, "message": "Report deleted successfully!"})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)})



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0" ,port=5050)
