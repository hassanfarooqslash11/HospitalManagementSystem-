from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder="Templates")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cityhospital.db"
db = SQLAlchemy(app)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    blood_group = db.Column(db.String(5), nullable=False)

@app.route("/")
def hospitalmanagement():
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

@app.route("/appointments")
def appointments(): 
     return render_template("Appointment.html")


@app.route("/home")
def home():
    return render_template("home.html")

@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5500)