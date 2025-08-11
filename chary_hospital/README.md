# CHARY's Super Speciality Hospital Web App

A modern, full-featured hospital management system built with Flask.

## Features

### Authentication
- User registration (sign up)
- Secure login/logout
- Passwords are hashed for security

### Dashboard
- Personalized welcome for logged-in users
- Modern UI with cards/buttons for each hospital section

### Main Sections (Accessible from Dashboard)
- **Patient Services:** Registration, appointments, reports
- **Doctor Section:** Doctor dashboard, appointments, patient care tools
- **Admin Section:** Hospital admin, staff management, analytics
- **Pharmacy:** Medicines, inventory, pharmacy management
- **Billing:** Patient billing, payments, financial records
- **Laboratory:** Lab requests, results, diagnostics
- **Feedback:** Submit feedback, suggestions, contact hospital staff

### Patient Management
- Add new patients
- View all patients
- Maintain patient medical history

### Technology Stack
- **Backend:** Python, Flask, Flask-Login, Flask-SQLAlchemy
- **Frontend:** Bootstrap 5, HTML, CSS
- **Database:** SQLite (easy to switch to other DBs)

### Deployment Ready
- GitHub Actions workflow for Azure Web App deployment
- Azure DevOps pipeline YAML (build & deploy stages)
- Modular variable management for CI/CD

## Quick Start
1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `python app.py`
3. Open your browser and go to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) or [http://localhost:5000/](http://localhost:5000/) to use the app locally.
4. Register a new user and log in to access the dashboard

## Project Structure
- `app.py` – Main Flask app and routes
- `models.py` – Database models
- `templates/` – HTML templates for each section
- `static/` – Static assets (CSS, images, etc.)
- `.github/workflows/` – GitHub Actions CI/CD
- `azure-webapp.yaml` – Azure DevOps pipeline
- `pipeline-variables.yaml` – Central pipeline variables

## Customization
- Add more features to any section by editing the corresponding template and route
- Update deployment variables in `pipeline-variables.yaml`

## License
This project is for demonstration and educational purposes. Please check image/asset licenses if deploying publicly.
