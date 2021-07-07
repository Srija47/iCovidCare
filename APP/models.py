from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from APP import db, login_manager
from flask_login import UserMixin
from flask import current_app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(128))
    created_on = db.Column(db.TIMESTAMP, default=datetime.now())
    role = db.Column(db.String(20),nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    patient = db.relationship('Patient',backref = 'puser',lazy=True)
    doctor=db.relationship('Doctor',backref='duser',lazy=True)
    clinician=db.relationship('Clinician',backref='cuser',lazy=True)

    def get_reset_token(self,expire_sec=1800):
        s=Serializer(current_app.config['SECRET_KEY'],expire_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s=Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id=s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}',{self.id}', '{self.email}', '{self.password}','{self.image_file}','{self.created_on}')"

class Patient(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    gender = db.Column(db.String(10),nullable=False)
    age = db.Column(db.String(10),nullable=False)
    status=db.Column(db.String(50),nullable=True)
    phonenumber = db.Column(db.Integer,nullable=False)
    address = db.Column(db.String(120),nullable=True)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    appointments_id = db.relationship('Appointments',backref = 'appointments_patient',lazy=True)
    user_id= db.Column(db.Integer, db.ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'), index=True, nullable=True)
    def __repr__(self):
        return f"Patient('{self.id}','{self.username}', '{self.email}', '{self.image_file}','{self.password}')"

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    designation = db.Column(db.String(20),nullable=False)
    speciality = db.Column(db.String(20),nullable=True)
    phonenumber = db.Column(db.Integer,nullable=False)
    status=db.Column(db.String(50),nullable=True)
    location = db.Column(db.String(120),nullable=True)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    appointments = db.relationship('Appointments',backref = 'appointments_doctor',lazy=True)
    user_id= db.Column(db.Integer, db.ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'), index=True, nullable=True)
    def __repr__(self):
        return f"Doctor('{self.username}', '{self.email}', '{self.image_file}')"

class Clinician(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    phonenumber = db.Column(db.Integer,nullable=False)
    status=db.Column(db.String(50),nullable=True)
    location = db.Column(db.String(120),nullable=True)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    appointments = db.relationship('Appointments',backref = 'appointments_clinician',lazy=True)
    user_id= db.Column(db.Integer, db.ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'), index=True, nullable=True)
    def __repr__(self):
        return f"Clinician('{self.name}', '{self.email}', '{self.image_file}')"

class Appointments(db.Model):  
    id = db.Column(db.Integer, primary_key=True)
    reports = db.relationship('Reports',backref='reports',lazy=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id', onupdate='CASCADE', ondelete='CASCADE'), index=True, nullable=False)
    clinician_id = db.Column(db.Integer, db.ForeignKey('clinician.id', onupdate='CASCADE', ondelete='CASCADE'), index=True, nullable=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id', onupdate='CASCADE', ondelete='CASCADE'), index=True, nullable=True)
    appointment_date = db.Column(db.DateTime(), nullable=False)
    appointment_type = db.Column(db.String(128), nullable=False, default='general')
    description = db.Column(db.String(150),nullable = False)
    labTestdescription = db.Column(db.String(100),nullable=True)
    def __repr__(self):
        return f"Appointments('{self.id}', '{self.appointment_type}','{self.patient_id}','{self.doctor_id}','{self.clinician_id}', '{self.appointment_date}','{self.description}')"

class Reports(db.Model):        
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(128), nullable=False)
    report = db.Column(db.String(128), nullable=False)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id', onupdate='CASCADE', ondelete='CASCADE'), index=True, nullable=False)
    def __repr__(self):
        return f"reports('{self.id}', '{self.report}','{self.appointment_id}')"
