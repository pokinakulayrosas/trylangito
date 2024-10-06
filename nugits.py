from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session, render_template_string
from flask_pymongo import PyMongo
from flask_cors import CORS
from flask_mail import Mail, Message

from bson import ObjectId
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from bson.json_util import dumps
import logging
import pytz
import random
import os
import base64
import traceback

from model import UserSchema, LoginSchema, ForVerification

from createToken import createToken

# Setup logging
logging.basicConfig(level=logging.DEBUG)

MONGODB_URI="mongodb+srv://elijahcobarrubias034:iZfMkoxoHYFiFHWI@nugitscluster.m4kd8.mongodb.net/Nugits?retryWrites=true&w=majority&appName=NugitsCluster&serverSelectionTimeoutMS=30000&socketTimeoutMS=30000"
        
app = Flask("__name__")
app.secret_key="secret_key"
CORS(app)

app.permanent_session_lifetime = timedelta(minutes=30)

UPLOAD_FOLDER = 'static/assets'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config["MONGO_URI"] = MONGODB_URI
mongo = PyMongo(app)
events = mongo.db.events
usersDB = mongo.db.usersDB
students = mongo.db.students


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'jhcb0503@gmail.com'
app.config['MAIL_PASSWORD'] = 'csqt ttrd qqqz ywuy'
app.config['MAIL_DEFAULT_SENDER'] = 'jhcb0503@gmail.com'
mail = Mail(app)


USERNAME="admin"
PASSWORD="root"

FACULTYNAME = "faculty"
FACULTYPASS = "login"

UPLOAD_FOLDER = 'C:\\Users\\Senju\\Downloads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['STATIC_FOLDER'] = 'static'

#ORGANIZER ROUTES

# ROUTES
# ROUTESAUTH
# ROUTESUSER
# ROUTESADMIN
# ROUTESFACULTY

# FUNCTIONS
# FUNCTIONSAUTH
# FUNCTIONSUSER
# FUNCTIONSADMIN
# FUNCTIONSFACULTY

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
        
        
@app.route('/upload_logo', methods=['POST'])
def upload_logo():
    current_user = session.get('username')
    if not current_user:
        return {'success': False, 'message': 'User not logged in'}, 403
    
    if 'logo' not in request.files:
        return {'success': False, 'message': 'No file part'}, 400
    
    file = request.files['logo']
    
    if file.filename == '':
        return {'success': False, 'message': 'No selected file'}, 400

    if file and allowed_file(file.filename):
        image_data = base64.b64encode(file.read()).decode('utf-8')
        
        print("Image data length:", len(image_data))
        
        mongo.db.savedProfile.update_one(
            {'form1.email': current_user},
            {'$set': {'logo': image_data}},
            upsert=True
        )
        
        return {'success': True, 'message': 'Logo uploaded successfully!'}
    
    return {'success': False, 'message': 'Invalid file type'}, 400

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}
        
        
@app.route("/testConnection")
def testConnection():
    try:
        mongo.cx.admin.command('ping')
        return "Connected to the Database"
    except Exception as e:
        return "Error: " + str(e)
        

    
# ROUTESAUTH

        
@app.route("/")
def logindex():
    return render_template('Login.html')

@app.route("/register")
def regdex():
    return render_template('Registration.html')

@app.route("/forgotpassword")
def forgotpassword():
    return render_template('Forgotten/ForgotPassword.html')

@app.route("/faculty/login")
def prof_login():
    return render_template('Professors/FacultyLogin.html')

@app.route("/faculty/register")
def prof_register():
    return render_template("Professors/FacultyRegister.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('prof_login'))

@app.route('/keep-alive', methods=['POST'])
def keep_alive():
    session.permanent = True
    return '', 204

# ROUTESUSER - FUNCTIONSUSER



@app.route("/home")
def home():
    
    current_user = session.get('username')
    
    if current_user:
        
        home = mongo.db.verifiedUsers.find_one({'email': session['username']})
        
        response = list(mongo.db.appointmentResponse.find({'studentEmail': current_user}))
        
        events = mongo.db.events.find()
        
        saved = mongo.db.savedProfile.find_one({'form1.email': current_user})
        
        logo = saved['logo'] if saved and 'logo' in saved else None

        if home:
            return render_template('Home.html', home=home, email=session['username'], saved=saved, logo=logo, events=events, response = response)
        else:
            return render_template('NotFound.html')
    else:
        return redirect(url_for('logindex'))
        

@app.route("/profile")
def profile_user():
    current_user = session.get('username')
    
    if current_user:
        profile = mongo.db.verifiedUsers.find_one({'email': current_user})
        saved = mongo.db.savedProfile.find_one({'form1.email': current_user})

        logo = saved['logo'] if saved and 'logo' in saved else None

        has_saved_data = saved is not None
        

        if profile:
            return render_template('Profile.html', profile=profile, email=current_user, saved=saved, has_saved_data=has_saved_data, logo=logo)
        else:
            return render_template('NotFound.html')
    else:
        return redirect(url_for("logindex"))

# @app.route("/journal")
# def journal_user():
    
#     current_user = session.get('username')
    
#     if current_user:
        
#         journal = mongo.db.verifiedUsers.find_one({'email': session['username']})
        
#         saved = mongo.db.savedProfile.find_one({'form1.email': current_user})
        
#         logo = saved['logo'] if saved and 'logo' in saved else None
        
#         if journal:
#             return render_template('Journal.html', journal = journal, email=session['username'], saved=saved, logo=logo)
#         else:
#             return "User not found", 404

#     else:
#         return redirect(url_for('logindex'))
    
@app.route("/journals")
def journals():
    
    current_user = session.get('username')
    
    if current_user:
        
        journal = mongo.db.verifiedUsers.find_one({'email': session['username']})
        
        saved = mongo.db.savedProfile.find_one({'form1.email': current_user})
        
        journal_entries = mongo.db.journal.find({'username': current_user})
        
        logo = saved['logo'] if saved and 'logo' in saved else None
        
        if journal:
            return render_template('NewJournal.html', journal = journal, email=session['username'], saved=saved, logo=logo, entries=journal_entries)
        else:
            return render_template('NotFound.html')

    else:
        return redirect(url_for('logindex'))
  
@app.route("/calendar")
def Calendar():
    
    current_user = session.get('username')
    
    if current_user:
        
        calendar = mongo.db.verifiedUsers.find_one({'email': session['username']})
        
        saved = mongo.db.savedProfile.find_one({'form1.email': current_user})

        logo = saved['logo'] if saved and 'logo' in saved else None
        
        if calendar:
            return render_template('Calendar.html', calendar = calendar, email=session['username'], saved=saved, logo=logo)
        else:
            return render_template('NotFound.html')

    else:
        return redirect(url_for('logindex'))
    
      
  
@app.route("/smartchat")
def smartchat():
    
    current_user = session.get('username')
    
    if current_user:
        Smartchat = mongo.db.verifiedUsers.find_one({'email': session['username']})
        
        saved = mongo.db.savedProfile.find_one({'form1.email': current_user})

        logo = saved['logo'] if saved and 'logo' in saved else None
        
        if Smartchat:
            return render_template('Smartchat.html', smartchat = Smartchat, email=session['username'], saved=saved, logo=logo)
        else:
            return render_template('NotFound.html')
    else:
        return redirect(url_for('logindex'))
    
@app.route("/clearance")
def clearance():
    current_user = session.get('username')
    
    if current_user:
        clearance = mongo.db.verifiedUsers.find_one({'email': session['username']})
        
        saved = mongo.db.savedProfile.find_one({'form1.email': current_user})

        logo = saved['logo'] if saved and 'logo' in saved else None
        
        if clearance:
            return render_template('Clearance.html', clearance = clearance, email=session['username'], saved=saved, logo=logo)
        else:
            return render_template('NotFound.html')
    else:
        return redirect(url_for('logindex'))   

@app.route("/ScheduleViewer")
def ScheduleViewer():
    current_user = session.get('username')
   
    if current_user:
        schedule = mongo.db.verifiedUsers.find_one({'email': current_user})
       
        saved = mongo.db.savedProfile.find_one({'form1.email': current_user})
       
        counselor = mongo.db.scheduleViewer.find()
        response = list(mongo.db.appointmentResponse.find({'studentEmail': current_user}))
        
        logo = saved['logo'] if saved and 'logo' in saved else None
       
        if schedule:
            return render_template('ScheduleViewer.html', schedule=schedule, email = session['username'], saved = saved, logo = logo, counselor = counselor, response = response)
        else:
            return render_template('NotFound.html')
    else:
        return redirect(url_for('logindex'))

@app.route("/meditation")
def meditation():
    current_user = session.get('username')
    
    if current_user:
        meditation = mongo.db.verifiedUsers.find_one({'email': current_user})
        
        saved = mongo.db.savedProfile.find_one({'form1.email': current_user})
        
        logo = saved['logo'] if saved and 'logo' in saved else None
        
        if meditation:
            return render_template('Meditation.html', meditation=meditation, email = session['username'], saved = saved, logo = logo)
        else:
            return render_template('NotFound.html')
    else:
        return redirect(url_for('logindex'))

#OVERVIEW

@app.route("/meditation/videos")
def videos():
    current_user = session.get('username')
    
    if current_user:
        meditation = mongo.db.verifiedUsers.find_one({'email': current_user})
        
        saved = mongo.db.savedProfile.find_one({'form1.email': current_user})
        
        logo = saved['logo'] if saved and 'logo' in saved else None
        
        if meditation:
            return render_template('Videos.html', meditation=meditation, email = session['username'], saved = saved, logo = logo)
        else:
            return render_template('NotFound.html')
    else:
        return redirect(url_for('logindex'))

@app.route("/meditation/audio")
def audio():
    current_user = session.get('username')
    
    if current_user:
        meditation = mongo.db.verifiedUsers.find_one({'email': current_user})
        
        saved = mongo.db.savedProfile.find_one({'form1.email': current_user})
        
        logo = saved['logo'] if saved and 'logo' in saved else None
        
        if meditation:
            return render_template('Audio.html', meditation=meditation, email = session['username'], saved = saved, logo = logo)
        else:
            return render_template('NotFound.html')
    else:
        return redirect(url_for('logindex'))

@app.route("/smart/overview")
def smartoverview():
    return render_template('SmartOverview.html')

@app.route("/NUMOA_GSO/overview")
def gsooverview():
    return render_template('GSOOverview.html')

@app.route("/NUMOA_Peers/overview")
def peersoverview():
    return render_template('PeersOverview.html')

#GALLERY

@app.route("/NUMOA_halloween2022/galleryOne")
def galleryOne():
    return render_template('galleryOne.html')

@app.route("/NUMOA_partnerships/galleryTwo")
def galleryTwo():
    return render_template('galleryTwo.html')

@app.route("/NUMOA_summer2024/galleryThree")
def galleryThree():
    return render_template('galleryThree.html')



#ADMIN SIDE
# ROUTESADMIN - FUNCTIONSADMIN



@app.route("/dashboard")
def index():
    if 'username' in session:
        
        faculty = mongo.db.facultyRegistration.count_documents({})
        
        student = mongo.db.verifiedUsers.count_documents({})
        
        total = faculty + student
        
        referralList = mongo.db.profReferrals.find()
        
        return render_template("Admin/dashboard.html", faculty = faculty, student = student, total = total, referrals = referralList)
    
    
    return redirect(url_for('logindex'))

@app.route("/dashboard/profile")
def profile():
    return render_template("Admin/pages/profile.html")

@app.route("/dashboard/faculty/profile")
def faculty_profile():
    return render_template("Admin/pages/facultyProfile.html")

@app.route("/dashboard/referral")
def referralResponse():
    return render_template("Admin/referral.html")
    
@app.route("/dashboard/addform")
def addForm():
    return render_template("Admin/pages/addUserForm.html")

@app.route("/admin/schedule")
def eventsu():
    return render_template("Admin/pages/events.html")


@app.route("/admin/journal/<email>", methods=['GET'])
def journalad(email):
    journal_entries = list(mongo.db.journal.find({'username': email}))
    
    return render_template('Admin/journal.html', entries=journal_entries, email=email)

@app.route("/schedule/setter")
def schedulead():
    
    schedule = mongo.db.scheduleViewer.find()
    
    return render_template("Admin/schedule.html", schedule = schedule)

@app.route("/admin/clearance")
def requirementsad():
    return render_template("Admin/requirements.html")

@app.route("/admin/appointments")
def appointmentsad():
    return render_template("Admin/appointments.html")

@app.route("/account")
def accountad():
    return render_template("Admin/account.html")

@app.route("/admin/feedback")
def feedbackad():
    
    feedback = mongo.db.feedback.find().sort('timestamp', -1)
    
    return render_template("Admin/feedback.html", feedback = feedback)

@app.route("/background")
def background():
    return render_template("Admin/pages/informations/background.html")

@app.route("/background/smart")
def smart():
    return render_template("Admin/pages/informations/journal2.html")

@app.route("/background/nojournal")
def norespond():
    return render_template("Admin/pages/none/nojournal.html")

@app.route("/journal/noappointment")
def noappointment():
    return render_template("Admin/pages/none/noappointment.html")



#FACULTY SIDE

# ROUTESFACULTY - FUNCTIONSFACULTY


    

@app.route("/professor/dashboard")
def prof_dashboard():
    
    
    current_faculty = session.get('user')
    
    if current_faculty:
        
        faculty = mongo.db.facultyRegistration.find_one({'email': current_faculty})
        
        referrals = list(mongo.db.profReferrals.find({'form1.email': current_faculty}))
        
        curtotal = mongo.db.profReferrals.count_documents({})
        
        if faculty:
            return render_template('Professors/professorDashboard.html', faculty=faculty, email=session['user'], referrals=referrals, total = curtotal )
        else:
            return "User not found", 404
    else:
        return redirect(url_for('prof_login'))        



@app.route("/professor/referral_form")
def referral_form():
    
    current_user = session.get('user')
    
    if current_user:
        
        userEmail = mongo.db.facultyRegistration.find_one({'email': session['user']})
        
        referral = mongo.db.profReferrals.find_one({'form1.email': current_user})
        
        
        if userEmail:
            return render_template('Professors/referralForm.html', email=current_user, username = userEmail, referral = referral)
        else:
            return "User not found", 404
    else:
        return redirect(url_for('prof_login'))  


#under maintenance
@app.route("/professor/recent_referrals")
def recent_referrals():
    if 'user' not in session:
        return redirect(url_for('prof_login'))
    
    user_id = session.get('user')
    
    try:
        user = mongo.db.facultyRegistration.find_one({'_id': ObjectId(user_id)})
        
        if user:
            referrals = mongo.db.referrals.find({'professor_id': user_id})
            referrals_list = list(referrals)
            return jsonify(referrals_list)
        else:
            return jsonify([])
    except Exception as e:
        print(f'Error fetching referrals: {e}')
        return jsonify([])


    

    
# @app.route("/faculty_response/<faculty_id>")
# def faculty_response(faculty_id):
#     try:
        
#         faculty = mongo.db.facultyRegistration.find_one({'_id': ObjectId(faculty_id)})

#         if faculty:
#             return render_template('Admin/pages/informations/referralResponse.html', faculty=faculty)
#         else:
#             return "Referral not found", 404

#     except Exception as e:
#         print(f'Error: {e}')
#         return "An error occurred", 500    



#FUNCTIONS


# FUNCTIONSAUTH - ROUTESAUTH




@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        color = request.form.get("color")
        
        if email == USERNAME and password == PASSWORD:
            session['username'] = email
            session.permanent = True
            return redirect(url_for("index"))
        elif email == FACULTYNAME and password ==FACULTYPASS:
             session['username'] = email
             session.permanent = True
             return redirect(url_for("prof_login"))
        elif mongo.db.verifiedUsers.find_one({"email": email, "password": password}):
            session['username'] = email
            mongo.db.colors.insert_one({'email': email, 'color': color})
            session.permanent = True
            return redirect(url_for("home")) 
        else:
            error = "Incorrect username or password. Please try again."
            return render_template("Login.html", error=error)  
    else:
        return render_template("Login.html")



#FOR REGISTRATION
@app.route("/register", methods=["GET", "POST"])
def registration():
    if request.method == "POST":
        email = request.form["email"]  # email of user

        if mongo.db.verifiedUsers.find_one({"email": email}) or mongo.db.forVerification.find_one({"email": email}):
            return render_template('Registration.html', messages="Email already exists")
            
        verification_token = createToken()  # create token
        msg = Message("Email Verification", recipients=[email])  # message to be sent

        # HTML content for the email
        html_content = render_template_string("""
        <html>
        <body>
            <h1>Email Verification</h1>
            <p>Please verify your email by clicking the link below:</p>
            <a href="http://127.0.0.1:5000/email-verified?token={{verification_token}}&email={{email}}">Verify Email</a>
        </body>
        </html>
        """, verification_token=verification_token, email=email)
        
        msg.html = html_content
        try:
            mail.send(msg)
            # If we reach this point, the email was sent successfully
            verificationInformation = {
                "email": email,
                "token": verification_token,
                "isVerified": False
            }

            verificationCollection = mongo.db.forVerification.insert_one(verificationInformation)
            print(verificationCollection.inserted_id)

            # Redirect to a page prompting user to check their email
            return render_template('verifyEmail.html', email=email)
        
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            return f'Email not sent {str(e)}', 500

    return render_template('Registration.html')
    
# FOR EMAIL VERIFICATION
@app.route("/verify-email")
def verify_email(email):
    
    return render_template('verifyEmail.html', email=email)


# EMAIL VERIFIED
@app.route("/email-verified", methods=["GET", "POST"])
def email_verified():
    email = request.args.get("email")
    token = request.args.get("token")

    if request.method == "POST":
        firstName = request.form["firstName"]
        lastName = request.form["lastName"]
        middleName = request.form["middleName"]
        studentID = request.form["studentID"]
        department = request.form["department"]
        password = request.form["password"]

        userInformation = {
            "email": email,
            "firstName": firstName,
            "lastName": lastName,
            "middleName": middleName,
            "studentID": studentID,
            "department": department,
            "password": password,
            "status": "Verified"
        }
        
        insertVerifiedUser = mongo.db.verifiedUsers.insert_one(userInformation)

        if insertVerifiedUser.inserted_id:
            # Check if the token is valid
            verification_collection = mongo.db.forVerification
            verification_data = verification_collection.delete_many({"email": email})

            return redirect(url_for('login'))

    return render_template('emailVerified.html', email=email)


@app.route('/faculty_auth', methods=['POST'])
def faculty_auth():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        
        if mongo.db.facultyRegistration.find_one({'email': email, 'password': password}):
            session['user'] = email
            session.permanent = True
            return redirect(url_for('prof_dashboard'))
        else:
            error = "Incorrect username or password. Please try again."
            return render_template('Professors/FacultyLogin.html', error = error)
    else:
        return render_template('Professors/FacultyLogin.html')

@app.route("/faculty/register", methods=['GET', 'POST'])
def faculty_registration():
    if request.method == "POST":
        email = request.form["email"]  # email of user

        if mongo.db.facultyRegistration.find_one({"email": email}) or mongo.db.forVerification.find_one({"email": email}):
            return render_template('Professors/FacultyRegister.html', messages="Email already exists")
            
        verification_token = createToken()  # create token
        msg = Message("Email Verification", recipients=[email])  # message to be sent

        # HTML content for the email
        html_content = render_template_string("""
        <html>
        <body>
            <h1>Email Verification</h1>
            <p>Please verify your email by clicking the link below:</p>
            <a href="http://127.0.0.1:5000/faculty-verified?token={{verification_token}}&email={{email}}">Verify Email</a>
        </body>
        </html>
        """, verification_token=verification_token, email=email)
        
        msg.html = html_content
        try:
            mail.send(msg)
            # If we reach this point, the email was sent successfully
            verificationInformation = {
                "email": email,
                "token": verification_token,
                "isVerified": False
            }

            verificationCollection = mongo.db.forVerification.insert_one(verificationInformation)
            print(verificationCollection.inserted_id)

            # Redirect to a page prompting user to check their email
            return render_template('Professors/FacultyVerify.html', email=email)
        
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            return f'Email not sent {str(e)}', 500

    return render_template('Professors/FacultyRegister.html')
    
@app.route("/faculty/verify")
def facultyVerify(email):
    
    return render_template('Professors/FacultyVerify.html', email=email)

@app.route("/faculty-verified", methods=["GET", "POST"])
def facultyVerified():
    email = request.args.get("email")
    token = request.args.get("token")

    if request.method == "POST":
        firstName = request.form["firstName"]
        lastName = request.form["lastName"]
        middleName = request.form["middleName"]
        facultyID = request.form["facultyID"]
        department = request.form["department"]
        password = request.form["password"]

        userInformation = {
            "email": email,
            "firstName": firstName,
            "lastName": lastName,
            "middleName": middleName,
            "facultyID": facultyID,
            "department": department,
            "password": password,
            "status": "Verified"
        }
        
        insertVerifiedUser = mongo.db.facultyRegistration.insert_one(userInformation)

        if insertVerifiedUser.inserted_id:
            # Check if the token is valid
            verification_collection = mongo.db.forVerification
            verification_data = verification_collection.delete_many({"email": email})

            return redirect(url_for('prof_login'))

    return render_template('Professors/VerifiedFaculty.html', email=email)
    
# For Reset password

@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form["email"]
        if mongo.db.verifiedUsers.find_one({"email": email}):
            verification_token = createToken()
            msg = Message("Password Reset Verification", recipients=[email])
            html_content = render_template_string("""
            <html>
            <body>
                <h1>Password Reset Verification</h1>
                <p>Please verify your email by clicking the link below:</p>
                <a href="http://127.0.0.1:5000/reset-password?token={{token}}&email={{email}}">Reset Password</a>
            </body>
            </html>
            """, token=verification_token, email=email)
            msg.html = html_content
            
            mail.send(msg)
            # Store token logic here...
            return render_template('Forgotten/checkEmail.html', email=email)
        else:
            return render_template('ForgotPassword.html', error="Email not found.")
    
    return render_template('Forgotten/ForgotPassword.html')

@app.route("/check-email")
def checkEmail(email):
    
    return render_template('Forgotten/checkEmail.html', email=email)

@app.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    email = request.args.get("email")
    token = request.args.get("token")

    if request.method == "POST":
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]

        if new_password == confirm_password:
            # Update the password in the database
            mongo.db.verifiedUsers.update_one({"email": email}, {"$set": {"password": new_password}})
            return redirect(url_for("login"))
        else:
            return render_template('ResetPassword.html', email=email, error="Passwords do not match.", token=token)

    return render_template('Forgotten/ResetPassword.html', email=email, token=token)



    
    
# ROUTESUSER - FUNCTIONSUSER



@app.route('/feedback_form', methods=['POST'])
def feedback_form():
    
    try:
        data = request.get_json()
        
        data['timestamp'] = datetime.utcnow()

        result = mongo.db.feedback.insert_one(data)

        return jsonify({'success': True, 'id': str(result.inserted_id)}), 201
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500



@app.route('/smartchat_form', methods=['POST'])
def smartchat_form():
    try:
        data = request.get_json()
        
        data['timestamp'] = datetime.utcnow()

        result = mongo.db.smartchat.insert_one(data)

        return jsonify({'success': True, 'id': str(result.inserted_id)}), 201
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500
    
    

@app.route("/clearance_form", methods=['POST'])
def clearance_form():
    try:
        data = request.get_json()
        
        data['timestamp'] = datetime.utcnow()
        
        local_tz = pytz.timezone('Asia/Manila')
        data['datetime'] = datetime.now(local_tz)
        
        result = mongo.db.clearance.insert_one(data)
        
        return jsonify({'success': True, 'id': str(result.inserted_id)}), 201
    
    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'success': False, 'message': str(e)}), 500
    
    
@app.route("/profile_user_db", methods=['POST'])
def profile_user_db():
    try:
        data = request.get_json()
        
        data['timestamp'] = datetime.utcnow()
        
        local_tz = pytz.timezone('Asia/Manila')
        data['datetime'] = datetime.now(local_tz)
        
        result = mongo.db.savedProfile.insert_one(data)
        
        return jsonify({'success': True, 'id': str(result.inserted_id)}), 201
    
    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'success': False, 'message': str(e)}), 500
    
@app.route('/journal_db', methods=['POST'])
def journal_db():
    date = request.form['date']
    mood = request.form['mood']
    title = request.form['title']
    notes = request.form['note']
    
    username = session.get('username')

    mongo.db.journal.insert_one({
        'date': date,
        'mood': mood,
        'title': title,
        'notes': notes,
        'username': username
    })

    return redirect(url_for('journals'))

@app.route('/edit_journal/<entry_id>', methods=['GET'])
def edit_journal(entry_id):
    current_user = session.get('username')
    
    if current_user:
        entry = mongo.db.journal.find_one({'_id': ObjectId(entry_id), 'username': current_user})
        profile = mongo.db.verifiedUsers.find_one({'email': current_user})
        saved = mongo.db.savedProfile.find_one({'form1.email': current_user})

        logo = saved['logo'] if saved and 'logo' in saved else None
        if entry:
            return render_template('Journal.html', entry=entry, journal = profile, logo=logo)
        else:
            return "Entry not found", 404
    else:
        return redirect(url_for('journals'))
    
@app.route('/update_journal/<entry_id>', methods=['POST'])
def update_journal(entry_id):
    date = request.form['date']
    mood = request.form['mood']
    title = request.form['title']
    notes = request.form['note']
    
    current_user = session.get('username')
    
    mongo.db.journal.update_one(
        {'_id': ObjectId(entry_id), 'username': current_user},
        {'$set': {
            'date': date,
            'mood': mood,
            'title': title,
            'notes': notes
        }}
    )

    return redirect(url_for('journals'))


@app.route('/delete_journal/<entry_id>', methods=['POST'])
def delete_journal(entry_id):
    current_user = session.get('username')
    
    if current_user:
        mongo.db.journal.delete_one({'_id': ObjectId(entry_id), 'username': current_user})
        return redirect(url_for('journals'))  # Redirect back to the journals page
    else:
        return redirect(url_for('logindex'))

    
    
# ROUTESADMIN - FUNCTIONSADMIN


@app.route('/dashboard/colors', methods=['GET'])
def get_colors():
    pipeline = [
        {
            "$group": {
                "_id": "$color",
                "count": {"$sum": 1}
            }
        }
    ]
    colors = mongo.db.colors.aggregate(pipeline)
    color_data = [{"color": color["_id"], "count": color["count"]} for color in colors]
    return jsonify(color_data)


@app.route("/api/events/one", methods=["GET"])
def getOneEvent():
    try:            
        new_id = request.args.get("new_id")

        # Find the event with the specified ID
        event = events.find_one({"new_id": new_id}, {'_id': False})

        if event:
            return jsonify(event), 200
        else:
            return jsonify({"message": "Event not found"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
@app.route("/api/schedule", methods=["GET"])
def get_schedule():
    selected_date = request.args.get("date")
    if not selected_date:
        return jsonify({"error": "Date parameter is missing"}), 400

    schedule_data = list(events.find({"date": selected_date}, {'_id': False}))
    if not schedule_data:
        return jsonify([])
        
    return jsonify(schedule_data)

@app.route("/api/schedule/all", methods=["GET"])
def getAllEvents():
    selected_month = request.args.get("month")
    selected_year = request.args.get("year")

    logging.debug(f"Selected Month: {selected_month}, Selected Year: {selected_year}")

    if not selected_month or not selected_year:
        return jsonify({"error": "Month and year parameters are required"}), 400

    try:
        selected_month = int(selected_month)
        selected_year = int(selected_year)
    except ValueError:
        return jsonify({"error": "Month and year must be integers"}), 400

    start_date = datetime(selected_year, selected_month, 1)
    if selected_month == 12:
        end_date = datetime(selected_year + 1, 1, 1) - timedelta(days=1)
    else:
        end_date = datetime(selected_year, selected_month + 1, 1) - timedelta(days=1)

    logging.debug(f"Start Date: {start_date.strftime('%m/%d/%Y')}, End Date: {end_date.strftime('%m/%d/%Y')}")

    schedule_data = list(events.find({
        "date": {"$gte": start_date.strftime('%m/%d/%Y'), "$lte": end_date.strftime('%m/%d/%Y')}
    }, {'_id': False}))

    logging.debug(f"Schedule Data: {schedule_data}")

    if not schedule_data:
        return jsonify([]) 

    return jsonify(schedule_data)



@app.route("/api/events", methods=["POST"])
def add_event():
    data = request.json
    eventID = data.get("_id")
    title = data.get("title")
    time = data.get("time")
    date = data.get("date")
    
    events.insert_one({"new_id" : eventID, "title": title, "time": time, "date": date})
    
    return jsonify({"message": "Event added successfully"}), 201

@app.route("/api/students", methods=["POST"])
def studentsInfo():
    _json = request.json
    _studId = _json ['studentID']
    _name = _json['name']
    _dept = _json['department']
    _section = _json['section']
    
    if _studId and _name and _dept and _section and request.method == 'POST':
        
        id = mongo.db.students.insert_one({'studentID':_studId, 'name':_name, 'department':_dept, 'section':_section})
        
        resp = jsonify('User added successfully')
        
        resp.status_code = 200
        
        return resp
    
    else:
        return not_found()
    
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'Status': 404,
        'Message': 'Not found' + request.url
    }
    resp = jsonify(message)
    
@app.route('/api/get/students')
def users():
    students = mongo.db.students.find()
    resp = dumps(students)
    return resp

@app.route('/api/get/faculty')
def faculty_users():
    faculty = mongo.db.facultyRegistration.find()
    resp = dumps(faculty)
    return resp

@app.route('/api/get/student', methods=['GET'])
def get_student_details():
    student_id = request.args.get('_id')
    student = mongo.db.students.find_one({'_id': ObjectId(student_id)})
    if student:
        student['_id'] = str(student['_id'])
        return jsonify(student)
    else:
        return jsonify({'error': 'Student not found'}), 404

@app.route("/api/events/<new_id>", methods=["DELETE"])
def delete_event(new_id):
    try:
        new_id = request.args.get("new_id")
        deleted_event = events.find_one_and_delete({"new_id": str(new_id)})
        print(new_id)
        if deleted_event:
            return jsonify({"theEvent": deleted_event, "message": "Successfully deleted the entry"}), 200
        else:
            return jsonify({"message": "Event not found"}), 404
    except Exception as e:
        return jsonify({"message": "Something went wrong", "error": str(e)}), 500

@app.route("/api/events", methods=["DELETE"])
def delete_events():
    try:
        title = request.args.get('title')
        new_id = request.args.get('new_id')

        if title:
            deleted_event = events.find_one_and_delete({"title": title})
        elif new_id:
            deleted_event = events.find_one_and_delete({"new_id": new_id})
        else:
            return jsonify({"message": "Please provide 'title' or 'new_id' parameter"}), 400

        if deleted_event:
            return jsonify({"message": "Event deleted successfully"}), 200
        else:
            return jsonify({"message": "Event not found"}), 404
    except Exception as e:
        return jsonify({"message": "Failed to delete event", "error": str(e)}), 500

@app.route("/api/schedule/all/events", methods=["GET"])
def get_all_events():
    # getting all of the events
    all_events = list(events.find({}, {'_id': False}))
    return jsonify(all_events)

@app.route("/appointment_table", methods=['GET'])
def appointment_table():

    search_query = request.args.get('query', '')  
    
    try:
        query = {
            '$or': [
                {'form1.fullname': {'$regex': search_query, '$options': 'i'}},
                {'form5.email': {'$regex': search_query, '$options': 'i'}},
                {'form3.studentnumber': {'$regex': search_query, '$options': 'i'}},
                {'form3.strand': {'$regex': search_query, '$options': 'i'}},
                {'form3.section': {'$regex': search_query, '$options': 'i'}}
            ]
        }

        referrals = mongo.db.smartchat.find(query).sort('timestamp', -1)
        referral_list = []
        
        for referral in referrals:
            referral['_id'] = str(referral['_id'])

            referral_list.append(referral)
        

        return jsonify(referral_list), 200

    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'success': False, 'message': 'An error occurred'}), 500

@app.route("/appointment_response/<appointment_id>")
def appointment_response(appointment_id):
    try:
        appointment = mongo.db.smartchat.find_one({'_id': ObjectId(appointment_id)})

        if appointment:
            # Get the email using the correct field name
            email = appointment.get('form5', {}).get('email')
            print(f"Email extracted from appointment: {email}")  # Debugging

            # Find responses by the correct email field
            responses = mongo.db.appointmentResponse.find({'studentEmail': email})
            responses_list = list(responses)  # Convert cursor to list
            
            print(f"Responses found: {responses_list}")  # Debugging

            appointment['responseSubmitted'] = len(responses_list) > 0
            
            response_data = []
            for response in responses_list:
                response_data.append({
                    'name': response.get('counselorName', ''),
                    'date': response.get('date', ''),
                    'modality': response.get('modality', ''),
                    'room': response.get('room', ''),
                    'status': response.get('status', 'N/A')
                })
            
            return render_template(
                'Admin/pages/informations/appointmentResponse.html',
                appointment=appointment,
                responses=response_data
            )
        else:
            return "Appointment not found", 404

    except Exception as e:
        print(f'Error: {e}')
        return "An error occurred", 500
    
@app.route("/clearance_table", methods=['GET'])
def clearance_table():
    try:
        search_query = request.args.get('search', '')
        
        query = {
            '$or': [
                {'form.student_number': {'$regex': search_query, '$options': 'i'}},
                {'form.first_name': {'$regex': search_query, '$options': 'i'}},
                {'form.last_name': {'$regex': search_query, '$options': 'i'}},
                {'form.email': {'$regex': search_query, '$options': 'i'}},
                {'form.contact_number': {'$regex': search_query, '$options': 'i'}},
                {'form.reason': {'$regex': search_query, '$options': 'i'}}
            ]
        }
        
        # Fetch and sort results
        referrals = mongo.db.clearance.find(query).sort('timestamp', -1)
        
        referral_list = []
        
        for referral in referrals:
            referral['_id'] = str(referral['_id'])

            referral_list.append(referral)

        return jsonify(referral_list), 200

    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'success': False, 'message': 'An error occurred'}), 500


@app.route("/profile_table", methods=['GET'])
def profile_table():
    
    search_query = request.args.get('search', '')
    
    try:
        
        query = {
            '$or': [
                {'email': {'$regex': search_query, '$options': 'i'}},
                {'firstName': {'$regex': search_query, '$options': 'i'}},
                {'lastName': {'$regex': search_query, '$options': 'i'}},
                {'studentID': {'$regex': search_query, '$options': 'i'}},
                {'department': {'$regex': search_query, '$options': 'i'}}
            ]
        }
        
        referrals = mongo.db.verifiedUsers.find(query).sort('timestamp', -1)
        
        referral_list = []
        
        for referral in referrals:
            referral['_id'] = str(referral['_id'])

            referral_list.append(referral)

        return jsonify(referral_list), 200

    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'success': False, 'message': 'An error occurred'}), 500


@app.route("/profile_response/<profile_id>")
def profile_response(profile_id):
    try:
        profile = mongo.db.verifiedUsers.find_one({'_id': ObjectId(profile_id)})

        if profile:
            email = profile.get('email')

            saved = mongo.db.savedProfile.find_one({'form1.email': email})
            
            appointments = mongo.db.smartchat.find({'form5.email': email})
            
            logo = saved['logo'] if saved and 'logo' in saved else None

            return render_template('Admin/pages/informations/background.html', profile=profile, saved=saved, logo=logo, appointments = appointments)
        else:
            return "Profile not found", 404

    except Exception as e:
        print(f'Error: {e}')
        return "An error occurred", 500

@app.route('/appointment_modal/response', methods=['POST'])
def appointment_modal():
    data = request.json

    data['timestamp'] = datetime.utcnow()

    mongo.db.appointmentResponse.insert_one(data)

    appointment_id = data['smartchatID']
    mongo.db.smartchat.update_one(
        {'_id': ObjectId(appointment_id)},
        {'$set': {'responseSubmitted': True}}
    )

    return jsonify({"message": "Data saved successfully!"}), 201

@app.route('/update-appointment', methods=['POST'])
def update_appointment_route():
    student_email = request.form.get('studentEmail')
    counselor_name = request.form.get('name')
    date = request.form.get('date')
    modality = request.form.get('modality')
    room = request.form.get('room')
    status = request.form.get('status')

    try:
        result = mongo.db.appointmentResponse.update_one(
            {'studentEmail': student_email},
            {
                '$set': {
                    'counselorName': counselor_name,
                    'date': date,
                    'modality': modality,
                    'room': room,
                    'status': status
                }
            }
        )

        if result.modified_count > 0:
            return jsonify({'message': 'Appointment updated successfully!'}), 200
        else:
            return jsonify({'message': 'No changes made or appointment not found.'}), 400
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/scheduleViewer/response', methods=['POST'])
def scheduleViewer_modal():
    data = request.json
 
    data['timestamp'] = datetime.utcnow()
 
    mongo.db.scheduleViewer.insert_one(data)
 
    return jsonify({"message": "Data saved successfully!"}), 201
   
    
@app.route("/tangina", methods=['GET'])
def tangina():
    search_query = request.args.get('search', '')

    try:
        query = {
            '$or': [
                {'email': {'$regex': search_query, '$options': 'i'}},
                {'firstName': {'$regex': search_query, '$options': 'i'}},
                {'lastName': {'$regex': search_query, '$options': 'i'}},
                {'facultyID': {'$regex': search_query, '$options': 'i'}},
                {'department': {'$regex': search_query, '$options': 'i'}}
            ]
        }

        referrals = mongo.db.facultyRegistration.find(query).sort('timestamp', -1)
        
        referral_list = []

        for referral in referrals:
            referral['_id'] = str(referral['_id'])
            
            referral_list.append(referral)

        return jsonify(referral_list), 200

    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'success': False, 'message': 'An error occurred'}), 500
    

# ROUTESFACULTY - FUNCTIONSFACULTY





@app.route("/referral_form_db", methods=['POST'])
def referral_form_db():
    try:
        data = request.get_json()
        
        data['timestamp'] = datetime.utcnow()

        if not data or not isinstance(data, dict):
            raise ValueError("Invalid data received")
        result = mongo.db.profReferrals.insert_one(data)

        return jsonify({'success': True, 'id': str(result.inserted_id)}), 201
    
    except ValueError as ve:
        print(f'ValueError: {ve}')
        return jsonify({'success': False, 'message': 'Invalid data received'}), 400
    
    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'success': False, 'message': 'An error occurred'}), 500

@app.route("/referral_response/<referral_id>")
def referral_response(referral_id):
    try:
        referral = mongo.db.profReferrals.find_one({'_id': ObjectId(referral_id)})

        if referral:
            return render_template('Admin/pages/informations/referralResponse.html', referral=referral)
        else:
            return "Referral not found", 404

    except Exception as e:
        print(f'Error: {e}')
        return "An error occurred", 500
    
@app.route("/referral_table", methods=['GET'])
def referrals_table():
    search_query = request.args.get('search', '').strip()
    
    try:
        query = {}
        if search_query:
            query = {
                '$or': [
                    {'form1.fullname': {'$regex': search_query, '$options': 'i'}},
                    {'form2.studFname': {'$regex': search_query, '$options': 'i'}},
                    {'form2.college': {'$regex': search_query, '$options': 'i'}},
                    {'_id': {'$regex': search_query, '$options': 'i'}}
                ]
            }
        
        referrals = mongo.db.profReferrals.find(query).sort('timestamp', -1)
        
        referral_list = []
        
        for referral in referrals:
            referral['_id'] = str(referral['_id'])
            if 'date' in referral:
                referral['date'] = referral['date'].strftime('%Y-%m-%d') if isinstance(referral['date'], datetime) else referral['date']
            else:
                referral['date'] = 'N/A'
    
            referral_list.append(referral)

        return jsonify(referral_list), 200

    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'success': False, 'message': 'An error occurred'}), 500
    
@app.route("/referral_table_dashboard", methods=['GET'])
def referrals_table_dashboard():
    try:
        search_query = request.args.get('search', '').strip()

        current_user_foreign_id = session.get('foreign_id')

        query_filter = {
            '$and': [
                {'foreignID': current_user_foreign_id},
                {
                    '$or': [
                        {'form2.studFname': {'$regex': search_query, '$options': 'i'}},
                        {'form1.fname': {'$regex': search_query, '$options': 'i'}},
                        {'form1.lname': {'$regex': search_query, '$options': 'i'}},
                        {'form2.college': {'$regex': search_query, '$options': 'i'}},
                        {'form2.date': {'$regex': search_query, '$options': 'i'}},
                        {'_id': {'$regex': search_query, '$options': 'i'}}
                    ]
                }
            ]
        }

        referrals = mongo.db.profReferrals.find(query_filter).sort('timestamp', -1)

        referral_list = []

        for referral in referrals:
            referral['_id'] = str(referral['_id'])
            if 'date' in referral:
                referral['date'] = referral['date'].strftime('%Y-%m-%d')
            else:
                referral['date'] = 'N/A'

            referral_list.append(referral)

        return jsonify(referral_list), 200

    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'success': False, 'message': 'An error occurred'}), 500


@app.route("/faculty_table", methods=['GET'])
def faculty_table():
    
    search_query = request.args.get('search', '')
    
    try:
        
        query = {
            '$or': [
                {'email': {'$regex': search_query, '$options': 'i'}},
                {'firstName': {'$regex': search_query, '$options': 'i'}},
                {'lastName': {'$regex': search_query, '$options': 'i'}},
                {'studentID': {'$regex': search_query, '$options': 'i'}},
                {'department': {'$regex': search_query, '$options': 'i'}}
            ]
        }
        
        referrals = mongo.db.facultyRegistration.find(query).sort('timestamp', -1)
        
        referral_list = []
        
        for referral in referrals:
            referral['_id'] = str(referral['_id'])

            referral_list.append(referral)

        return jsonify(referral_list), 200

    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'success': False, 'message': 'An error occurred'}), 500
    

if __name__=="__main__":
    app.run(debug=True)
    
