import pandas as pd 
import polars as pl
import mysql.connector
from flask import Flask, render_template


db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "projects123123",
    database = "Patient_management_system"
    
    
    )

cursor = db.cursor()
# table = Patient_info
# table Appointments
# table Billing

cursor.execute("DELETE FROM Patient_info WHERE Patient_ID IS NULL AND Name IS NULL AND Age IS NULL AND Sex IS NULL AND Medical_record_number IS NULL AND diagnosis IS NULL ")
db.commit()


app = Flask(__name__)

# Write a function that returns patient info table

@app.route("/")
def patient_information_table():
    cursor.execute("SELECT * FROM Patient_info")
    cursor.description
    
    col_name_list = []
    row_list = []
    remove_duplicate_list = []
    
    for i in cursor.description:
        column_names = i[0]
        col_name_list.append(column_names)
        
        
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
        
        
if __name__ == "__main__":
    app.run()

