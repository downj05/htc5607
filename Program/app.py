from flask import Flask, render_template, request, flash, redirect, url_for
import tables
from login import check as check_login
app = Flask(__name__)
app.secret_key = '5adb7e8253ee317c97e1d4b20bf7693c733d8dbe509b5cd856e603fb8f56a59c'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form["username"]
        password = request.form["password"]
        if check_login(username, password) is True:
            flash('Logged In!')
            return redirect(url_for('home'))
        else:
            flash('Incorrect!')
            return redirect(url_for('login'))

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/addcourse', methods=['GET','POST'])
def addcourse():
    if request.method == 'GET':
        return render_template('addcourse.html', programmes=tables.get_programmes_list())
    else:
        courseName = request.form["courseName"]
        credits = request.form["credits"]
        fee = request.form["fee"]
        status = request.form["status"].lower()
        programmeID = request.form["programme"]
        course = tables.Course((None, courseName,credits,fee,status,programmeID))
        course.add()
        flash("Course added successfully")
        return redirect(url_for('addcourse'))


if __name__ == ('__main__'):
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.debug = True
    app.run(host='0.0.0.0')