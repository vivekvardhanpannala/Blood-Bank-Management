from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db = SQLAlchemy(app)

class Donor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    blood_group = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    district = db.Column(db.String(50), nullable=False)
    mobile_number = db.Column(db.String(15), nullable=False)

class BloodRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    blood_group = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    district = db.Column(db.String(50), nullable=False)
    mobile_number = db.Column(db.String(15), nullable=False)


with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/donate', methods=['POST','GET'])
def donate():
    if request.method == 'POST':
        name = request.form['name']
        blood_group = request.form['blood_group']
        address = request.form['address']
        district = request.form['district']
        mobile_number = request.form['mobile_number']

        donor = Donor(name=name, blood_group=blood_group, address=address, district=district, mobile_number=mobile_number)
        db.session.add(donor)
        db.session.commit()

        return redirect(url_for('index'))
    else:
        return render_template('donate.html')
        

@app.route('/request_blood', methods=['POST','GET'])
def request_blood():
    if request.method == 'POST':
        name = request.form['name']
        blood_group = request.form['blood_group']
        address = request.form['address']
        district = request.form['district']
        mobile_number = request.form['mobile_number']

        # Query donors in the same district with the requested blood type
        available_donors = Donor.query.filter_by(district=district, blood_group=blood_group).all()

        return render_template('donors_list.html', donors=available_donors)
    else:
        return render_template('request_blood.html')

@app.route('/donors_list')
def donor_list():
    available_donors = Donor.query.all()
    return render_template('donors_list.html',donors=available_donors)

if __name__ == '__main__':
    
    app.run(debug=True)
