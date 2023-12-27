import mysql.connector
import random
import string

def generate_default_password():
    random_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))  # Generates an 8-character random string
    return 'p' + random_password

def add_patient(name, age, sex, contact_no, email, adhar_no):
    mydb = mysql.connector.connect(
          host="localhost",
          user="root",
          password="pdk164@#",
          database="NashaMukti"
      )
    cursor = mydb.cursor()

    default_password=generate_default_password()
    # Insert into login table
    cursor.execute("INSERT INTO login (id,username, password, status) VALUES (%s,%s, %s, %s)",
                   (0,adhar_no, default_password, "patient"))
    mydb.commit()

    login_id = cursor.lastrowid  # Get the auto-generated login id

    # Insert into Patient table
    cursor.execute("INSERT INTO Patient (Name, Age, Sex, ContactNo, Email, LoginID) VALUES (%s, %s, %s, %s, %s, %s)",
                   (name, age, sex, contact_no, email, login_id))
    mydb.commit()

    cursor.close()
    mydb.close()
    return default_password

def add_facility(location, fname, contact_no, contact_person, state):
    mydb = mysql.connector.connect(
          host="localhost",
          user="root",
          password="pdk164@#",
          database="NashaMukti"
      )
    cursor = mydb.cursor()

    # Insert into Facility table
    cursor.execute("INSERT INTO Facility (FID,Location, FName, ContactNo, ContactPerson, State) VALUES (%s, %s, %s, %s, %s,%s)",
                   (0,location, fname, contact_no, contact_person, state))
    mydb.commit()

    cursor.close()
    mydb.close()
def add_government_official(name, position, contact_no, email, adhar_no):
    mydb = mysql.connector.connect(
          host="localhost",
          user="root",
          password="pdk164@#",
          database="NashaMukti"
      )
    cursor = mydb.cursor()

    default_password = generate_default_password()
    
    # Insert into login table
    cursor.execute("INSERT INTO login (id,username, password, status) VALUES (%s,%s, %s, %s)",
                   (0, adhar_no, default_password, "government official"))
    mydb.commit()

    login_id = cursor.lastrowid  # Get the auto-generated login id

    # Insert into GovernmentOfficial table
    cursor.execute("INSERT INTO GovernmentOfficial (GOID,Name, Position, ContactNo, Email, LoginID) VALUES (%s, %s, %s, %s, %s,%s)",
                   (0,name, position, contact_no, email, login_id))
    mydb.commit()

    cursor.close()
    mydb.close()

    return default_password
def add_healthcare_prof(name,facilityname,designation, contact_no, email, adhar_no):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="pdk164@#",
            database="NashaMukti"
        )
        cursor = mydb.cursor(buffered=True)

        default_password = generate_default_password()

        

        # Insert into login table
        cursor.execute("INSERT INTO login (id,username, password, status) VALUES (%s,%s, %s, %s)",
                    (0, adhar_no, default_password, "healthcare professional"))
        mydb.commit()

        # Get the login_id
        login_id = cursor.lastrowid 
        # Get the auto-generated login id
        cursor.execute("SELECT FID FROM Facility WHERE FName = %s", (facilityname,))
        facility_id = cursor.fetchone()[0]
        # Insert into healthcareprofessional table
        cursor.execute("INSERT INTO healthcareprofessional (HID,Name, Designation, ContactNo, Email, LoginID, FACID) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (0, name, designation, contact_no, email, login_id, facility_id))
        mydb.commit()

        cursor.close()
        mydb.close()

        return default_password

import mysql.connector

def add_treatment_details(id,patientname,facility_name, aadhar_no, start_date, status, drug_name, treatment_method):
    # Connect to the database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="pdk164@#",
        database="NashaMukti"
    )
    cursor = mydb.cursor()
    if id is not None:
        cursor.execute("SELECT HID  FROM healthcareprofessional WHERE LoginID = %s", (id,))
        hid = cursor.fetchone()[0]
        # Step 1: Get Facility ID
        cursor.execute("SELECT fid FROM Facility WHERE fname = %s", (facility_name,))
        facility_id = cursor.fetchone()

        if facility_id is not None:
            facility_id = facility_id[0]

            # Step 2: Get Login ID using Aadhar Number
            cursor.execute("SELECT id FROM login WHERE username = %s", (aadhar_no,))
            login_id = cursor.fetchone()

            if login_id is not None:
                login_id = login_id[0]

                # Step 3: Get Patient ID using Login ID
                cursor.execute("SELECT pid FROM Patient WHERE LoginID = %s", (login_id,))
                patient_id = cursor.fetchone()

                if patient_id is not None:
                    patient_id = patient_id[0]

                    # Step 4: Insert Treatment Details
                    cursor.execute("INSERT INTO treatmentdetails(TDID,HealthcareProfessionalID, FacilityID, PatientID,DrugName,TreatmentMethod,StartDate, status) VALUES ( %s, %s, %s, %s, %s, %s,%s,%s)",
                                (0,hid,facility_id, patient_id,drug_name,treatment_method, start_date, status))

                    # Commit the changes
                    mydb.commit()

                    # Close the cursor and connection
                    cursor.close()
                    mydb.close()
                    return "Treatment details added successfully."
                else:
                    return "Patient ID not found."
            else:
                return "Login ID not found."
        else:
            return "Facility ID not found."
    else:
        return "HID is not found"


     