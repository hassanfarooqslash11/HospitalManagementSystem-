from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cityhospital.db"
db = SQLAlchemy(app)

class Patient(db.Model):
    Patid = db.Column(db.Integer, primary_key=True)
    Patname = db.Column(db.String(100), nullable=False)
    Patage = db.Column(db.Integer, nullable=False)
    patblood_group = db.Column(db.String(5), nullable=True)



@app.route("/")
def hospitalmanagement():
    return render_template("home.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5500)