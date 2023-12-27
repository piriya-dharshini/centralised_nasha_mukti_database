import mysql.connector


def view_patient(login_id):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="pdk164@#",
        database="NashaMukti"
    )
    cursor = mydb.cursor(dictionary=True)

    cursor.execute("SELECT Name, Age, Sex, ContactNo, Email FROM Patient WHERE LoginID = %s", (login_id,))
    patient = cursor.fetchone()

    cursor.close()
    mydb.close()

    return patient

def view_treatmentdetails(loginid):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="pdk164@#",
        database="NashaMukti"
    )
    cursor = mydb.cursor()

    # Execute the SQL query to get treatment details
    cursor.execute("""
        SELECT td.DrugName, td.TreatmentMethod, f.FName AS FacilityName, 
               hp.Name AS HealthcareProfessional, td.StartDate, td.Status
        FROM TreatmentDetails td
        JOIN Facility f ON td.FacilityID = f.FID
        JOIN HealthcareProfessional hp ON td.HealthcareProfessionalID = hp.HID
        JOIN Patient p ON td.PatientID = p.PID
        JOIN Login l ON p.LoginID = l.id
        WHERE l.id = %s
    """, (loginid,))

    treatment_details = cursor.fetchone()

    cursor.close()
    mydb.close()
    return treatment_details

def get_facilities_by_state():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="pdk164@#",
        database="NashaMukti"
    )
    cursor = mydb.cursor()

    cursor.execute("""
        SELECT State, GROUP_CONCAT(FName SEPARATOR ', ') AS Facilities
        FROM Facility
        GROUP BY State
    """)

    facilities_by_state = cursor.fetchall()

    cursor.close()
    mydb.close()

    return facilities_by_state

def stats():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="pdk164@#",
        database="NashaMukti"
    )
    cursor = mydb.cursor(dictionary=True)

    # Execute the queries to get the treatment statistics
    cursor.execute("""
        SELECT 
               COUNT(*) AS WomenReachedOut
        FROM TreatmentDetails TD
        JOIN Patient P ON TD.PatientID = P.PID
        WHERE P.Sex = 'F'
    """)

    women_reached_out = cursor.fetchall()

    cursor.execute("""
        SELECT 
               COUNT(*) AS YouthReachedOut
        FROM TreatmentDetails TD
        JOIN Patient P ON TD.PatientID = P.PID
        WHERE P.Age BETWEEN 18 AND 30
    """)

    youth_reached_out = cursor.fetchall()

    cursor.execute("""
        SELECT 
               COUNT(*) AS TotalPatientsReachedOut
        FROM TreatmentDetails

    """)

    total_patients_reached_out = cursor.fetchall()
    print(women_reached_out,youth_reached_out,total_patients_reached_out)
    cursor.close()
    mydb.close()
    return women_reached_out,youth_reached_out,total_patients_reached_out

stats()