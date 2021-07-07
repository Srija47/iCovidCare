from flask import render_template, request, Blueprint
from flask import url_for, flash, redirect
from APP.models import Patient,Doctor,Appointments
from APP import db,mail
from flask_mail import Message
from APP.main.forms import ContactForm

main=Blueprint('main',__name__)



@main.route("/",methods=['GET','POST'])
def layout():
    if request.method=='POST':
        if request.form.get('action1')=='patient':
            return redirect(url_for('users.register'))
        elif request.form.get('action2')=='doctor':
            return redirect(url_for('users.dregister'))
        elif request.form.get('action3')=='clinician':
            return redirect(url_for('users.cregister'))
    return render_template('layout.html')


@main.route("/home")
def home():
    appointments = db.session.query(Appointments,Patient).join(Patient,Appointments.patient_id==Patient.id).all()
    doctorview = db.session.query(Appointments,Patient).join(Patient,Appointments.patient_id==Patient.id).all()
    clinicianview = db.session.query(Appointments,Patient,Doctor).join(Patient,Appointments.patient_id==Patient.id).join(Doctor,Appointments.doctor_id==Doctor.id).all()
    return render_template('home.html',appointments=appointments,doctorview=doctorview,clinicianview=clinicianview)


@main.route("/about")
def about():
    return render_template('about.html', title='About')    


@main.route("/contact",methods=['GET','POST'])
def contact():
    form=ContactForm()
    if request.method == 'POST':
        if form.validate_on_submit() == False:
            flash('All fields are required.')
            return render_template('contact.html', form=form)
        else:
            msg = Message(form.subject.data, sender='chinisp12@gmail.com', recipients=[form.email.data])
            msg.body = """
            From: %s  %s
            %s
            """ % (form.username.data, form.email.data, form.message.data)
            mail.send(msg)
        
            return render_template('contact.html', success=True)
    elif request.method == 'GET':
        return render_template('contact.html',title='contact',form=form)


@main.route('/search',methods=['GET','POST'])
def search():
    if request.method == 'POST':
        form=request.form
        search_input = form['search_input']
        search="%{0}%".format(search_input)
        doctors=db.session.query(Doctor).filter(Doctor.username.like(search)).all()
        return render_template('search.html', doctorslist= doctors,title='search')
    return render_template('layout.html')    
