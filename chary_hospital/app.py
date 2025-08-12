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
        # Redirect to the correct dashboard based on role
        if current_user.role == 'doctor':
            return redirect(url_for('doctor_dashboard'))
        elif current_user.role == 'admin':
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('patient_dashboard'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        user = User.query.filter_by(username=username, role=role).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully.')
            # Redirect based on role
            if user.role == 'doctor':
                return redirect(url_for('doctor_dashboard'))
            elif user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('patient_dashboard'))
        else:
            flash('Invalid username, password, or role.')
    return render_template('login.html')

@app.route('/patient_dashboard')
@login_required
def patient_dashboard():
    return render_template('patient_dashboard.html')

@app.route('/doctor_dashboard')
@login_required
def doctor_dashboard():
    return render_template('doctor_dashboard.html')

@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    return render_template('admin_dashboard.html')

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

# Departments data
DEPARTMENTS = [
    {"name": "Anaesthesia", "slug": "anaesthesia", "icon": "<i class='bi bi-capsule'></i>"},
    {"name": "Cardiology", "slug": "cardiology", "icon": "<i class='bi bi-heart-pulse'></i>"},
    {"name": "Dermatology", "slug": "dermatology", "icon": "<i class='bi bi-droplet-half'></i>"},
    {"name": "Dietetics", "slug": "dietetics", "icon": "<i class='bi bi-egg-fried'></i>"},
    {"name": "Emergency", "slug": "emergency", "icon": "<i class='bi bi-exclamation-triangle'></i>"},
    {"name": "Endocrinology", "slug": "endocrinology", "icon": "<i class='bi bi-bar-chart'></i>"},
    {"name": "Family Medicine", "slug": "family-medicine", "icon": "<i class='bi bi-people'></i>"},
    {"name": "Gastroenterology", "slug": "gastroenterology", "icon": "<i class='bi bi-cup-straw'></i>"},
    {"name": "General Surgery", "slug": "general-surgery", "icon": "<i class='bi bi-scissors'></i>"},
    {"name": "Headache Clinic", "slug": "headache-clinic", "icon": "<i class='bi bi-emoji-dizzy'></i>"},
    {"name": "Internal Medicine", "slug": "internal-medicine", "icon": "<i class='bi bi-clipboard2-pulse'></i>"},
    {"name": "Laboratory", "slug": "laboratory", "icon": "<i class='bi bi-beaker'></i>"},
    {"name": "Neurology", "slug": "neurology", "icon": "<i class='bi bi-brain'></i>"},
    {"name": "Obs-Gynaecology", "slug": "obs-gynaecology", "icon": "<i class='bi bi-gender-female'></i>"},
    {"name": "Ophthalmology (EYE)", "slug": "ophthalmology", "icon": "<i class='bi bi-eye'></i>"},
    {"name": "Orthopedics", "slug": "orthopedics", "icon": "<i class='bi bi-bone'></i>"},
    {"name": "Otolaryngology (ENT)", "slug": "otolaryngology", "icon": "<i class='bi bi-ear'></i>"},
    {"name": "Pediatrics", "slug": "pediatrics", "icon": "<i class='bi bi-baby'></i>"},
    {"name": "Psychiatry", "slug": "psychiatry", "icon": "<i class='bi bi-emoji-expressionless'></i>"},
    {"name": "Pulmonology", "slug": "pulmonology", "icon": "<i class='bi bi-wind'></i>"},
    {"name": "Radiology", "slug": "radiology", "icon": "<i class='bi bi-radioactive'></i>"},
    {"name": "Rheumatology", "slug": "rheumatology", "icon": "<i class='bi bi-droplet'></i>"},
    {"name": "Rehabilitation (Physiotherapy)", "slug": "rehabilitation", "icon": "<i class='bi bi-person-walking'></i>"},
    {"name": "Urology", "slug": "urology", "icon": "<i class='bi bi-droplet-half'></i>"},
]

@app.route('/departments')
def departments():
    return render_template('department_glass.html', departments=DEPARTMENTS)

@app.route('/department/<slug>')
def department_landing(slug):
    dept = next((d for d in DEPARTMENTS if d['slug'] == slug), None)
    if not dept:
        return "Department not found", 404
    return render_template('department_landing.html', dept=dept)

HEALTH_PACKAGES = [
    {
        "title": "Executive Health Checkup",
        "slug": "executive-checkup",
        "img": "https://img.freepik.com/free-photo/doctor-with-stethoscope-hospital_1150-17852.jpg",
        "desc": "A complete package for busy professionals to monitor all vital health parameters."
    },
    {
        "title": "Women's Wellness",
        "slug": "womens-wellness",
        "img": "https://img.freepik.com/free-photo/portrait-young-woman-having-medical-check-up-clinic_1098-2176.jpg",
        "desc": "Specialized screening and preventive care for women of all ages."
    },
    {
        "title": "Child Health",
        "slug": "child-health",
        "img": "https://img.freepik.com/free-photo/child-doctor-checkup_1098-2099.jpg",
        "desc": "Comprehensive pediatric checkups and vaccinations for your child's well-being."
    },
    {
        "title": "Senior Citizen Care",
        "slug": "senior-care",
        "img": "https://img.freepik.com/free-photo/elderly-man-medical-exam_1098-2177.jpg",
        "desc": "Regular health monitoring and preventive care for the elderly."
    },
    {
        "title": "Diabetes Screening",
        "slug": "diabetes-screening",
        "img": "https://img.freepik.com/free-photo/doctor-measuring-blood-pressure-patient_1150-17853.jpg",
        "desc": "Early detection and management of diabetes with our expert care team."
    },
    {
        "title": "Heart Checkup",
        "slug": "heart-checkup",
        "img": "https://img.freepik.com/free-photo/doctor-checking-heartbeat-patient_1150-17851.jpg",
        "desc": "Advanced cardiac screening and consultations with our specialists."
    }
]

@app.route('/health-packages')
def health_packages():
    return render_template('health_packages.html', packages=HEALTH_PACKAGES)

@app.route('/health-package/<slug>')
def health_package_detail(slug):
    pkg = next((p for p in HEALTH_PACKAGES if p['slug'] == slug), None)
    if not pkg:
        return "Package not found", 404
    return render_template('health_package_detail.html', pkg=pkg)

OFFERS = {
    "full-body-checkup": {
        "title": "Full Body Checkup",
        "img": "https://images.pexels.com/photos/1170979/pexels-photo-1170979.jpeg?auto=compress&w=400",
        "price": "₹1499"
    },
    # Add other offers here as needed
}

@app.route('/offers')
def offers():
    return render_template('offers.html')

from models import Booking, db
from flask_mail import Mail, Message
import os

# Flask-Mail config (fully flexible for any provider)
# Set these environment variables for your provider (Gmail, Outlook, custom SMTP, etc)
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'True').lower() in ('true','1','yes')
app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL', 'False').lower() in ('true','1','yes')
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', 'your_gmail@gmail.com')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', 'your_app_password')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'your_gmail@gmail.com')
mail = Mail(app)

@app.route('/book-offer/<slug>', methods=['GET', 'POST'])
def book_offer(slug):
    offer = OFFERS.get(slug)
    if not offer:
        return "Offer not found", 404
    from datetime import date, datetime
    min_date = date.today().isoformat()
    if request.method == 'POST':
        booking = Booking(
            offer_slug=slug,
            offer_title=offer['title'],
            patient_name=request.form['patient_name'],
            email=request.form['email'],
            phone=request.form['phone'],
            appointment_date=datetime.strptime(request.form['appointment_date'], "%Y-%m-%d").date()
        )
        db.session.add(booking)
        db.session.commit()
        # Send confirmation email
        try:
            msg = Message(
                subject=f"Booking Confirmation: {offer['title']}",
                recipients=[request.form['email']],
                body=f"Dear {request.form['patient_name']},\n\nYour booking for {offer['title']} on {request.form['appointment_date']} at CTS Health Care is confirmed.\n\nThank you!\nCTS Health Care Team"
            )
            mail.send(msg)
        except Exception as e:
            print('Email send failed:', e)
        flash(f"Booking confirmed for {offer['title']} on {request.form['appointment_date']}. Confirmation email sent.")
        return redirect(url_for('offers'))
    return render_template('book_offer.html', offer=offer, min_date=min_date)

@app.route('/doctors')
def doctors():
    return render_template('doctors.html')

@app.route('/homecare')
def homecare():
    return render_template('homecare.html')

@app.route('/new-patient-registration', methods=['GET', 'POST'])
def new_patient_registration():
    if request.method == 'POST':
        # Here you would handle saving the registration details to the database
        flash('Registration submitted successfully! Our staff will contact you soon.')
        return redirect(url_for('new_patient_registration'))
    return render_template('new_patient_registration.html')

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
