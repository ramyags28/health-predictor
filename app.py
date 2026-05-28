from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Table
class Patient(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100))
    dob = db.Column(db.String(20))
    email = db.Column(db.String(100))
    glucose = db.Column(db.Float)
    haemoglobin = db.Column(db.Float)
    cholesterol = db.Column(db.Float)
    remarks = db.Column(db.String(200))


# AI Prediction Function
def predict_health(glucose, haemoglobin, cholesterol):

    if glucose > 140:
        return "Possible Diabetes Risk"

    elif haemoglobin < 12:
        return "Possible Anemia Risk"

    elif cholesterol > 240:
        return "Possible Heart Disease Risk"

    else:
        return "Healthy"


# Home Page
@app.route('/')
def index():

    patients = Patient.query.all()

    return render_template('index.html', patients=patients)


# Add Patient
@app.route('/add', methods=['GET', 'POST'])
def add():

    if request.method == 'POST':

        fullname = request.form['fullname']
        dob = request.form['dob']
        email = request.form['email']

        glucose = float(request.form['glucose'])
        haemoglobin = float(request.form['haemoglobin'])
        cholesterol = float(request.form['cholesterol'])

        remarks = predict_health(
            glucose,
            haemoglobin,
            cholesterol
        )

        patient = Patient(
            fullname=fullname,
            dob=dob,
            email=email,
            glucose=glucose,
            haemoglobin=haemoglobin,
            cholesterol=cholesterol,
            remarks=remarks
        )

        db.session.add(patient)
        db.session.commit()

        return redirect('/')

    return render_template('add.html')


# Delete Patient
@app.route('/delete/<int:id>')
def delete(id):

    patient = Patient.query.get(id)

    db.session.delete(patient)
    db.session.commit()

    return redirect('/')


# Edit Patient
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):

    patient = Patient.query.get(id)

    if request.method == 'POST':

        patient.fullname = request.form['fullname']
        patient.dob = request.form['dob']
        patient.email = request.form['email']

        patient.glucose = float(request.form['glucose'])
        patient.haemoglobin = float(request.form['haemoglobin'])
        patient.cholesterol = float(request.form['cholesterol'])

        patient.remarks = predict_health(
            patient.glucose,
            patient.haemoglobin,
            patient.cholesterol
        )

        db.session.commit()

        return redirect('/')

    return render_template('edit.html', patient=patient)


# Run Application
if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    app.run(host='0.0.0.0', port=5000, debug=True)