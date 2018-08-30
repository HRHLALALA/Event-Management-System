from init_database import db,create_db
create_db()
from server import app, valid_time
from flask import request, render_template,session,redirect,url_for,flash
from flask_login import LoginManager,UserMixin,login_required,login_user,current_user,logout_user
from all_user import *
from events import *
from datetime import datetime,timedelta
from EMS import EMS
from role_required import trainer_only
app.config['SECRET_KEY']='HRHLALALA'
login_manager = LoginManager()
login_manager.init_app(app)
ems = EMS()
@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method== 'POST':
        form = request.form
        username=str(form['Username'])
        password=str(form['password'])
        user = ems.valid_user(username,password)
        if user is not None:
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username or password",'alart')
            return redirect(url_for('login'))

    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    else :
        return render_template('sign.html',user_type = "user")

@app.route('/guest_form', methods=['POST', 'GET'])
def guest_form():
    if request.method== 'POST':
        form = request.form
        username=str(form['Username'])
        password=str(form['password'])
        real_name = str(form['real_name'])
        user = guest(zid="NONE",id=username,password=password,name=real_name)
        try:
            ems.add_guest(user)
        except MemberError as error:
            flash(error.message,'alart')
            return redirect('guest_form')
        return redirect(url_for('login'))
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    else :
        return render_template('sign.html',user_type = "guest")

@app.route('/dashboard',methods=['POST','GET'])
@login_required
def dashboard():
    events = ems.valid_events()
    return render_template('dashboard.html',Events=events,user=current_user)

@app.route('/sign-up',methods=['POST','GET'])
def logout():
    logout_user()
    return redirect(url_for('login'))


@login_manager.user_loader
def load_user(user_id):
    return ems.get_user_id(user_id)

@app.route('/Post_Course',methods=['GET','POST'])
@login_required
@trainer_only
def post_course():
    date_format="%Y-%m-%d"
    if request.method == 'POST':
        form = request.form
        title = str(form['Title'])
        location = str(form['Location'])
        try:
            start_date = datetime.strptime(form['Start_Date'],date_format)
            end_date = datetime.strptime(form['End_Date'],date_format)
            deadline = datetime.strptime(form['deadline'],date_format)
            EB_start = datetime.strptime(form['EB_Start_Date'],date_format)
            EB_end = datetime.strptime(form['EB_End_Date'],date_format)
        except:
            flash("Cannot Recognise the date",'alart')
            return redirect(url_for('post_course'))
        cap = int(form['Capacitor'])
        desc = str(form['Description'])
        fee=float(request.form['Fee'])
        Course = course(status="OPEN",title=title,start_date=start_date,end_date=end_date,
                    location = location,convenor=current_user.id,
                    capacitor=cap,description=desc,deregister_deadline=deadline,
                    fee=fee,EB_start=EB_start,EB_end=EB_end)
        try:
            current_user.post_event(Course)
        except (PeriodError,CapacityError,DupulicationError) as error:
            flash(error.message,'alart')
            return redirect(url_for('post_course'))
        return redirect('/Posted_Event')
    return render_template('Post_Course.html')

@app.route('/Post_Seminar',methods=['GET','POST'])
@login_required
@trainer_only
def post_seminar():
    date_format="%Y-%m-%d"
    if request.method == 'POST':
        form = request.form
        title = str(form['Title'])
        location = str(form['Location'])
        try:
            start_date = datetime.strptime(form['Start_Date'],date_format)
            end_date = datetime.strptime(form['End_Date'],date_format)
            deadline = datetime.strptime(form['deadline'],date_format)
            EB_start = datetime.strptime(form['EB_Start_Date'],date_format)
            EB_end = datetime.strptime(form['EB_End_Date'],date_format)
        except:
            flash("Invalid Date Format",'alart')
            return redirect(url_for('post_seminar'))
        desc = str(form['Description'])
        fee=float(request.form['Fee'])
        Seminar = seminar(status="OPEN",title=title,start_date=start_date,end_date=end_date,
                location = location,convenor=current_user.id,capacitor=0,
                deregister_deadline=deadline,description=desc,
                fee=fee,EB_start=EB_start,EB_end=EB_end)
        try:
            current_user.post_event(Seminar)
        except (PeriodError,CapacityError,DupulicationError) as error:
            flash(error.message,'alart')
            return redirect(url_for('post_seminar'))
        return redirect('/Posted_Event')
    return render_template('Post_Seminar.html')

@app.route('/Registered_Event',methods=['GET','POST'])
@login_required
def registered_event():
    for Event in current_user.registers:
        if Event.status == "Canceled":
            flash(Event.title+" has been Cancelled",'alart')
    return render_template('dashboard.html',user=current_user,Events=current_user.registers)

@app.route('/Posted_Event',methods=['GET','POST'])
@login_required
@trainer_only
def posted_event():
    return render_template('dashboard.html',Events=event.query.filter_by(convenor=current_user.id),user=current_user)

@app.route('/Canceled_Event',methods=['GET','POST'])
@login_required
@trainer_only
def canceled_event():
    return render_template('dashboard.html',Events=event.query.filter_by(status='Canceled'),user=current_user)

        

        
@app.route('/dashboard/<title>',methods=['GET','POST'])
@login_required
def event_details(title):
    date_format="%Y-%m-%d"
    now = datetime.now()
    event=ems.get_event_title(title)
    before_open = event.start_date-now
    after_end = now-event.end_date
    before_deadline = event.deregister_deadline-now
    enable=True
    if event.status=="Closed" or event.status=="Canceled":
        enable=False
    if current_user.id== event.convenor:
        if after_end.days> 0:
            mode="Close"
        else:
            if before_open.days<0:
                enable=False
            mode="Cancel"
    else:
        if event in current_user.registers:
            if before_deadline.days <0:
                enable=False
            mode = "deregister"
        else:
            if event.is_full==True:
                enable=False
            mode = "register"
    if request.method == "POST":
        if "Cancel" in request.form:
            event.status="Canceled"
            db.session.commit()
        elif "Close" in request.form:
            event.status="Closed"
            db.session.commit()
        elif "register" in request.form:
            event.attendees.append(current_user)
            db.session.commit()
        else:
            event.attendees.remove(current_user)
            db.session.commit()
        return redirect(url_for('event_details',title=title))
    if before_deadline.days <0:
        permit_deregister= False
    else:
        permit_deregister = True
    return render_template('Event_Detail.html',user=current_user,event=event,mode=mode,enable=enable,deregister=permit_deregister)

@app.route('/dashboard/<title>/Sessions',methods=['GET','POST'])
@login_required
def post_session(title):
    event=ems.get_event_title(title)
    if request.method=="POST":
        speaker = request.form['Speaker']
        name = request.form['Name']
        capacitor=int(request.form['Capacitor'])
        Session = session(title=name,speaker=speaker,capacitor=capacitor,seminar_id=event.id)
        try:
            current_user.post_session(Session)
        except (SpeakerError,CapacityError,DupulicationError) as error:
            flash(error.message,'alart')
            return redirect(url_for('post_session',title=event.title))
        return redirect(url_for('event_details',title=event.title))
    return render_template('Post_Sessions.html',event=event)

@app.route('/<seminar_tit>/<session_tit>',methods=['GET','POST'])
@login_required
def register_session(seminar_tit,session_tit):
    seminar=ems.get_event_title(seminar_tit)
    session=seminar.get_session_title(session_tit)
    if current_user in session.attendees:
        session.deregister(current_user)
    else:
        session.register(current_user) 
    return redirect(url_for('event_details',title=seminar_tit))
    