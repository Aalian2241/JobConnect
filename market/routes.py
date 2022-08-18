from datetime import datetime
from turtle import ht, title
import flask
from matplotlib.pyplot import hot
import glob,os
from sqlalchemy import null
import requests
from market import app
from flask import render_template, redirect, url_for, flash,session,send_file
from market.models import Item, User
from market.mongodb_import import project_database, _users
from market.forms import RegisterForm, LoginForm
from market import db
from flask_login import login_user, logout_user, login_required
from flask import Flask, request
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
from wtforms import MultipleFileField

url="http://localhost:5000/"
import os
from wtforms.validators import InputRequired
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'
app.config['history']='static/history'

@app.route('/')
@app.route('/home')
def home_page():
    if "_user_id" not in session:
        return redirect(url_for('login_page'))
    if not os.path.isdir(f"market/Users/{session['_user_id']}"):
        session['path'] = f"market/Users/{session['_user_id']}"
        os.makedirs(f"{session['path']}/seeker", exist_ok=False)
        os.makedirs(f"{session['path']}/employer/desc", exist_ok=False)
        os.makedirs(f"{session['path']}/employer/files", exist_ok=False)
    print(session)
    return render_template('indexnew.html')



@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data,
                              path=f'{form.username.data}/')

        db.session.add(user_to_create)
        
        attempted_user = User.query.filter_by(username=form.username.data).first()
        session['username']= attempted_user.username


        requests.post(url, data={'username':attempted_user.username, 
                                "user_search_results":[]})


        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('home_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    print(session)
    form = LoginForm()
    

    if form.validate_on_submit():
        

        attempted_user = User.query.filter_by(username=form.username.data).first()

        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            session['username'] = attempted_user.username
            
            return redirect(url_for('home_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():

    logout_user()
    import shutil
    print(session['path'])
    #session['path'] = f"market/Users/{session['_user_id']}"

    shutil.rmtree(session['path'])
    session.pop('path', None)
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

def upload_in_history(form):
    file = form.file.data
    file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['history'],secure_filename(file.filename)))


@app.route('/Upload', methods=['GET',"POST"])
def home():
    
    # clear contents of folder
    files = glob.glob(f"{session['path']}/seeker/*")
    for f in files:
        os.remove(f)


    form = UploadFileForm()
    # if os.path.isdir(r'C:\Users\Dell\Downloads\project_draft_1255_hours_10th_may\project\market\static\history')==False:
    #      os.mkdir(r'C:\Users\Dell\Downloads\project_draft_1255_hours_10th_may\project\market\static\history')
    # else:
    #      l=r'C:\Users\Dell\Downloads\project_draft_1255_hours_10th_may\project\market\static\history'
    # file.seek(0)

    if form.validate_on_submit():
        file = form.file.data # First grab the file
        print("file uploaded: ",file.filename)
        session['seekerFilename'] = file.filename        
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),f"Users/{session['_user_id']}/seeker",secure_filename(file.filename)))
                #file.save(os.path.join(l, secure_filename(file.name)))
        file.seek(0) # reset the cursor thingy
        return result()
    # upload_in_history(form)
    else:
        print('hello')
        return render_template('index.html', form=form)


#  
@app.route('/resultemp')
def resultemp():
    from extract import deploy_ext
    deploy_ext('employer',f"Users/{session['_user_id']}")
    from vectorize import deploy

    resumes = deploy('employer',f"{session['path']}", f"{session['path']}")
    session.pop('job_description_file', None)
    print(resumes)
    return render_template('resultsemp.html', users=resumes)


@app.route('/result')
def result():
    import pprint
    #exec(open('extract.py').read())methods=['GET',"POST"]
    from extract import deploy_ext
    print('path on result function: ',f"{session['path']}")
    deploy_ext('seeker',f"{session['path']}")

    from vectorize import deploy
    _jobs = deploy('seeker',f"{session['path']}",None)
    #os.system('python extract.py')
    #_users=_jobs['Apply Here: ']
    add_data(_jobs)

    username = session['username']
    print("USERNAME: ", username)
    to_update = _users.find_one({"username":username})
    _id = to_update["_id"]
    print(_id)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(_jobs)
    _url = f"http://localhost:5000/{_id}"
    requests.post(_url, data=_jobs)
    

    # # saving the results in mongodb...
    # _users.delete_one({"id": username})
    # save_this = {
    #     "id": username,
    #     "search_time": datetime.now(),
    #     "jobs_found": _jobs
    # }
    # _users.insert_one(save_this) 
    # user_data=_users.find_one({"id": username})

    return render_template('res.html', users=_jobs)
    #to see results type with localhost /results

class NewFileForm(FlaskForm):
    files = MultipleFileField('File(s) Upload')

@app.route('/empupload',methods=['GET',"POST"])
def empupload():
    files = glob.glob(f"{session['path']}/employer/files/*")
    for f in files:
        os.remove(f)

    form = UploadFileForm()
    if flask.request.method == "POST":
        files = flask.request.files.getlist("formmultiple")
        for file in files:
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),f"Users/{session['_user_id']}/employer/files",secure_filename(file.filename)))
 # Then save the file
    return render_template('upemp.html', form=form)


@app.route('/updes',methods=['GET',"POST"])
def updes():
    files = glob.glob(f"{session['path']}/employer/desc/*")
    for f in files:
        os.remove(f)
    form = UploadFileForm()
    if os.path.isdir(r'C:\Users\Dell\Downloads\project_draft_1255_hours_10th_may\project\market\static\history')==False:
         os.mkdir(r'C:\Users\Dell\Downloads\project_draft_1255_hours_10th_may\project\market\static\history')
    else:
         l=r'C:\Users\Dell\Downloads\project_draft_1255_hours_10th_may\project\market\static\history'

    if form.validate_on_submit():
        file = form.file.data # First grab the file
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),f"Users/{session['_user_id']}/employer/desc",secure_filename(file.filename)))
        session['job_description_file'] = file.filename 
        file.save(os.path.join(l, secure_filename(file.name)))
 # Then save the file
        return redirect(url_for('empupload'))
    else:
        return render_template('updes.html', form=form)



COUNT = 1

import sqlite3 as sql
def add_data(jobs):
    from sqlalchemy import func

    global COUNT
    

    # Adding data
    for i in range(len(jobs['Apply Here: '])):
        COUNT +=1
#_jobs = {
#'Posted By: ' : [], #['systems', 'fccu'],
#'Job Title: ' : [],
#'Salary: ' : [],
#'Apply Here: ': [],
#'Job Id: ': []
        items=Item(title=jobs['Job Title: '][i],link=jobs['Apply Here: '][i],postedby=jobs['Posted By: '][i],owner=1,salary=None)
        db.session.add(items)
        db.session.commit()

@app.route('/plot_csv')
def plot_csv():
    return send_file('outputs/result.xlsx',     
                     attachment_filename='result.xlsx',
                     as_attachment=True)

@app.route('/about')
def about():
    return render_template('about.html')