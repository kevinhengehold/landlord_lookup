
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/#a-minimal-application 

#from sqlalchemy import Column, Integer, String, ForeignKey
#from sqlalchemy import text, select, and_, or_

import re

#import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import psycopg

import os

from dotenv import load_dotenv 

load_dotenv()

CONNSTR = f"postgresql+psycopg://{os.getenv('PGUSER')}:{os.getenv('PGPASSWORD')}@ep-nameless-wave-277031.us-east-2.aws.neon.tech/neondb"
 
#CONNSTR = f"postgresql+psycopg://{process.env.PGUSER}:{process.env.PGPASSWORD}@ep-nameless-wave-277031.us-east-2.aws.neon.tech/neondb"

app = Flask(__name__)             # create an app instance
app.config['SQLALCHEMY_DATABASE_URI'] = CONNSTR
db = SQLAlchemy()
db.init_app(app)


class Parcels(db.Model):  
    __tablename__ = 'parcels'
    id = db.Column(db.Integer, primary_key=True)
    parcel_number = db.Column(db.String(50))
    appraisal_area = db.Column(db.Text, db.ForeignKey('appraisal_areas.id') )
    location_street_address = db.Column(db.Text)
    owner_name_1 = db.Column(db.String(250))
    owner_address_1 = db.Column(db.String(250))
    mailing_name_1 = db.Column(db.String(250))
    mailing_address_1 = db.Column(db.Text)

    def __repr__(self):
        return f'<Parcels {self.parcel_number}>'


class AppraisalAreas(db.Model):
    __tablename__ = "appraisal_areas" 
    id = db.Column(db.Text, primary_key=True)
    area_description = db.Column(db.Text)


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
        search_str = re.sub(punct_re, "", search_str).upper()
        
        if len(search_str) <3:
            return render_template('search_landlord_address.html', results = "You must enter at least three numbers or letters to search.", search_string = search_str) 
        # do the database stuff
        else:
            results = Parcels.query.join(AppraisalAreas, AppraisalAreas.id == Parcels.appraisal_area
                ).add_columns(Parcels.parcel_number, Parcels.location_street_address, AppraisalAreas.area_description,
                Parcels.owner_name_1, Parcels.owner_address_1, Parcels.mailing_name_1, Parcels.mailing_address_1
                ).filter(Parcels.owner_address_1.like("%" + search_str + "%") | \
                        (Parcels.mailing_address_1.like("%" + search_str + "%")) )
            
            return render_template('search_landlord_address.html', results = results, search_string = search_str) 
 

@app.route('/search_landlord_name', methods = ['POST', 'GET'])
def search_name():
    search_str = ""
    punct_re = r"[^\w\s\%\_]"

    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        form_data = request.form
        search_str = form_data['landlord_name']
        search_str = re.sub(punct_re, "", search_str).upper()
        
        if len(search_str) <3:
            return render_template('search_landlord_address.html', results = "You must enter at least three numbers or letters to search.", search_string = search_str) 
        # do the database stuff
        else:
            results = Parcels.query.join(AppraisalAreas, AppraisalAreas.id == Parcels.appraisal_area
                ).add_columns(Parcels.parcel_number, Parcels.location_street_address, AppraisalAreas.area_description,
                Parcels.owner_name_1, Parcels.owner_address_1, Parcels.mailing_name_1, Parcels.mailing_address_1
                ).filter(Parcels.owner_name_1.like("%" + search_str + "%") | \
                        (Parcels.mailing_name_1.like("%" + search_str + "%")) )
            
            return render_template('search_landlord_address.html', results = results, search_string = search_str) 

 
if __name__ == "__main__":        # on running python app.py
    app.run()                     # run the flask app
    
