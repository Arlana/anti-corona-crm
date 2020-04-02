# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Date, Boolean, Float, ForeignKey, JSON

from app import db
from app import constants as c

from app.login.util import hash_pass

class Patient(db.Model):

    __tablename__ = 'Patient'

    id = Column(Integer, primary_key=True)
    full_name = Column(String, unique=False)
    iin = Column(String, unique=False)
    dob = Column(Date, unique=False)
    citizenship = Column(String, unique=False)
    pass_num = Column(String, unique=False)
    telephone = Column(String, unique=False)
    arrival_date = Column(Date, unique=False)
    visited_country = Column(String, unique=False)
    
    is_contacted_person = Column(Boolean, unique=False)

    travel_type_id = Column(Integer, ForeignKey('TravelType.id'), nullable=True, default=None)
    travel_type = db.relationship('TravelType')    

    flight_code_id = Column(Integer, ForeignKey('FlightCode.id'), nullable=True, default=None)
    flight_code = db.relationship('FlightCode')

    region_id = Column(Integer, ForeignKey('Region.id'))
    region = db.relationship('Region')

    status_id = Column(Integer, ForeignKey('PatientStatus.id'))
    status = db.relationship('PatientStatus')

    is_found = Column(Boolean, unique=False)
    is_infected = Column(Boolean, unique=False, default=False)

    hospital_id = Column(Integer, ForeignKey('Hospital.id'))
    hospital = db.relationship('Hospital')

    home_address = Column(String, unique=False)
    job = Column(String, unique=False)

    address_lat = Column(Float, unique=False)
    address_lng = Column(Float, unique=False)

    attrs = Column(JSON, unique=False)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]
                
            setattr(self, property, value)

    def __repr__(self):
        return str(self.id)

class ContactedPersons(db.Model):
    __tablename__ = 'ContactedPersons'

    id = Column(Integer, primary_key=True)
    
    person_id = Column(Integer, ForeignKey('Patient.id'))
    # person = db.relationship('Patient')

    patient_id = Column(Integer, ForeignKey('Patient.id'))
    # patient = db.relationship('Patient')
    attrs = Column(JSON, unique=False)
    

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]
                
            setattr(self, property, value)

    def __repr__(self):
        return str(self.id)   

class PatientStatus(db.Model):

    __tablename__ = 'PatientStatus'

    id = Column(Integer, primary_key=True)
    value = Column(String, unique=True)
    name = Column(String, unique=True)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]
                
            setattr(self, property, value)

    def __repr__(self):
        return str(self.name)        

class ContactedPerson(db.Model):

    __tablename__ = 'ContactedPerson'

    id = Column(Integer, primary_key=True)
    full_name = Column(String, unique=False)
    iin = Column(String, unique=True)
    # dob = Column(Date, unique=False)
    telephone = Column(String, unique=False)
    
    region_id = Column(Integer, ForeignKey('Region.id'))
    region = db.relationship('Region')

    home_address = Column(String, unique=False)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]
                
            setattr(self, property, value)

    def __repr__(self):
        return str(self.id)