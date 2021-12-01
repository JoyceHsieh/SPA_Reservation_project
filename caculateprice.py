from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from datetime import datetime, timedelta
from itertools import chain
from flask_bootstrap import Bootstrap
from flask import render_template, redirect, url_for, request, send_from_directory, flash
import numpy as np
from time import ctime
from time import strftime
import pandas as pd
import json
import os


# Create our database engine
engine = create_engine("sqlite:///SPA_1130.sqlite", echo=False)
#Reflect Database into ORM classes
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

# The ORM’s “handle” to the database is the Session.
from sqlalchemy.orm import Session
session = Session(engine)

GU=Base.classes.guest
RE=Base.classes.reservation
ST=Base.classes.service_type
U=Base.classes.user



#Caculate service_price
def caculate_service_price(start_time,end_time,service_id):
    start_cal=int(start_time.replace(":", ""))
    end_cal=int(end_time.replace(":", ""))
    duration=int((end_cal-start_cal)/100)

    
    service_price=session.query(ST.price).filter(ST.service_id==service_id).first()
    price_list = np.array(service_price)
    price_list.reshape(1,-1)
    service_charge=price_list*duration
    
    return service_charge



def profit_service(month):
    months=str(month)
    col_ps=[GU.guest_firstName, GU.guest_lasttName, GU.checkin_date, GU.checkout_date, 
         RE.start_time, RE.end_time, RE.service_id, RE.service_charge, RE.cancel, 
        ST.service_id, ST.service_name, ST.price]
    
    service_type_revenue=session.query(*col_ps).filter(GU.guest_id==RE.guest_id).filter(RE.cancel==False).filter(ST.service_id==RE.service_id).all()
    re_1=[]
    re_2=[]
    re_3=[]
    re_4=[]
    re_5=[]
    re_6=[]
    servicetype={1:"SPA", 2:"Swim", 3:"Massage", 4:"Sauna", 5:"Gym", 6:"Movie center"}
    
    for record in service_type_revenue:
        (gu_fn, gu_ln, gu_cid, gu_cod, re_st, re_et, re_si, re_sc, re_c, st_id, st_sn, st_p) =record
        checkin_m=gu_cid.split("-")[1]
        if checkin_m==months:
            if st_id==1:
                re_1.append(re_sc)
            elif st_id==2:
                re_2.append(re_sc)
            elif st_id==3:
                re_3.append(re_sc)
            elif st_id==4:
                re_4.append(re_sc)
            elif st_id==5:
                re_5.append(re_sc)
            elif st_id==6:
                re_6.append(re_sc)

    total_revenue_1=sum(re_1)
    total_revenue_2=sum(re_2)
    total_revenue_3=sum(re_3)
    total_revenue_4=sum(re_4)
    total_revenue_5=sum(re_5)
    total_revenue_6=sum(re_6)
    
    profit=[total_revenue_1,total_revenue_2,total_revenue_3,total_revenue_4,total_revenue_5,total_revenue_6]
    
    
    return profit


def revenue_year(year):
    year=str(year)
    col=[GU.guest_firstName, GU.guest_lasttName, GU.checkin_date, GU.checkout_date, RE.start_time, RE.end_time, RE.service_id, RE.service_charge, RE.cancel]
    
    revenue=session.query(*col).filter(GU.guest_id==RE.guest_id).filter(RE.cancel==False).all()
    revenue_Jan=[]
    revenue_Feb=[]
    revenue_Mar=[]
    revenue_April=[]
    revenue_May=[]
    revenue_June=[]
    revenue_July=[]
    revenue_Aug=[]
    revenue_Sept=[]
    revenue_Oct=[]
    revenue_Nov=[]
    revenue_Dec=[]

    for record in revenue:
        (gu_fn, gu_ln, gu_cid, gu_cod, re_st, re_et, re_si, re_sc, re_c) =record
        checkin_y=gu_cid.split("-")[0]
        checkin_m=gu_cid.split("-")[1]
        if checkin_y==year:
            if checkin_m=='01':
                revenue_Jan.append(re_sc)
            elif checkin_m=='02':
                revenue_Feb.append(re_sc)
            elif checkin_m=='03':
                revenue_Mar.append(re_sc)
            elif checkin_m=='04':
                revenue_April.append(re_sc)
            elif checkin_m=='05':
                revenue_May.append(re_sc)
            elif checkin_m=='06':
                revenue_June.append(re_sc)
            elif checkin_m=='07':
                revenue_July.append(re_sc)
            elif checkin_m=='08':
                revenue_Aug.append(re_sc)
            elif checkin_m=='09':
                revenue_Sept.append(re_sc)
            elif checkin_m=='10':
                revenue_Oct.append(re_sc)
            elif checkin_m=='11':
                revenue_Nov.append(re_sc)
            elif checkin_m=='12':
                revenue_Dec.append(re_sc)
    print(revenue_Oct)
    x=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    y=[sum(revenue_Jan), sum(revenue_Feb),sum(revenue_Mar),sum(revenue_April), sum(revenue_May), sum(revenue_June), sum(revenue_July), sum(revenue_Aug), sum(revenue_Sept), sum(revenue_Oct), sum(revenue_Nov), sum(revenue_Dec)]
    
    return  y