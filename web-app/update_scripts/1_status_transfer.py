# -*- encoding: utf-8 -*-
# import os
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

# from app import create_app
# from app.main.patients.models import Patient, PatientStatus, PatientState, State

# from config import config_dict

# get_config_mode = os.environ.get('CONFIG_MODE', 'Debug')
# config_mode = config_dict[get_config_mode.capitalize()]

# app = create_app(config_mode) 
# engine = create_engine(config_mode.SQLALCHEMY_DATABASE_URI)

# Session = sessionmaker(bind = engine)
# session = Session()

# patients = session.query(Patient).all()
# for patient in patients:
#     print(patient)

# session.close()

import os
import json
from datetime import datetime, timedelta

import psycopg2

# Connect to our PostgreSQL
psqlConn = psycopg2.connect(dbname=os.getenv("DATABASE_NAME"),
                            user=os.getenv("DATABASE_USER"),
                            password=os.getenv("DATABASE_PASSWORD"),
                            host=os.getenv("DATABASE_HOST"))
psqlConn.autocommit = True
psqlCursor = psqlConn.cursor()

def psqlQuery(query_message):
    """
    Function that queries PostgreSQL
    If SELECT returns key-value paired objects
    """
    psqlCursor.execute(query_message)
    # print(query_message)
    try:
        columns = [col.name for col in psqlCursor.description]
        returnValue = []
        for row in psqlCursor:
            pairs = list(zip(columns, row))
            obj = {}
            for pair in pairs:
                obj[pair[0]] = pair[1]
            returnValue.append(obj)
    except Exception:
        returnValue = None
    return returnValue

"""
    Transfer is_found, is_infected, status_id (PatientStatus) to attrs
"""

patients = psqlQuery('SELECT * FROM "Patient" WHERE is_found = true OR is_infected = true OR status_id IS NOT NULL OR status_id != 1 ORDER BY id;')
for patient in patients:
    print(patient["id"])
    attrs = {}
    if patient['is_found'] == True:
        attrs['is_found'] = True
    if patient['is_infected'] == True:
        attrs['is_infected'] = True
    status_id = patient['status_id']
    if status_id is not None:
        status = psqlQuery('SELECT * FROM "PatientStatus" WHERE id=%d' % status_id)
        if len(status) > 0:
            status = status[0]
            if status != "Нет Статуса":
                attrs['status'] = status['name']
    concat_attrs = ""
    if patient['attrs']:
        concat_attrs = "attrs::jsonb ||"
    psqlQuery('UPDATE "Patient" SET attrs = %s \'%s\'::jsonb WHERE id=%d;' % (concat_attrs, json.dumps(attrs), patient['id']))
    # print(attrs)



