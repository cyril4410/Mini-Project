from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from models import User, db
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a secure secret key

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if username already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists. Please choose a different one.', 'error')
            return redirect(url_for('register'))

        # Create a new User instance
        new_user = User(username=username, password=generate_password_hash(password))

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)

def create_tables():
    with app.app_context():
        # Read SQL statements from the schema file and execute them
        with open('schema.sql', 'r') as file:
            sql_statements = file.read()

        # Execute the SQL statements
        db.engine.execute(sql_statements)

if __name__ == '__main__':
    create_tables()


# Route for patient sign-in
@app.route('/patient/signin', methods=['GET', 'POST'])
def patient_signin():
    if request.method == 'POST':
        # Perform authentication (placeholder)
        # Replace this with actual authentication logic
        username = request.form['username']
        password = request.form['password']
        # Placeholder for authentication (replace with actual logic)
        if username == 'patient_username' and password == 'patient_password':
            # Authentication successful
            session['logged_in'] = True
            session['username'] = username
            session['role'] = 'patient'
            flash('You have been successfully signed in.', 'success')
            return redirect(url_for('patient_home'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('patient_signin.html')

'''
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'  # Add a secret key for session management

db = SQLAlchemy(app)

# Define your User model here

if __name__ == '__main__':
    # Create all database tables
    db.create_all()

    # Add a sample user to the database
    username = 'sample_user'
    password = 'sample_password'
    new_user =User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    app.run(debug=True)

'''
# Route for doctor sign-in
@app.route('/doctor/signin', methods=['GET', 'POST'])
def doctor_signin():
    if request.method == 'POST':
        # Perform authentication (placeholder)
        # Replace this with actual authentication logic
        username = request.form['username']
        password = request.form['password']
        
        # Placeholder for authentication (replace with actual logic)
        if username == 'doctor_username' and password == 'doctor_password':
            # Authentication successful
            session['logged_in'] = True
            session['username'] = username
            session['role'] = 'doctor'
            flash('You have been successfully signed in.', 'success')
            return redirect(url_for('doctor_home'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('doctor_signin.html')
# Route for patient homepage
@app.route('/patient/home')
def patient_home():
    if 'logged_in' not in session or session['role'] != 'patient':
        flash('You must be logged in as a patient to access this page.', 'error')
        return redirect(url_for('patient_signin'))

    return render_template('patient_home.html', username=session['username'])

# Route for doctor homepage
@app.route('/doctor/home')
def doctor_home():
    if 'logged_in' not in session or session['role'] != 'doctor':
        flash('You must be logged in as a doctor to access this page.', 'error')
        return redirect(url_for('doctor_signin'))

    return render_template('doctor_home.html', username=session['username'])
# Route for adding patient details
@app.route('/doctor/add_patient', methods=['GET', 'POST'])
def add_patient():
    if 'logged_in' not in session or session['role'] != 'doctor':
        flash('You must be logged in as a doctor to add patient details.', 'error')
        return redirect(url_for('doctor_signin'))

    if request.method == 'POST':
        # Placeholder for adding patient details
        # Replace this with actual logic to add patient details to the database
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        
        # Placeholder: Add patient details to the database (replace with actual logic)
        flash('Patient details added successfully.', 'success')
        return redirect(url_for('doctor_home'))

    return render_template('add_patient.html')

# Route for viewing patient details
@app.route('/doctor/view_patient/<int:patient_id>')
def view_patient(patient_id):
    if 'logged_in' not in session or session['role'] != 'doctor':
        flash('You must be logged in as a doctor to view patient details.', 'error')
        return redirect(url_for('doctor_signin'))

    # Placeholder: Fetch patient details from the database (replace with actual logic)
    patient_details = {}  # Placeholder for patient details
    
    return render_template('view_patient.html', patient_details=patient_details)
# Route for viewing appointments
@app.route('/patient/appointments')
def view_appointments():
    if 'logged_in' not in session or session['role'] != 'patient':
        flash('You must be logged in as a patient to view appointments.', 'error')
        return redirect(url_for('patient_signin'))

    # Placeholder: Fetch appointments from the database (replace with actual logic)
    appointments = []  # Placeholder for appointments
    
    return render_template('view_appointments.html', appointments=appointments)

# Route for viewing medical reports
@app.route('/patient/medical_reports')
def view_medical_reports():
    if 'logged_in' not in session or session['role'] != 'patient':
        flash('You must be logged in as a patient to view medical reports.', 'error')
        return redirect(url_for('patient_signin'))

    # Placeholder: Fetch medical reports from the database (replace with actual logic)
    medical_reports = []  # Placeholder for medical reports
    
    return render_template('view_medical_reports.html', medical_reports=medical_reports)
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key
# Route for viewing medical history
@app.route('/doctor/medical_history/<int:patient_id>')
def view_medical_history(patient_id):
    if 'logged_in' not in session or session['role'] != 'doctor':
        flash('You must be logged in as a doctor to view medical history.', 'error')
        return redirect(url_for('doctor_signin'))

    # Placeholder: Fetch patient details and medical history from the database (replace with actual logic)
    patient_details = {}  # Placeholder for patient details
    scan_reports = []  # Placeholder for scan reports
    diagnosed_diseases = []  # Placeholder for diagnosed diseases
    allergies = []  # Placeholder for allergies
    
    return render_template('view_medical_history.html', patient_details=patient_details, 
                           scan_reports=scan_reports, diagnosed_diseases=diagnosed_diseases,
                           allergies=allergies)
# Route for patient sign-in
@app.route('/patient/signin', methods=['GET', 'POST'])
def patient_signin():
    if request.method == 'POST':
        # Placeholder: Validate patient credentials (replace with actual logic)
        username = request.form['username']
        password = request.form['password']

        # Placeholder: Check if username and password are valid (replace with actual logic)
        if username == 'patient' and password == 'password':
            session['logged_in'] = True
            session['username'] = username
            session['role'] = 'patient'
            flash('You have been successfully signed in.', 'success')
            return redirect(url_for('patient_home'))
        else:
            flash('Invalid username or password.', 'error')

    return render_template('patient_signin.html')

# Route for doctor sign-in
@app.route('/doctor/signin', methods=['GET', 'POST'])
def doctor_signin():
    if request.method == 'POST':
        # Placeholder: Validate doctor credentials (replace with actual logic)
        username = request.form['username']
        password = request.form['password']

        # Placeholder: Check if username and password are valid (replace with actual logic)
        if username == 'doctor' and password == 'password':
            session['logged_in'] = True
            session['username'] = username
            session['role'] = 'doctor'
            flash('You have been successfully signed in.', 'success')
            return redirect(url_for('doctor_home'))
        else:
            flash('Invalid username or password.', 'error')

    return render_template('doctor_signin.html')
# Route for the index page
@app.route('/')
def index():
    if 'logged_in' in session:
        if session['role'] == 'patient':
            return redirect(url_for('patient_home'))
        
        elif session['role'] == 'doctor':
            return redirect(url_for('doctor_home'))
        
    return render_template('index.html')

# Other routes and functionalities will be added next

if __name__ == '__main__':
    app.run(debug=True)
'''
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
db = SQLAlchemy(app)

# Define the Patient model
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)

# Route for adding patient details
@app.route('/doctor/add_patient', methods=['GET', 'POST'])
def add_patient():
    if 'logged_in' not in session or session['role'] != 'doctor':
        flash('You must be logged in as a doctor to add patient details.', 'error')
        return redirect(url_for('doctor_signin'))

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']

        # Create a new Patient object
        new_patient = Patient(name=name, age=age, gender=gender)

        # Add the new patient to the database
        try:
            db.session.add(new_patient)
            db.session.commit()
            flash('Patient details added successfully.', 'success')
            return redirect(url_for('doctor_home'))
        except IntegrityError:
            db.session.rollback()
            flash('Error: Patient details could not be added.', 'error')

    return render_template('add_patient.html')

# Other routes and functionalities will be added next

if __name__ == '__main__':
    app.run(debug=True)
'''
