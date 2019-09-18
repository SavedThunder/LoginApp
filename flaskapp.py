from flask import Flask, url_for, render_template, request, Response, flash, session
from flask_static_compress import FlaskStaticCompress
from forms import SignUp, SignUp2
import config
import sys
import mysql.connector
# import json
from collections import Counter

myConnection = mysql.connector.connect(host='localhost', user='ubuntu', password='ubuntu', db='users')
myConnection.autocommit = True
app = Flask(__name__, static_folder="static", template_folder="templates")
app.config['TESTING'] = True
app.config['SECRET_KEY'] = b'\x0c\xce\x93\xed\x11_\xa4\x97|\xd7~h\n\xd2\x82:'
app.static_folder = 'static'
compress = FlaskStaticCompress(app)

dbcursor = myConnection.cursor()
username = ""
@app.route('/')
def signup():
    return render_template('signup.html')

@app.route('/signup2', methods=['GET', 'POST'])
def register():
    """Sign Up  Page."""
    username = request.form['Username']
    pword = request.form['Password']
    

    sql_wrong = "select * from user_info where username=%s and password <> %s"
    val = (username, pword)
    dbcursor.execute(sql_wrong, val)
    result = dbcursor.fetchone()
    if result:
        return render_template('signup.html', error = "This user already exists - you have entered the wrong password")

    sql = "select * from user_info where username=%s and password=%s;"
    val = (username, pword)
    dbcursor.execute(sql, val)
    result = dbcursor.fetchone()
    if result:
        session['loggedin'] = True
        session['username'] = username
        session['password'] = pword
        sql = "select fname, lname, email from user_info where username=%s"
        val = (session['username'],)
        dbcursor.execute(sql, val)
        info = dbcursor.fetchone()
        session['FirstName'] = info[0]
        session['LastName'] = info[1]
        session['Email'] = info[2]

        return render_template('dashboard.html', fname = session['FirstName'], lname = session['LastName'], email = session['Email'] )
    else:
        sql = "insert into user_info (username, password) values (%s, %s);"
        val = (username, pword)
        dbcursor.execute(sql, val)

        session['username'] = username
        session['password'] = pword
        return render_template('signup2.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dash():
    fname = request.form['FirstName']
    lname = request.form['LastName']
    email = request.form['Email']

    session['FirstName'] = fname
    session['LastName'] = lname
    session['Email'] = email
    
    sql = "update user_info set fname = %s, lname = %s, email = %s where username = %s"
    vals = (fname, lname, email, session['username'])
    dbcursor.execute(sql, vals)

    return render_template('dashboard.html', fname = session['FirstName'], lname = session['LastName'], email = session['Email'])

if __name__ == '__main__':
    app.run()
