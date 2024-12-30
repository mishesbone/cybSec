from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

app = Flask(__name__)

# Configuration for Flask-Login, Flask-SQLAlchemy, and Flask-WTF
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///incidents.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='User')  # Admin or User

# Incident Model
class Incident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(100), nullable=False)
    threat_name = db.Column(db.String(100), nullable=False)
    severity = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)

# Login manager loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Home Route
@app.route("/")
def home():
    return render_template("home.html")

# Incidents Page
@app.route("/incidents")
@login_required
def incidents():
    all_incidents = Incident.query.all()
    return render_template("incidents.html", incidents=all_incidents)

# Add Incident Page (Only accessible to Admins)
@app.route("/add_incident", methods=["GET", "POST"])
@login_required
def add_incident():
    if current_user.role != 'Admin':
        flash("You don't have permission to access this page.", "danger")
        return redirect(url_for("incidents"))
    
    if request.method == "POST":
        timestamp = request.form['timestamp']
        threat_name = request.form['threat_name']
        severity = request.form['severity']
        description = request.form['description']

        new_incident = Incident(timestamp=timestamp, threat_name=threat_name,
                                 severity=severity, description=description)

        db.session.add(new_incident)
        db.session.commit()

        flash("Incident added successfully!", "success")
        return redirect(url_for("incidents"))

    return render_template("add_incident.html")

# User Authentication Routes
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=100)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):  # Secure password check
            login_user(user)
            flash("Login successful", "success")
            return redirect(url_for("home"))
        else:
            flash("Login failed. Check your username and password.", "danger")

    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully!", "info")
    return redirect(url_for("login"))

# Registration Route
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = StringField('Role (Admin/User)', validators=[DataRequired(), Length(min=3, max=10)])
    submit = SubmitField('Register')

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        hashed_password = generate_password_hash(password)
        role = form.role.data

        # Check if username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists. Please choose another.", "danger")
            return redirect(url_for('register'))

        new_user = User(username=username, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('login'))

    return render_template("register.html", form=form)

# Real-time Alert for Critical Threats
def check_for_critical_threats():
    critical_incidents = Incident.query.filter_by(severity='Critical').all()
    return critical_incidents

@app.route("/alerts")
@login_required
def alerts():
    critical_incidents = check_for_critical_threats()
    return render_template("alerts.html", incidents=critical_incidents)

# Ensure the database is created
def create_db():
    with app.app_context():  # Ensures app context is active
        db.create_all()  # Create the database and tables within the app context

if __name__ == "__main__":
    create_db()  # Create the database and tables
    app.run(debug=True)
