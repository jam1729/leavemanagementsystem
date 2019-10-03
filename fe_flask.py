from flask import Flask, render_template, request, redirect
from flask_cors import CORS as cors
import sqlite3 as sql
import sys
import postgres_dbms as db
from json import dumps

app = Flask(__name__)
cors(app)

@app.route('/')
def home():
   return render_template('home.html')

@app.route('/login')
def login():
   return render_template('login.html')

@app.route('/validate',methods = ["POST","GET"])
def validate():
   username =  dict(request.form)['uname']
   password =  dict(request.form)['pswd']
   print(request.form)
   try:
      if int(username)>=2000:                                                                   #Manager
         if(db.verifyManager(username,password,db.c)):
            return render_template('manager_home.html',username=username)
         else:
            return render_template('print_error.html',inputtext="Incorrect username or password!")
      else:                                                                                     #Employee
         if(db.verifyEmployee(username,password,db.c)):
            tab = db.viewLog(username,db.c)
            return render_template('employee_home.html',username=username)
         else:
            return render_template('print_error.html',inputtext="Incorrect username or password!")
   except Exception as e:
      return render_template('print_error.html',inputtext="Invalid ID! ("+str(e)+" )")

app.run(host = '0.0.0.0', port = 4000, debug = 1)