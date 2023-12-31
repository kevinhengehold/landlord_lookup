
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/#a-minimal-application 

#from sqlalchemy import Column, Integer, String, ForeignKey
#from sqlalchemy import text, select, and_, or_

import re

#import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
#import psycopg2

from string import punctuation 

import os

from dotenv import load_dotenv 

load_dotenv()

CONNSTR = f"postgresql://{os.getenv('PGUSER')}:{os.getenv('PGPASSWORD')}@ep-nameless-wave-277031.us-east-2.aws.neon.tech/neondb"
 
#CONNSTR = f"postgresql+psycopg://{process.env.PGUSER}:{process.env.PGPASSWORD}@ep-nameless-wave-277031.us-east-2.aws.neon.tech/neondb"

app = Flask(__name__)             # create an app instance
app.config['SQLALCHEMY_DATABASE_URI'] = CONNSTR
db = SQLAlchemy()
db.init_app(app)


class Parcels(db.Model):  
    __tablename__ = 'parcels'
    id = db.Column(db.Integer, primary_key=True)
    parcel_number = db.Column(db.String(15))
    prop_class_code = db.Column(db.Integer, db.ForeignKey('property_classes.id'))
    appraisal_area = db.Column(db.Text, db.ForeignKey('appraisal_areas.id') )
    owner_name = db.Column(db.String(250))
    owner_address = db.Column(db.String(250))
    owner_city  = db.Column(db.String(100))
    owner_state = db.Column(db.String(50))
    owner_zip = db.Column(db.String(10))
    location_street_address = db.Column(db.String(250))
    location_city = db.Column(db.String(250))
    mailing_name = db.Column(db.String(250))
    mailing_address = db.Column(db.String(250))
    mailing_city = db.Column(db.String(100))
    mailing_state = db.Column(db.String(50))
    mailing_zip = db.Column(db.String(10))
    rental_registration_flag = db.Column(db.CHAR)
    transfer_date = db.Column(db.Date)

    def __repr__(self):
        return f'<Parcels {self.parcel_number}>'

class AppraisalAreas(db.Model):
    __tablename__ = "appraisal_areas" 
    id = db.Column(db.Float, primary_key=True)
    area_description = db.Column(db.String)

class PropertyClasses(db.Model):
    __tablename__ = "property_classes" 
    id = db.Column(db.Integer, primary_key=True)
    class_description = db.Column(db.String)

class Addresses(db.Model):
    __tablename__ = "addresses" 
    id = db.Column(db.Integer, primary_key=True)
    grppclid = db.Column(db.String(12))
    bldgplace = db.Column(db.String(50))
    unit =  db.Column(db.String(12))
    citypermid =  db.Column(db.String(10))
    cntypermid = db.Column(db.String(10))
    zipcode = db.Column(db.String(5))
    address = db.Column(db.String(50))
    addrtype = db.Column(db.String(3))
    hnumsfx = db.Column(db.String(10))
    condoflg = db.Column(db.CHAR)
    multiunit  = db.Column(db.CHAR)
    jurisfull = db.Column(db.String(30))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    fullmailadr = db.Column(db.String(75))
    fk_parcel_number = db.Column(db.String(15), db.ForeignKey('parcels.parcel_number') )



# reroutes to 'search_input'. 
@app.route("/")                   
def test_method(): 
    return render_template('search_input.html')       
 
 
 
 ################# Input cleaning ############################
 #### 1. input too short. #########
 #### 2. 
 
@app.route('/search_landlord_address', methods = ['POST', 'GET'])
def search_address():
    search_str = ""
    punct_re = r"[^\w\s\%\_]"

    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        form_data = request.form
        search_str = form_data['landlord_address']
        # search_str = re.sub(punct_re, "", search_str).upper()

        search_str = "%" + search_str.upper() + "%"
        
        if len(search_str) <3:
            return render_template('search_landlord_address.html', results = "You must enter at least three numbers or letters to search.", search_string = search_str) 
        # do the database stuff
        else:
            results = Parcels.query.join(PropertyClasses, PropertyClasses.id == Parcels.prop_class_code, isouter=False).join(AppraisalAreas, AppraisalAreas.id == Parcels.appraisal_area, isouter=False).join(Addresses, Addresses.fk_parcel_number == Parcels.parcel_number, isouter = False).add_columns(Addresses.fullmailadr, Addresses.latitude, Addresses.longitude, AppraisalAreas.area_description, PropertyClasses.class_description, Parcels.owner_name, Parcels.owner_address, Parcels.mailing_name, Parcels.mailing_address).filter(Parcels.owner_address.like( search_str ) | \
                        (Parcels.mailing_address.like( search_str )) )
            
            return render_template('search_landlord_address.html', results = results, search_string = search_str[1:-1]) 
 

@app.route('/search_landlord_name', methods = ['POST', 'GET'])
def search_name():
    search_str = ""
    punct_re = r"[^\w\s\%\_]"

    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        form_data = request.form
        search_str = form_data['landlord_name']
        
        search_str = "%" + search_str.upper() + "%"
        
        if len(search_str) <3:
            return render_template('search_landlord_address.html', results = "You must enter at least three numbers or letters to search.", search_string = search_str) 
        # do the database stuff
        else:
            results = Parcels.query.join(PropertyClasses, PropertyClasses.id == Parcels.prop_class_code, isouter=False).join(AppraisalAreas, AppraisalAreas.id == Parcels.appraisal_area, isouter=False).join(Addresses, Addresses.fk_parcel_number == Parcels.parcel_number, isouter = False).add_columns(Addresses.fullmailadr, Addresses.latitude, Addresses.longitude, AppraisalAreas.area_description, PropertyClasses.class_description, Parcels.owner_name, Parcels.owner_address, Parcels.mailing_name, Parcels.mailing_address).filter(Parcels.owner_address.like( search_str ) | \
            (Parcels.mailing_address.like( search_str )) )
            
            return render_template('search_landlord_address.html', results = results, search_string = search_str[1:-1]) 

 
if __name__ == "__main__":        # on running python app.py
    app.run()                     # run the flask app
    
