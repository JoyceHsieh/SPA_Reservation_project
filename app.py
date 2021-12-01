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
import os
import pandas as pd
import json
import caculateprice


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

#Set up Flask
TEMPLATE_DIR = os.path.abspath('templates')
STATIC_DIR = os.path.abspath('static')

# app = Flask(__name__) # to make the app run without any
app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.secret_key="SPA_project"
app.config['SESSION_COOKIE_SECURE'] = False
Bootstrap(app)

@app.route("/",  methods=['GET', 'POST'])
def homepage():
    return render_template('index.html', title='homepage')


@app.route("/login",  methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']

        records = session.query(U.name).all()
        name_list = np.array(records)
        name_list.reshape(1,-1)
        if username in name_list:
            password_key=session.query(U.password).filter(U.name==username).first()
            password_list = np.array(password_key)
            password_list.reshape(1,-1)
            if (password in password_list):
                if username=="Manager":
                    return redirect('/manager')
                elif username=="Clerk":
                    return redirect('/menu')
            else:
                print('Password incorrect!')
        else:
            print('Username is incorrect!')


    return render_template('login.html', title='login', msg='')


@app.route("/menu",methods=['GET', 'POST'])
def menu():
    return render_template('menu.html', title='menu', show_modal=True)

@app.route("/checkin",methods=['GET', 'POST'])
def checkin():
    if request.method == 'POST':
        fn=request.form['firstname']
        ln=request.form['lastname']
        cid=request.form['checkindate']
        cod=request.form['checkoutdate']
        group_id=request.form['groupid']
        session.add(GU(guest_firstName=fn, guest_lasttName=ln, checkin_date=cid, checkout_date=cod,group_id=group_id))
        session.new
        session.commit()
        flash('Check in success!!')
        
    return render_template('menu.html', title='menu', show_modal=True)


@app.route("/viewall",methods=['GET', 'POST'])
def viewall():
    if request.method == 'POST':
        reservation_item = session.query(RE)
    return render_template('menu.html', title='menu', show_modal=True, viewall=reservation_item )

@app.route("/inser",methods=['GET', 'POST'])
def inser():
    if request.method == 'POST':
        g_id= request.form['guestid']
        fn=request.form['firstname']
        ln=request.form['lastname']
        s_id=request.form['serviceid']
        st=request.form['starttime']
        et=request.form['endtime']
        time_created=strftime('%Y/%m/%d %H:%M:%S')

        service_charge=caculateprice.caculate_service_price(st,et,s_id)
        cancel=False
        cancel_time="N/A"

        session.add(RE(time_created=time_created, guest_id=g_id, start_time=st, end_time=et, service_id=s_id, service_charge=service_charge, cancel=cancel, cancel_time=cancel_time))
        session.new
        session.commit()
        flash('Reservation success!!')

    return render_template('menu.html', title='menu', show_modal=True )


@app.route("/cusinfo",methods=['GET', 'POST'])
def cusinfo():
    if request.method == 'POST':
        g_id= request.form['guestid']
        reservation_customer=session.query(RE).filter(RE.guest_id==g_id).all()
    return render_template('menu.html', title='menu', show_modal=True, custom_info=reservation_customer )

@app.route("/update",methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        g_id= request.form['guestid']
        s_id=request.form['serviceid']
        ns_id=request.form['newserviceid']
        st=request.form['starttime']
        et=request.form['endtime']
        time_update=strftime('%Y/%m/%d %H:%M:%S')

        service_charge=caculateprice.caculate_service_price(st,et,s_id)

        session.query(RE).filter(RE.guest_id==g_id).filter(RE.service_id==s_id).filter(RE.cancel==False)\
        .update({'service_id':ns_id, 'start_time':st, 'end_time':et,'time_created':time_update,'service_charge':service_charge})
        session.commit()
        flash('Your reservation has been changed!!')
    return render_template('menu.html', title='menu', show_modal=True )

@app.route("/cancelcheck",methods=['GET', 'POST'])
def cancelcheck():
    if request.method == 'POST':
        g_id= request.form['guestid']
        s_id=request.form['serviceid']
        reservation_info=session.query(RE).filter(RE.guest_id==g_id).filter(RE.service_id==s_id).filter(RE.cancel==False)
    return render_template('menu.html', title='menu', show_modal=True, cancel_info=reservation_info )


@app.route("/cancel",methods=['GET', 'POST'])
def cancel():
    if request.method == 'POST':
        r_id= request.form['reservationid']
        cancel=True
        cancel_time=strftime('%Y/%m/%d %H:%M:%S')
        service_charge=0
        session.query(RE).filter(RE.reservation_id==r_id).filter(RE.cancel==False)\
        .update({'service_charge':service_charge,'cancel':cancel, 'cancel_time':cancel_time })
        session.commit()
    flash('Your cancellation success, Thank you.')
    return render_template('menu.html', title='menu', show_modal=True)

@app.route("/receipt",methods=['GET', 'POST'])
def receipt():
    if request.method == 'POST':
        g_id= request.form['guestid']
        customer_info=session.query(GU).filter(GU.guest_id==g_id).all()
        reservation_customer=session.query(RE).filter(RE.guest_id==g_id).filter(RE.cancel==False).all()
        price_list=[]
        for item in reservation_customer:
            price_list.append(item.service_charge)
        total_charge=[sum(price_list)]
    return render_template('menu.html', title='menu', show_modal=True, customer_info=customer_info, reservation_customer=reservation_customer, total_charge=total_charge )


@app.route("/manager")
def manager():
    return render_template('manager.html', title='manager')

@app.route("/monthprofit",methods=['GET', 'POST'])
def monthprofit():
    if request.method == 'POST':
        year= request.form['year']
        Mresults= caculateprice.revenue_year(year)
        print(Mresults)

    return render_template('manager.html', title='manager', show_modal=True, year=year, Mresults=Mresults)



@app.route("/profitservice",methods=['GET', 'POST'])
def profitservice():
    if request.method == 'POST':
        month= request.form['month']
        results= caculateprice.profit_service(month)
        print(results)

    return render_template('manager.html', title='manager', show_modal=True, month=month, results=results)



if __name__ == "__main__":
    app.run(debug=True)