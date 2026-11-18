from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, template_folder="Templates")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cityhospital.db"
app.secret_key = ""
db = SQLAlchemy(app)


class Patient(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    blood_group = db.Column(db.String(5), nullable=False)
    password=db.Column(db.String(45) , nullable=False)
    email=db.Column(db.String(50) , nullable=False)
    phoneNO = db.Column(db.String(13) , nullable=False)
    


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    blood_group = db.Column(db.String(5))
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="patient")


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pname = db.Column(db.String(100), nullable=False)
    page = db.Column(db.Integer, nullable=False)
    pcity = db.Column(db.String(100), nullable=False)
    pphone = db.Column(db.String(20), nullable=False)
    pblood = db.Column(db.String(5))
    pdoctor = db.Column(db.String(50), nullable=False)
    pdate = db.Column(db.String(20), nullable=False)



@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/add_patient", methods=["GET", "POST"])
def add_patient():
    if request.method == "POST":
        patient = Patient(
            name=request.form["name"],
            age=int(request.form["age"]),
            blood_group=request.form["blood_group"],
        )
        db.session.add(patient)
        db.session.commit()
        return redirect("/patients")
    return render_template("add_patient.html")


@app.route("/patients")
def patients():
    all_patients = Patient.query.all()
    return render_template("patients.html", patients=all_patients)


@app.route("/appointments", methods=["GET", "POST"])
def appointments():
    if request.method == "POST":
        appt = Appointment(
            pname=request.form["pname"],
            page=int(request.form["page"]),
            pcity=request.form["pcity"],
            pphone=request.form["pphone"],
            pblood=request.form.get("pblood", ""),
            pdoctor=request.form["pdoctor"],
            pdate=request.form["pdate"],
        )
        db.session.add(appt)
        db.session.commit()
        return redirect("/home")
    return render_template("Appointment.html")


@app.route("/login")
def login():
    return render_template("login.html")


def register_user(role):
    email = request.form["email"].strip().lower()
    if User.query.filter_by(email=email).first():
        return "Yeh email pehle se registered hai. <a href='/login'>Login</a>", 400
    user = User(
        name=request.form["name"],
        email=email,
        phone=request.form.get("phone"),
        blood_group=request.form.get("blood_group"),
        password_hash=generate_password_hash(request.form["password"]),
        role=role,
    )
    db.session.add(user)
    db.session.commit()
    return redirect("/login")


def login_user(role):
    email = request.form["email"].strip().lower()
    user = User.query.filter_by(email=email, role=role).first()
    if user and check_password_hash(user.password_hash, request.form["password"]):
        session["user_id"] = user.id
        session["role"] = user.role
        return redirect("/home")
    return "Email ya password galat hai. <a href='/login'>Dobara try karo</a>", 401


@app.route("/patient_register", methods=["POST"])
def patient_register():
    return register_user("patient")


@app.route("/staff_register", methods=["POST"])
def staff_register():
    return register_user("staff")


@app.route("/patient_login", methods=["POST"])
def patient_login():
    return login_user("patient")


@app.route("/staff_login", methods=["POST"])
def staff_login():
    return login_user("staff")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/home")


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=5500)

