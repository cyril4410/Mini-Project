from flask import Flask, render_template, request, redirect, url_for, flash
import pymongo
import os
from datetime import datetime


client=pymongo.MongoClient("mongodb://localhost:27017")
app = Flask(__name__)
app.secret_key = os.urandom(24)
db = client.hospital_management
patients_collection = db.patients
doctor_collection = db.doctors
prescriptions_collection = db.prescriptions
@app.route('/login/doctor_home/out_patient/add_patient', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        patient_data = {
            'patient_id': request.form['patient_id'],
            'patient_name': request.form['patient_name'],
            'age': int(request.form['age']),
            'patient_dob': request.form['patient_dob'],
            'gender': request.form['gender']
        }
        patients_collection.insert_one(patient_data)
        flash('Patient details added successfully.', 'success')
        return redirect(url_for('doctor_home'))

    return render_template('add_patient.html')

@app.route('/login/doctor_home')
def doctor_home():
    
    return render_template('doctor_home.html')


doctor_users = {
    "Sahami": "123",
    "Nandana": "456"
}

patient_users = {
    "Bala": "xyz",
    "Cyril": "abc"
}


@app.route('/', methods=['GET', 'POST'])
def login():
    doctor_error = ""
    patient_error = ""
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_type = request.form['user_type']
        if user_type == 'doctor':
            if username in doctor_users and doctor_users[username] == password:
                return render_template('doctor_home.html', user_type=user_type, username=username)
            else:
                doctor_error = 'Invalid doctor credentials. Please try again.'
        elif user_type == 'patient':
            if username in patient_users and patient_users[username] == password:
                return render_template('patient_home.html', user_type=user_type, username=username)
            else:
                patient_error = 'Invalid patient credentials. Please try again.'

    return render_template('login.html', doctor_error=doctor_error, patient_error=patient_error)
def get_patient_by_id(patient_id):
    return patients_collection.find_one({'patient_id': patient_id})

def get_patients_by_name(patient_name):
    return patients_collection.find({'patient_name': {'$regex': patient_name, '$options': 'i'}})

def get_all_patients():
    return patients_collection.find()
@app.route('/login/doctor_home/out_patient/view_patient', methods=['GET', 'POST'])
def view_patients():
    patients = get_all_patients()
    if request.method == 'POST':
        search_type = request.form['search_type']
        search_query = request.form['search_query']

        if search_type == 'patient_id':
            patient = get_patient_by_id((search_query))
            patients = [patient] if patient else []
        elif search_type == 'patient_name':
            patients = get_patients_by_name(search_query)
    return render_template('view_patient.html', patients=patients)
@app.route('/modify_view/<patient_id>')
def modify_view(patient_id):
    patient = get_patient_by_id(patient_id)  # Fetch patient details from the database
    if patient:
        return render_template('modify_view.html', patient=patient)  # Pass patient details to the template
    else:
        # Handle the case where the patient is not found
        flash('Patient not found.', 'error')
@app.route('/patient_details/<patient_id>')
def patient_details(patient_id):
    patient = patients_collection.find_one({'patient_id':(patient_id)})
    if patient:
        return render_template('patient_details.html', patient=patient)
    else:
        flash('Patient with the specified ID not found.', 'error')
        return redirect(url_for('view_patient'))
@app.route('/login/doctor_home/out_patient/modify_patient_records/modify_view/<patient_id>/add_prescription', methods=['GET', 'POST'])
def add_prescription(patient_id):
    if request.method == 'POST':
        prescription_details ={
            'prescription_id': request.form['prescription_id'],
            'patient_id': patient_id,
            'doctor_name': request.form['doctor_name'],
            'date_added': datetime.now(),
            'diagnosed_disease': request.form['diagnosed_disease'],
            'medications': []
        }

        medication_count = int(request.form['medication_count'])
        for i in range(1, medication_count + 1):
            medication = {
                'medication': request.form[f'medication_{i}'],
                'dosage': request.form[f'dosage_{i}'],
                'frequency': request.form[f'frequency_{i}'],
                'period': request.form[f'period_{i}']
                # Add more fields as needed
            }
            prescription_details['medications'].append(medication)
        prescriptions_collection.insert_one(prescription_details)

        flash('Prescription added successfully.', 'success')
        # Optionally, you can redirect to another page after adding the prescription
        return redirect(url_for('out_patients'))

    return render_template('add_prescription.html', patient_id=patient_id)

@app.route('/login/doctor_home/out_patient')
def out_patients():
    return render_template('out_patient.html')
@app.route('/login/doctor_home/out_patient/modify_patient_records', methods=['GET', 'POST'])
def modify_patient_records():
    patients = get_all_patients()
    if request.method == 'POST':
        search_type = request.form['search_type']
        search_query = request.form['search_query']

        if search_type == 'patient_id':
            patient = get_patient_by_id((search_query))
            patients = [patient] if patient else []
        elif search_type == 'patient_name':
            patients = get_patients_by_name(search_query)
    return render_template('modify_patient_records.html', patients=patients)

@app.route('/login')
def logout():
    return render_template('login.html')
def get_prescriptions(patient_id):
    # Assuming you have a MongoDB collection named 'prescriptions'
    prescriptions = db.prescriptions.find({'patient_id': patient_id})
    return prescriptions

@app.route('/login/doctor_home/out_patient/view_patient/prescriptions/<patient_id>')
def view_prescriptions(patient_id):
    # Assuming you have a function to retrieve prescription data from the database
    prescription = get_prescriptions(patient_id)
    return render_template('prescriptions.html', prescriptions=prescription)
if __name__ == '__main__':
    app.run(debug=True)