import pandas as pd 
import polars as pl
import mysql.connector
from flask import Flask, render_template
from flask import request
import json

# Creating a connection to my database
db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "password",
    database = "Patient_management_system" 
    )

# Creating a cursor object
cursor = db.cursor()
# table = Patient_info
# table Appointments
# table Billing


# Initialising app
app = Flask(__name__)

# Write a function that returns patient info table

# Function/Endpoint that retrieves patient information 
@app.route("/")
def patient_information_table():
    cursor.execute("SELECT * FROM Patient_info")
    cursor.description
    
    col_name_list = []
    row_list = []
    remove_duplicate_list = []
    
    # Getting all column names
    for i in cursor.description:
        column_names = i[0]
        col_name_list.append(column_names)
        
    # Getting all rows
    all_rows = cursor.fetchall()
    
    # Loop over all the rows and create an empty dictionary
    # Now have the col names as keys and rows as values
    for row in all_rows:
        row_dict = {}
        
        for col_name, value in zip(col_name_list, row):
            row_dict[col_name] = value
            
            row_list.append(row_dict)
            
            
    for index, row in enumerate(row_list):
        if index % 6 < 1:
            remove_duplicate_list.append(row)
    
            
    return render_template("index.html", data = remove_duplicate_list)



# Creating a function/endpoint that registers/adds patient to the database
@app.route("/add_patient", methods = ["GET", "POST"])
def add_patient():
    with db.cursor() as cursor:
        patient_id = request.form.get("Patient_ID")
        name = request.form.get("Name")
        age = request.form.get("Age")
        sex = request.form.get("Sex")
        mrn = request.form.get("Medical_record_number")
        diagnosis = request.form.get("diagnosis")
        
        cursor.execute("INSERT INTO Patient_info (Patient_ID, Name, Age, Sex, Medical_record_number, diagnosis)"
                       "VALUES (%s, %s, %s, %s, %s, %s)",
                       (patient_id, name, age, sex, mrn, diagnosis)
                       
                       )
            
        db.commit()
        
        return render_template("add_patient.html")
    
# Creating a function/endpoint that renders patient info based on Patient ID 
@app.route("/edit_patient_details/<patient_id>", methods=["GET", "POST"])
def get_patient_details(patient_id):
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM Patient_info WHERE Patient_ID = %s", (patient_id, ))
        patient_details = cursor.fetchone()

        col_names = [name[0] for name in cursor.description]    
        to_dict = dict(zip(col_names, patient_details))
        
        return render_template("edit_details.html", patient_details=[to_dict])
   


# Creating a function/endpoint that updates patient information based on Patient ID
@app.route("/edit_patient_details/<patient_id>", methods = ["GET", "POST"])
def update_patient_details(patient_id):
    with db.cursor() as cursor:
            new_patient_id = request.form.get("Patient_ID")
            name = request.form.get("Name")
            age = request.form.get("Age")
            sex = request.form.get("Sex")
            mrn = request.form.get("Medical_record_number")
            diagnosis = request.form.get("diagnosis")
            
            cursor.execute("UPDATE Patient_info SET Patient_ID = %s , Name = %s, Age = %s, Sex = %s, Medical_record_number = %s, diagnosis = %s WHERE Patient_ID = %s" ,
                           (new_patient_id, name, age, sex , mrn, diagnosis, patient_id))
            
            
            db.commit()              
            
    return render_template("edit_details.html")
            
            
if __name__ == "__main__":
    app.run(debug = True, use_reloader = False)
    
    
        
    
    
    
