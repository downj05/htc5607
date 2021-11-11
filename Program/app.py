import flask_login
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import LoginManager, login_required
import tables
from login import check as check_login, user_exists
app = Flask(__name__)
app.secret_key = '5adb7e8253ee317c97e1d4b20bf7693c733d8dbe509b5cd856e603fb8f56a59c'
login_manager = LoginManager()
login_manager.init_app(app)


class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(username):
    if user_exists(username):
        user = User()
        user.id = username
        return user
    else:
        return


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    if user_exists(username):
        user = User()
        user.id = username
        return user
    else:
        return


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form["username"]
        password = request.form["password"]
        if check_login(username, password) is True:
            user = User()
            user.id = username
            flask_login.login_user(user)
            flash('Logged In!')
            return redirect(url_for('home'))
        else:
            flash('Incorrect!')
            return redirect(url_for('login'))


@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('unauthorized.html')


@app.route('/logout')
def logout():
    flask_login.logout_user()
    flash('Logged out!')
    return redirect(url_for('login'))


@app.route('/home')
@login_required
def home():
    return render_template('home.html')


@app.route('/addcourse', methods=['GET','POST'])
@login_required
def addcourse():
    if flask_login.current_user.id != 'p_admin':
        flash('No Permission!')
        return redirect(url_for('home'))
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
        return render_template('addcourse.html', programmes=tables.get_programmes_list(), continuePrompt=True,
                               continueMessage="Would you like to add another course?")


@app.route('/updatecourse', methods=['GET','POST'])
@login_required
def updatecourse():
    if flask_login.current_user.id != 'p_admin':
        flash('No Permission!')
        return redirect(url_for('home'))
    if request.method == 'GET':
        return render_template('updatecourse.html', courses=tables.get_courses_list())
    else:
        courseID = request.form["courseID"]
        courseName = request.form["courseName"]
        credits = request.form["credits"]
        fee = request.form["fee"]
        status = request.form["status"].lower()
        # fetch course from id, get its programme id
        old_course = tables.get_course_from_id(courseID)

        course = tables.Course((courseID, courseName,credits,fee,status,old_course.programmeID))
        course.update()
        flash("Course updated successfully!")
        return render_template('updatecourse.html', courses=tables.get_courses_list(), continuePrompt=True,
                               continueMessage="Would you like to update another course?")


@app.route('/deletecourse', methods=['GET', 'POST'])
@login_required
def deletecourse():
    if flask_login.current_user.id != 'p_admin':
        flash('No Permission!')
        return redirect(url_for('home'))
    if request.method == 'GET':
        return render_template('deletecourse.html', courses=tables.get_courses_list(True))
    else:
        courseID = request.form["courseID"]
        course = tables.get_course_from_id(courseID)
        course.delete()
        flash("Course deleted successfully!")
        return render_template('deletecourse.html', courses=tables.get_courses_list(True),
                               continuePrompt=True, continueMessage="Would you like to delete another course?")


@app.route('/coursereport', methods=['GET', 'POST'])
@login_required
def coursereport():
    if flask_login.current_user.id != 'p_admin':
        flash('No Permission!')
        return redirect(url_for('home'))
    if request.method == 'GET':
        return render_template('coursereport.html')
    else:
        # Generate report
        courses = tables.get_courses_list()
        response = {
            "courses": [],
        }
        for course in courses:
            enrolment_count = len(tables.get_enrolments_from_course(course))
            assessment_count = len(tables.get_assessments_from_course(course))
            programme_name = tables.get_programme_from_id(course.programmeID).name
            response_object = {
                "name": course.name,
                "id": course.id,
                "credits": course.credits,
                "status": course.status,
                "fee": course.fee,
                "programme": programme_name,
                "enrolments": enrolment_count,
                "assessments": assessment_count
            }
            response["courses"].append(response_object)
        return response

@app.route('/addprogramme', methods=['GET','POST'])
@login_required
def addprogramme():
    if flask_login.current_user.id != 'p_admin':
        flash('No Permission!')
        return redirect(url_for('home'))
    if request.method == 'GET':
        return render_template('addprogramme.html')
    else:
        name = request.form["programmeName"]
        level = request.form["level"]
        programme = tables.Programme((None, name,level))
        programme.add()
        flash("Course added successfully")
        return render_template('addprogramme.html', continuePrompt=True,
                               continueMessage="Would you like to add another programme?")

@app.route('/api/<command>', methods=['GET', 'POST'])
@login_required
def api(command):
    if command == 'course':
        request_json = request.get_json()
        id = request_json['id']
        course = tables.get_course_from_id(id)
        course_json = {
            "id": course.id,
            "name": course.name,
            "credits": course.credits,
            "fee": course.fee,
            "status": course.status,
            "programmeID": course.programmeID
        }
        return course_json

    elif command == 'programme':
        request_json = request.get_json()
        id = request_json['id']
        programme = tables.get_programme_from_id(id)
        programme_json = {
            "id": programme.id,
            "name": programme.name,
            "level": programme.level
        }
        return programme_json


if __name__ == ('__main__'):
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.debug = True
    app.run(host='0.0.0.0')