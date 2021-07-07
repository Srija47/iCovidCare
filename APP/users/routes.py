from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from APP import db, bcrypt
from APP.models import User,Patient,Doctor,Clinician,Appointments,Reports
from APP.users.forms import (DoctorRegistrationForm,ClinicianRegistrationForm, upload,RegistrationForm, LoginForm,  UpdateAccountForm,AppointmentForm, ResetPasswordForm,RequestResetForm,Report,DocReport,clin_appoint)
from APP.users.utils import save_picture, send_reset_email
# from flask import send_from_directory
# from keras.models import load_model
# import numpy as np
# import tensorflow as tf
# from keras.preprocessing import image
# import matplotlib.cm as cm
# from IPython.display import Image, display


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

@users.route("/aimodel")
def aimodel():
    form=upload()
    return render_template('aimodel.html', title='AIDiagnosis',form=form)

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

# def get_img_array(img_path):
#   """
#   Input : Takes in image path as input 
#   Output : Gives out Pre-Processed image
#   """
#   path = img_path
#   img = image.load_img(path, target_size=(224,224,3))
#   img = image.img_to_array(img)
#   img = np.expand_dims(img , axis= 0 )
  
#   return img

#     # path for that new image. ( you can take it either from google or any other scource)

#     path = "/content/all_images/COVID-2118.png"       # you can add any image path

#     #predictions: path:- provide any image from google or provide image from all image folder
#     img = get_img_array(path)

#     res = class_type[np.argmax(model.predict(img))]
#     print(f"The given X-Ray image is of type = {res}")
#     print()
#     print(f"The chances of image being Covid is : {model.predict(img)[0][0]*100} percent")
#     print()
#     print(f"The chances of image being Normal is : {model.predict(img)[0][1]*100} percent")


#     # to display the image  
#     plt.imshow(img[0]/255, cmap = "gray")
#     plt.title("input image")
#     plt.show()

# # this function is udes to generate the heat map of aan image
# def make_gradcam_heatmap(img_array, model, last_conv_layer_name, pred_index=None):
#     # First, we create a model that maps the input image to the activations
#     # of the last conv layer as well as the output predictions
#     grad_model = tf.keras.models.Model(
#         [model.inputs], [model.get_layer(last_conv_layer_name).output, model.output]
#     )

#     # Then, we compute the gradient of the top predicted class for our input image
#     # with respect to the activations of the last conv layer
#     with tf.GradientTape() as tape:
#         last_conv_layer_output, preds = grad_model(img_array)
#         if pred_index is None:
#             pred_index = tf.argmax(preds[0])
#         class_channel = preds[:, pred_index]

#     # This is the gradient of the output neuron (top predicted or chosen)
#     # with regard to the output feature map of the last conv layer
#     grads = tape.gradient(class_channel, last_conv_layer_output)

#     # This is a vector where each entry is the mean intensity of the gradient
#     # over a specific feature map channel
#     pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

#     # We multiply each channel in the feature map array
#     # by "how important this channel is" with regard to the top predicted class
#     # then sum all the channels to obtain the heatmap class activation
#     last_conv_layer_output = last_conv_layer_output[0]
#     heatmap = last_conv_layer_output @ pooled_grads[..., tf.newaxis]
#     heatmap = tf.squeeze(heatmap)

#     # For visualization purpose, we will also normalize the heatmap between 0 & 1
#     heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
#     return heatmap.numpy()

# def save_and_display_gradcam(img_path , heatmap, cam_path="cam.jpg", alpha=0.4):
#     """
#     img input shoud not be expanded 
#     """

#     # Load the original image
#     img = keras.preprocessing.image.load_img(img_path)
#     img = keras.preprocessing.image.img_to_array(img)

    
#     # Rescale heatmap to a range 0-255
#     heatmap = np.uint8(255 * heatmap)

#     # Use jet colormap to colorize heatmap
#     jet = cm.get_cmap("jet")

#     # Use RGB values of the colormap
#     jet_colors = jet(np.arange(256))[:, :3]
#     jet_heatmap = jet_colors[heatmap]

#     # Create an image with RGB colorized heatmap
#     jet_heatmap = keras.preprocessing.image.array_to_img(jet_heatmap)
#     jet_heatmap = jet_heatmap.resize((img.shape[1], img.shape[0]))
#     jet_heatmap = keras.preprocessing.image.img_to_array(jet_heatmap)

#     # Superimpose the heatmap on original image
#     superimposed_img = jet_heatmap * alpha + img
#     superimposed_img = keras.preprocessing.image.array_to_img(superimposed_img)

#     # Save the superimposed image
#     superimposed_img.save(cam_path)

#     # Display Grad CAM
#     display(Image(cam_path))

# # function that is used to predict the image type and the ares that are affected by covid


# def image_prediction_and_visualization(path,last_conv_layer_name = "conv5_block3_3_conv", model = model):
#   """
#   input:  is the image path, name of last convolution layer , model name
#   output : returs the predictions and the area that is effected
#   """
  
#   img_array = get_img_array(path)

#   heatmap = make_gradcam_heatmap(img_array, model, last_conv_layer_name)

#   plt.title("the heat map of the image is ")
#   plt.imshow(heatmap)
#   plt.show()
#   print()
#   img = get_img_array(path)

#   res = class_type[np.argmax(model.predict(img))]
#   print(f"The given X-Ray image is of type = {res}")
#   print()
#   print(f"The chances of image being Covid is : {model.predict(img)[0][0]*100} %")
#   print(f"The chances of image being Normal is : {model.predict(img)[0][1]*100} %")

#   print()
#   print("image with heatmap representing region on interest")

#   # function call
#   save_and_display_gradcam(path, heatmap)

#   print()
#   print("the original input image")
#   print()

#   a = plt.imread(path)
#   plt.imshow(a, cmap = "gray")
#   plt.title("Original image")
#   plt.show()

#   #predictions
# # provide the path of any image from google or any other scource 
# # the path is already defigned above , but you can also provide the path here to avoid scrolling up 

# # for covid image :  path:- provide any image from google or provide image from all image folder
# path = "/content/all_images/COVID-2118.png"

# image_prediction_and_visualization(path)

# # for normal image :  path:- provide any image from google or provide image from all image folder
# path = "/content/all_images/train_test_split/validation/Normal/Normal-10024.png"

# image_prediction_and_visualization(path)

# # for a healthey chest x-Ray heap map will be white thus the x-ray will look blue

# @app.route("/diagnosis")
# def diagnosis():
#     return render_template('diagnosis.html')

# # dir_path=os.path.dirname(os.path.realpath(__file__))
# # #UPLOAD_FOLDER=dir_path+'/uploads'
# # #STATIC_FOLDER=dir_path+'/static'
# UPLOAD_FOLDER='uploads'
# # STATIC_FOLDER='static'

# # graph=tf.get_default_graph()
# # withgraph.as_default():
# # #load model at very first
# # model=load_model(STATIC_FOLDER+'/'+'bestmodel.h5')
# #call model to predict an image
# def api(full_path):
# #     data=image.load_img(full_path,target_size=(150,150,3))
# #     data=np.expand_dims(data,axis=0)
# #     data=data*1.0/255

# #     withgraph.as_default():
# #     predicted=model.predict(data)
# #     return predicted

# #processing uploaded file and  predict it
# @app.route('/upload',methods=['POST','GET'])
# def upload_file():
#     if request.method=='GET':
#         return render_template('diagnosis.html')
#     else:
#         file=request.files['image']
#         full_name=os.path.join(UPLOAD_FOLDER,file.filename)
#         file.save(full_name)
#         indices={0:'PNEUMONIA',1:'NORMAL',2:'Invasive carcinomar',3:'Normal'}
#         result=api(full_name)
#         predicted_class=np.asscalar(np.argmax(result,axis=1))
#         accuracy=round(result[0][predicted_class]*100,2)
#         label=indices[predicted_class]
#         return render_template('predict.html',image_file_name=file.filename,label=label,accuracy=accuracy)

# @app.route('/uploads/<filename>')
# def send_file(filename):
#     return send_from_directory(UPLOAD_FOLDER,filename)
