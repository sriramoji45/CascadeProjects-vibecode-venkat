from flask import Flask, render_template, redirect, url_for, request, flash
from extensions import db
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from models import User, Patient, PatientHistory

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username already exists.')
            return redirect(url_for('register'))
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully.')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/patient-services')
@login_required
def patient_services():
    return render_template('patient_services.html')

@app.route('/doctor')
@login_required
def doctor():
    return render_template('doctor.html')

@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html')

@app.route('/pharmacy')
@login_required
def pharmacy():
    return render_template('pharmacy.html')

@app.route('/billing')
@login_required
def billing():
    return render_template('billing.html')

@app.route('/laboratory')
@login_required
def laboratory():
    return render_template('laboratory.html')

@app.route('/feedback')
@login_required
def feedback():
    return render_template('feedback.html')

@app.route('/add_patient', methods=['GET', 'POST'])
@login_required
def add_patient():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        contact = request.form['contact']
        patient = Patient(name=name, age=age, gender=gender, contact=contact)
        db.session.add(patient)
        db.session.commit()
        flash('Patient added successfully.')
        return redirect(url_for('patients'))
    return render_template('add_patient.html')

@app.route('/patients')
@login_required
def patients():
    all_patients = Patient.query.all()
    return render_template('patients.html', patients=all_patients)

@app.route('/patient/<int:patient_id>')
@login_required
def patient_history(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    return render_template('patient_history.html', patient=patient)

@app.route('/add_history/<int:patient_id>', methods=['GET', 'POST'])
@login_required
def add_history(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    if request.method == 'POST':
        visit_date = request.form['visit_date']
        diagnosis = request.form['diagnosis']
        treatment = request.form['treatment']
        history = PatientHistory(patient_id=patient.id, visit_date=visit_date, diagnosis=diagnosis, treatment=treatment)
        db.session.add(history)
        db.session.commit()
        flash('History added successfully.')
        return redirect(url_for('patient_history', patient_id=patient.id))
    return render_template('add_history.html', patient=patient)

if __name__ == '__main__':
    with app.app_context():
        if not os.path.exists('hospital.db'):
            db.create_all()
    app.run(debug=True)
