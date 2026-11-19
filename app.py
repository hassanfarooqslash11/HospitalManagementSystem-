from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date

app = Flask(__name__, template_folder="Templates")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cityhospital.db"
app.secret_key = "change-this-secret-key"
db = SQLAlchemy(app)


class Register(db.Model):
    __tablename__ = "register"
    phoneNO = db.Column(db.String(13), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    blood_group = db.Column(db.String(5))
    email = db.Column(db.String(120))
    role = db.Column(db.String(20), nullable=False, default="patient")


class Userlogin(db.Model):
    __tablename__ = "userlogin"
    email = db.Column(db.String(120), primary_key=True)
    password_hash = db.Column(db.String(200), nullable=False)


class Stafflogin(db.Model):
    __tablename__ = "stafflogin"
    email = db.Column(db.String(120), primary_key=True)
    password_hash = db.Column(db.String(200), nullable=False)


class Appointment(db.Model):
    __tablename__ = "appointment"
    id = db.Column(db.Integer, primary_key=True)
    pNo = db.Column(db.String(13), db.ForeignKey("register.phoneNO"), nullable=False)
    pname = db.Column(db.String(100), nullable=False)
    page = db.Column(db.Integer, nullable=False)
    pcity = db.Column(db.String(100), nullable=False)
    pblood = db.Column(db.String(5))
    pdoctor = db.Column(db.String(50), nullable=False)
    pdate = db.Column(db.String(20), nullable=False)


class Report(db.Model):
    __tablename__ = "report"
    id = db.Column(db.Integer, primary_key=True)
    phoneNO = db.Column(db.String(13), db.ForeignKey("register.phoneNO"), nullable=False)
    report_name = db.Column(db.String(100), nullable=False)
    file_name = db.Column(db.String(200), nullable=False)
    uploaded_on = db.Column(db.String(20), default=lambda: str(date.today()))


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/add_patient", methods=["GET", "POST"])
def add_patient():
    if request.method == "POST":
        patient = Register(
            phoneNO=request.form["phone"],
            name=request.form["name"],
            age=int(request.form["age"]),
            blood_group=request.form["blood_group"],
            email=request.form.get("email", ""),
            role="patient",
        )
        db.session.add(patient)
        db.session.commit()
        return redirect("/home")
    return render_template("add_patient.html")


@app.route("/patients")
def patients():
    all_patients = Register.query.filter_by(role="patient").all()
    return render_template("patients.html", patients=all_patients)


@app.route("/appointments", methods=["GET", "POST"])
def appointments():
    if request.method == "POST":
        phone = request.form["pphone"]
        if not db.session.get(Register, phone):
            return "Yeh phone number registered nahi hai. <a href='/login'>Pehle register karo</a>", 400
        appt = Appointment(
            pNo=phone,
            pname=request.form["pname"],
            page=int(request.form["page"]),
            pcity=request.form["pcity"],
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

@app.route("/reports")
def Reports():
    return render_template("Reports.html")


def register_user(role, LoginTable):
    email = request.form["email"].strip().lower()
    phone = request.form["phone"].strip()
    if db.session.get(Register, phone) or db.session.get(LoginTable, email):
        return "Phone ya email pehle se registered hai. <a href='/login'>Login</a>", 400
    age = request.form.get("age")
    db.session.add(Register(
        phoneNO=phone,
        name=request.form["name"],
        age=int(age) if age else None,
        blood_group=request.form.get("blood_group"),
        email=email,
        role=role,
    ))
    db.session.add(LoginTable(
        email=email,
        password_hash=generate_password_hash(request.form["password"]),
    ))
    db.session.commit()
    return redirect("/login")


def login_user(role, LoginTable):
    email = request.form["email"].strip().lower()
    user = db.session.get(LoginTable, email)
    if user and check_password_hash(user.password_hash, request.form["password"]):
        session["email"] = email
        session["role"] = role
        return redirect("/home")
    return "Email ya password galat hai. <a href='/login'>Dobara try karo</a>", 401


@app.route("/patient_register", methods=["POST"])
def patient_register():
    return register_user("patient", Userlogin)


@app.route("/staff_register", methods=["POST"])
def staff_register():
    return register_user("staff", Stafflogin)


@app.route("/patient_login", methods=["POST"])
def patient_login():
    return login_user("patient", Userlogin)


@app.route("/staff_login", methods=["POST"])
def staff_login():
    return login_user("staff", Stafflogin)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/home")


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=5500)