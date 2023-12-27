from flask import Flask, render_template, request, redirect,url_for,session
from flask_mail import Mail, Message
from backend_addfns import *
from backend_login import *
from backendviewfns import *

from templates import *


app = Flask(__name__)
app.secret_key ='ursecrectkey'


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'ur_gmail'
app.config['MAIL_PASSWORD'] = 'ur_password'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

@app.route('/')
def home():
    return redirect('/login')
@app.route('/login')
def render_login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    user_id, status = authenticate(username, password)
    print(user_id,status)
    if user_id and status:
        session['user']=user_id
        if status == 'admin':
            return redirect('/admin')  # Redirect to admin dashboard
        elif status == 'healthcare professional':
            return redirect('/healthcare_dashboard')  # Redirect to healthcare professional dashboard
        elif status == 'patient':
            return redirect('/patient_dashboard')  # Redirect to patient dashboard
        elif status == 'government official':
            return redirect('/governmentofficial')  # Redirect to government official dashboard
    else:
        return "Invalid username or password"  # You can render an error page if needed



# Render admin dashboard (you can create similar routes for other dashboards)
@app.route('/admin')
def render_governmentofficial():
    return render_template('admin.html')

@app.route('/addgovernmentofficial')
def render_addgovtofficial():
    return render_template('add_government_official.html')

@app.route('/addgovernmentofficial',methods=['POST'])
def addgovtofficial():
    name=request.form['name']
    position=request.form['position']
    contactno=request.form['contactno']
    email=request.form['email']
    adharno=request.form['adharno']
    
    pswrd=add_government_official(name, position, contactno, email, adharno)
    msg = Message(f"Login credentials", sender='clinic.management.system.service@gmail.com', recipients=[email])
    msg.body = f'Dear {name},\n \tYou have been added as a government official to nasha mukthi portal.\nPlease use the  username(your adhar no)\t{adharno} and password  {pswrd}"'
    
    mail.send(msg)
    return render_template('add_government_official.html')

@app.route('/addhealthcareprof')
def render_addhealthcareprof():
    return render_template('add_healthcare_professional.html')

@app.route('/addhealthcareprof',methods=['POST'])
def addhealthcareprof():
    name=request.form['name']
    facilityname=request.form['facilityname']
    designation=request.form['designation']
    contactno=request.form['contactno']
    email=request.form['email']
    adharno=request.form['adharno']
    
    pswrd=add_healthcare_prof(name,facilityname,designation, contactno, email, adharno)
    msg = Message(f"Login credentials", sender='clinic.management.system.service@gmail.com', recipients=[email])
    msg.body = f'Dear {name},\n \tYou have been added as a healthcare professional to nasha mukthi portal.\nPlease use the  username(your adhar no)\t{adharno} and password  {pswrd}"'
    
    mail.send(msg)
    return render_template('add_healthcare_professional.html')

@app.route('/governmentofficial')
def render_govtoff():
    return render_template('governmentofficial.html')

@app.route('/addfacility')
def render_addfacility():
    return render_template('addfacility.html')

@app.route('/addfacility',methods=['POST'])
def additionoffacility():
    location=request.form['location']
    name=request.form['name']
    contactno=request.form['contactno']
    contactperson=request.form['contactperson']
    state=request.form['state']
    
    add_facility(location, name, contactno, contactperson, state)
    msg = Message('New Facility Added', sender='clinic.management.system.service@gmail.com', recipients=['piriyadharshini2210418@ssn.edu.in'])
    msg.body = f'New Facility Details:\nLocation: {location}\nName: {name}\nContact Number: {contactno}\nContact Person: {contactperson}\nState: {state}'
    
    mail.send(msg)
    return render_template('addfacility.html')

@app.route('/healthcare_dashboard')
def render_healthcareprof():
    return render_template('healthcare.html')

@app.route('/addpatient')
def render_addpatient():
    return render_template('addpatient.html')

@app.route('/addpatient',methods=['POST'])
def addpatient():
    name=request.form['name']
    age=request.form['age']
    sex=request.form['sex']
    contactno=request.form['contactno']
    email=request.form['email']
    adharno=request.form['adharno']
    pswrd=add_patient(name, age, sex, contactno, email, adharno)
    msg = Message('Login credentials', sender='clinic.management.system.service@gmail.com', recipients=[email])

    msg.body = f'Dear {name},\n \tYou have been added as a patient to nasha mukthi portal.\nPlease use the  username(your adhar no)\t{adharno} and password  {pswrd}"'
    
    mail.send(msg)
    return render_template('addpatient.html')

@app.route('/patient_dashboard')
def render_patient():
    return render_template('patient.html')

@app.route('/viewpatientprofile')
def viewpatient():
    print('viewing')
    login_id=session.get('user')
    print(login_id)
    user_details=view_patient(login_id)
    print(user_details)
    return render_template('patientview.html', user_details=user_details)

@app.route('/addtreatmentdetails')
def render_addtreatment():
    return render_template('addtreatmentdetails.html')

@app.route('/addtreatmentdetails',methods=['POST'])
def add_treatment():
    hid=session.get('user')
    print(hid)
    patientname=request.form['patient_name']
    facility_name=request.form['facility_name']
    aadhar_no=request.form['aadhar_no']
    start_date=request.form['start_date']
    status=request.form['status']
    drug_name=request.form['drug_name']
    treatment_method=request.form['treatment_method']

    add_treatment_details(hid,patientname,facility_name, aadhar_no, start_date, status, drug_name, treatment_method)
    return render_template('addtreatmentdetails.html')
@app.route('/viewtreatmentdetails')
def view_treatment():
    login_id=session.get('user')
    treatment_details=view_treatmentdetails(login_id)
    if treatment_details:
        drug_name, treatment_method, facility_name, healthcare_professional, start_date, status = treatment_details
       
        return render_template('viewtreatmentdetails.html',
                               drug_name=drug_name, treatment_method=treatment_method,
                               facility_name=facility_name, healthcare_professional=healthcare_professional,
                               start_date=start_date, status=status)
    else:
        return "No treatment details found for the provided login ID."
    
@app.route('/facilities_by_state')
def show_facilities_by_state():
    facilities_by_state = get_facilities_by_state()
    return render_template('facilityofcenter.html', facilities_by_state=facilities_by_state)

@app.route('/treatment_stats')
def treatment_stats():
    returnedvalues=stats()
    xvalues=['WOMEN REACHED OUT','YOUTH REACHED OUT','PATIENTS REACHED OUT']
    yvalues=[returnedvalues[0][0]['WomenReachedOut']],returnedvalues[1][0]['YouthReachedOut'],returnedvalues[2][0]['TotalPatientsReachedOut']
    return render_template('barchart.html',
                           xvalues=xvalues, yvalues=yvalues)
if __name__ == '__main__':
    app.run(debug=True)
