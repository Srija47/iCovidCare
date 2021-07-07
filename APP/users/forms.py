from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField,RadioField,IntegerField,TextAreaField
from wtforms.widgets.core import CheckboxInput
from wtforms.fields.core import DateField
from datetime import date
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from APP.models import User
from APP.models import User,Doctor,Clinician





class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)],
                           render_kw={"placeholder":"Username"})
    email = StringField('Email',
                        validators=[DataRequired(), Email()],
                        render_kw={"placeholder":"Email"})
    password = PasswordField('Password', 
                                        validators=[DataRequired()],
                                        render_kw={"placeholder":"Password"})
    confirm_password = PasswordField('Confirm Password',
                                    validators=[DataRequired(), EqualTo('password')],
                                    render_kw={"placeholder":"Re-enter your password"})
    gender= RadioField('Gender',
                                choices=[('M','Male'),('F','Female')])
    age= IntegerField('Age',
                            validators=[DataRequired()],
                            render_kw={"placeholder":"Age"})
    address= TextAreaField('Address',
                                    validators=[DataRequired()],
                                    render_kw={"placeholder":"Address"})
    phonenumber= IntegerField('Phonenumber',
                                            validators=[DataRequired()],
                                            render_kw={"placeholder":"Phonenumber"})
    submit = SubmitField('Sign Up')

    def validate_username(self,username):
        user= User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please a choose a different one.')
    
    def validate_email(self,email):
        user= User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please a choose a different one.')


class DoctorRegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)],
                           render_kw={"placeholder":"Username"})
    email = StringField('Email',
                        validators=[DataRequired(), Email()],
                        render_kw={"placeholder":"Email"})
    password = PasswordField('Password', 
                                        validators=[DataRequired()],
                                        render_kw={"placeholder":"Password"})
    confirm_password = PasswordField('Confirm Password',
                                    validators=[DataRequired(), EqualTo('password')],
                                    render_kw={"placeholder":"Re-enter your password"})
    designation= StringField('designation',
                                    validators=[DataRequired()],
                                    render_kw={"placeholder":"Designation"})
    speciality= StringField('speciality',
                                          validators=[DataRequired()],
                                          render_kw={"placeholder":"Speciality"})
    phonenum= IntegerField('Phonenumber',
                                            validators=[DataRequired()],
                                            render_kw={"placeholder":"Phonenumber"})
    location= StringField('location',
                                        validators=[DataRequired()],
                                        render_kw={"placeholder":"Location"})
    submit = SubmitField('Sign Up')

    def validate_username(self,username):
        doctor=Doctor.query.filter_by(username=username.data).first()
        if doctor:
            raise ValidationError('That username is already taken! Please choose a new one')
    def validate_email(self,email):
        doctor=Doctor.query.filter_by(email=email.data).first()
        if doctor:
            raise ValidationError('That email is already taken! Please choose a new one')
    

class ClinicianRegistrationForm(FlaskForm):
    name = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)],
                           render_kw={"placeholder":"Username"})
    email = StringField('Email',
                        validators=[DataRequired(), Email()],
                        render_kw={"placeholder":"Email"})
    password = PasswordField('Password', 
                                        validators=[DataRequired()],
                                        render_kw={"placeholder":"Password"})
    confirm_password = PasswordField('Confirm Password',
                                    validators=[DataRequired(), EqualTo('password')],
                                    render_kw={"placeholder":"Re-enter your password"})
    phonenum= IntegerField('Phonenumber',
                                            validators=[DataRequired()],
                                            render_kw={"placeholder":"Phonenumber"})
    location= StringField('location',
                                        validators=[DataRequired()],
                                        render_kw={"placeholder":"Location"})
    submit = SubmitField('Sign Up')
    def validate_name(self,name):
        clinician=Clinician.query.filter_by(name=name.data).first()
        if clinician:
            raise ValidationError('That username is already taken! Please choose a new one')
    def validate_email(self,email):
        clinician=Clinician.query.filter_by(email=email.data).first()
        if clinician:
            raise ValidationError('That email is already taken! Please choose a new one')
    



class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()],
                        render_kw={"placeholder":"Email"})
    password = PasswordField('Password', 
                                        validators=[DataRequired()],
                                        render_kw={"placeholder":"Password"})
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')



class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)],
                           render_kw={"placeholder":"Username"})
    email = StringField('Email',
                        validators=[DataRequired(), Email()],
                        render_kw={"placeholder":"Email"})
    picture=FileField('Update Profile Picture',
                                               validators=[FileAllowed(['jpg', 'png'])])
    status = CheckboxInput()
    submit = SubmitField('Update')

    def validate_username(self,username):
        if username.data!= current_user.username:
            user= User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please a choose a different one.')
    
    def validate_email(self,email):
        if email.data!= current_user.email:
            user= User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please a choose a different one.')

class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()],
                        render_kw={"placeholder":"Email"}) 
    submit=SubmitField('Request Password Reset')

    def validate_email(self,email):
        user= User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', 
                                        validators=[DataRequired()],
                                        render_kw={"placeholder":"Password"})
    confirm_password = PasswordField('Confirm Password',
                                    validators=[DataRequired(), EqualTo('password')],
                                    render_kw={"placeholder":"Re-enter your password"})
    submit=SubmitField('Reset Password')


class AppointmentForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)],
                           render_kw={"placeholder":"Username"})
    email = StringField('Email',
                        validators=[DataRequired(), Email()],
                        render_kw={"placeholder":"Email"})
    gender= RadioField('Gender',
                                choices=[('M','Male'),('F','Female')])
    age= IntegerField('Age',
                            validators=[DataRequired()],
                            render_kw={"placeholder":"Age"})
    address= TextAreaField('Address',
                                    validators=[DataRequired()],
                                    render_kw={"placeholder":"Address"})
    phonenumber= IntegerField('Phonenumber',
                                            validators=[DataRequired()],
                                            render_kw={"placeholder":"Phonenumber"})
    appointmentdate=DateField('Date',
                                    validators=[DataRequired()],
                                    render_kw={"placeholder":"Enter Date"},
                                    default=date.today())
    description=TextAreaField('Description',
                                        validators=[DataRequired()],
                                        render_kw={"placeholder":"Describe your symptoms"})
    
    submit=SubmitField('Book an Appointment')

class ReportForm(FlaskForm):
    patient_username=StringField('Patientname',validators=[DataRequired()])
    doctor_username=StringField('Doctorname',validators=[DataRequired()])
    description=TextAreaField('description',validators=[DataRequired])
    report=TextAreaField('Report',validators=[DataRequired()])
    submit=SubmitField('Submit')

class Report(FlaskForm):
    username=StringField('Username',validators=[DataRequired()],
                                    render_kw={"placeholder":"Enter patient name"})
    report=StringField('Report',validators=[DataRequired()],
                                    render_kw={"placeholder":"Report either person have covid or not"})
    description=TextAreaField('Description',validators=[DataRequired()],
                                            render_kw={"placeholder":"Describe report in few lines for better understanding"})
    submit=SubmitField('Send Report')

class DocReport(FlaskForm):
    patientname=StringField('Patientname',validators=[DataRequired()],
                                            render_kw={"placeholder":"Enter name of the patient"})
    description=TextAreaField('Description',
                                        validators=[DataRequired()],
                                        render_kw={"placeholder":"Describe patient symptoms"})
    appointmentdate=DateField('Date',
                                    validators=[DataRequired()],
                                    render_kw={"placeholder":"Enter Date"},
                                    default=date.today())
    labTestdescription=TextAreaField('Report',validators=[DataRequired()],
                                    render_kw={"placeholder":"Needs x-ray or not"})          
    prescription=TextAreaField('prescription',
                                        validators=[DataRequired()],
                                        render_kw={"placeholder":"Suggest medicines based on health condition"})                      
    submit=SubmitField('Send Report')


class upload(FlaskForm):
     picture=FileField('Upload X-Ray',
                                    validators=[FileAllowed(['jpg', 'png','pdf','xml'])])


class clin_appoint(FlaskForm):
    username=StringField('Username',validators=[DataRequired()],
                                    render_kw={"placeholder":"Enter patient name"})
    appointmentdate=DateField('Date',
                                    validators=[DataRequired()],
                                    render_kw={"placeholder":"Enter Date"},
                                    default=date.today())
    description=StringField('Description',validators=[DataRequired()],
                                            render_kw={"placeholder":"Description"})
    submit=SubmitField('Book Appointment')    