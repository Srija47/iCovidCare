from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from APP import db, bcrypt
from APP.models import User,Patient,Doctor,Clinician,Appointments,Reports
from APP.users.forms import (DoctorRegistrationForm,ClinicianRegistrationForm,RegistrationForm, LoginForm, upload, UpdateAccountForm,AppointmentForm, ResetPasswordForm,RequestResetForm,Report,DocReport,clin_appoint)
from APP.users.utils import save_picture, send_reset_email
from flask import send_from_directory
from tensorflow.keras.models import load_model
from tensorflow import keras
import numpy as np
import os
import pickle
import tensorflow as tf
from tensorflow.keras.preprocessing import image

users=Blueprint('users',__name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password= bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        patient=Patient(username=form.username.data,email=form.email.data,password=hashed_password,gender=form.gender.data,age=form.age.data,address=form.address.data,phonenumber=form.phonenumber.data)
        db.session.add(patient)
        db.session.commit()
        db.session.flush()
        user=User(username=patient.username,email=patient.email,password=patient.password,role='Patient')
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to log in', 'success') 
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Patient-SignUp', form=form)


@users.route("/dregister", methods=['GET', 'POST'])
def dregister():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form1 = DoctorRegistrationForm()
    if form1.validate_on_submit():
        hashed_password= bcrypt.generate_password_hash(form1.password.data).decode('utf-8')
        doctor=Doctor(username=form1.username.data,email=form1.email.data,password=hashed_password,designation=form1.designation.data,speciality=form1.speciality.data,phonenumber=form1.phonenum.data,location=form1.location.data)
        db.session.add(doctor)
        db.session.commit()
        db.session.flush()
        user=User(username=doctor.username,email=doctor.email,password=doctor.password,role='Doctor')
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to log in', 'success') 
        return redirect(url_for('users.login'))
    return render_template('dregister.html', title='Doctor-SignUp', form=form1)    

@users.route("/cregister", methods=['GET', 'POST'])
def cregister():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form2 =  ClinicianRegistrationForm()
    if form2.validate_on_submit():
        hashed_password= bcrypt.generate_password_hash(form2.password.data).decode('utf-8')
        clinician=Clinician(name=form2.name.data,email=form2.email.data,password=hashed_password,phonenumber=form2.phonenum.data,location=form2.location.data)
        db.session.add(clinician)
        db.session.commit()
        db.session.flush()
        user=User(username=clinician.name,email=clinician.email,password=clinician.password,role='Clinician')
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to log in', 'success') 
        return redirect(url_for('users.login'))
    return render_template('cregister.html', title='Clinician-SignUp', form=form2)    

@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember=form.remember.data)
            next_page=request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/account", methods=['GET','POST'])
@login_required
def account():
    form= UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file=save_picture(form.picture.data)
            current_user.image_file=picture_file
        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()
        if current_user.role == 'Doctor':
            Doctor.status = form.status
            db.session.commit()
        elif current_user.role == 'Patient':
            Patient.status = form.status
            db.session.commit()
        elif current_user.role == 'Clinician':
            Clinician.status =form.status
            db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method =='GET':
        form.username.data= current_user.username
        form.email.data= current_user.email
    image_file=url_for('static',filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file,form=form)



@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

@users.route("/patient_report")
def patientreport():
    reports = db.session.query(Reports,Appointments,Patient,Doctor).join(Appointments,Reports.appointment_id==Appointments.id).join(Patient,Appointments.patient_id==Patient.id).join(Doctor,Appointments.doctor_id==Doctor.id).all()
    return render_template('patient_report.html',reports=reports)

@users.route("/aimodel", methods=['GET'])
def aimodel():
    return render_template('aimodel.html', title='AIDiagnosis')

@users.route("/report", methods=['GET','POST'])
def report():
    form=Report()
    if form.validate_on_submit():
        appointments = db.session.query(Appointments,Patient).join(Patient,Appointments.patient_id==Patient.id).filter(Patient.username==form.username.data).all()
        for app,pat in appointments:
            report=Reports(report=form.report.data,description=form.description.data,appointment_id=app.id)
            db.session.add(report)
            db.session.commit()
        flash('Your report has been successfully sent!')
        return redirect(url_for('main.home'))
    return render_template('report.html',title='Send Report',form=form)


@users.route("/doctor_report",methods=['GET','POST'])
def docreport():
    form=DocReport()
    if form.validate_on_submit():
        #appointments = db.session.query(Appointments,Patient,Clinician,Doctor).join(Patient,Appointments.patient_id==Patient.id).join(Clinician,Appointments.clinician_id==Clinician.id).join(Doctor,Appointments.doctor_id==Doctor.id).filter(Patient.username == form.patientname.data,Patient.age==form.age.data,Patient.gender==form.gender.data,Patient.age==form.age.data,Patient.phonenumber==form.phonenumber.data,Appointments.description==form.description.data,Appointments.appointment_date==form.appointmentdate.data,Appointments.labTestdescription==form.labTestdescription.data).first()
        appointments = db.session.query(Appointments).filter(Patient.username == form.patientname.data,Appointments.description==form.description.data).first()
        reports=Reports(report=form.prescription.data,description=form.labTestdescription.data,appointment_id=appointments.id)
        db.session.add(reports)
        db.session.commit()
        flash('Report sent successfully!')
        return redirect(url_for('main.home'))
    return render_template('doctor_report.html',title='Doctor Report',form=form)


@users.route("/clin_appoint",methods=['GET','POST'])
def clinappoint():
    form=clin_appoint()
    if form.validate_on_submit():
        report = db.session.query(Appointments).filter(Patient.username == form.username.data).first()
        patient = db.session.query(Patient).filter_by(username=form.username.data).first()
        doctor = db.session.query(Doctor).first()
        clinician = db.session.query(Clinician).first()
        appoint=Appointments(appointments_patient=patient,
                                appointments_doctor=doctor,appointments_clinician=clinician,appointment_date=form.appointmentdate.data,appointment_type='clinician',description=form.description.data)
        db.session.add(appoint)
        db.session.commit()
        return redirect(url_for('main.home'))
    return render_template('clin_appoint.html',title="Clinician report",form=form)

@users.route("/appointment",methods=['GET','POST'])
@login_required
def appointment():
    form=AppointmentForm()
    if form.validate_on_submit():
        patient = db.session.query(Patient).filter_by(email=form.email.data).first()
        doctor = db.session.query(Doctor).first()
        clinician = db.session.query(Clinician).first()
        # doctor = db.session.query()
        current_user = form.username.data
        #pid = getattr(patient,'email')
        #patient.Appointments.append()
        appointment=Appointments(appointments_patient=patient,
                                appointments_doctor=doctor,appointments_clinician=clinician,appointment_date = form.appointmentdate.data,
                                appointment_type= "Doctor",description=form.description.data,labTestdescription="")    
        db.session.add(appointment)
        db.session.commit()
        flash('Your appointment is booked')
        return redirect(url_for('users.account'))
    return render_template('appointment.html',title='Appointment',form=form)





########### This is AI deep learning model executable functions ##############
########### Please don't rewrite code copyrights to Poojitha Arigela emailId:chinisp12@gmail.com#########

dir_path=os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER='uploads'
STATIC_FOLDER='/content/iCovidCare/APP/static/uploads/'

graph=tf.compat.v1.get_default_graph()
# #load model at very first
MODEL_PATH = '/content/iCovidCare/APP/users/bestmodel.h5'
model=keras.models.load_model(MODEL_PATH)
#call model to predict an image
#model = pickle.load(open('/content/iCovidCare/APP/bestmodel.pkl', 'rb'))
class_type = {0:'Covid',  1 : 'Normal'}

# def api(full_path):
#     data=image.load_img(full_path,target_size=(224,224,3))
#     data=np.expand_dims(data,axis=0)
    #data = image.img_to_array(data)
    #data=data*1.0/255
    #predicted = class_type[np.argmax(model.predict(data))]
    #predicted=model.predict(data)
    #return data

# #processing uploaded file and  predict it
@users.route("/predict", methods=['GET','POST'])
def upload_file():
    if request.method=='POST':
        form=request.form
        file=request.files['image']
        full_name= os.path.join(STATIC_FOLDER,file.filename)
        file.save(full_name)
        class_type = {0:'Covid',  1 : 'Normal'}
        data=image.load_img(full_name,target_size=(224,224,3))
        data=np.expand_dims(data,axis=0)
        predicted_class=np.asscalar(np.argmax(model.predict(data)))
        accuracy=model.predict(data)[0][0]*100
        acc=model.predict(data)[0][1]*100
        label=class_type[predicted_class]
        return render_template('predict.html',image_file_name=file.filename,label=label,accuracy=accuracy,acc=acc,form=form)
    return render_template('aimodel.html')
    
@users.route('/predict/<filename>')
def send_file(filename):
    return send_from_directory(STATIC_FOLDER,filename)

# @users.route("/predict", methods=['GET','POST'])
# def predict():
#     return render_template('predict.html',title='Predict')
