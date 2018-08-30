from init_database import db
from all_user import *
from datetime import datetime,timedelta
event_to_user = db.Table('event_to_user',
    db.Column('E-mail',db.String,db.ForeignKey('user.id')),
    db.Column('event_id',db.Integer,db.ForeignKey('event.id'))
)

class event(db.Model):
    __tablename__='event'
    id = db.Column('id',db.Integer,primary_key=True)
    status = db.Column('status',db.String)
    title = db.Column('title',db.String)
    type = db.Column('type',db.String)
    location =db.Column('Location',db.String)
    convenor = db.Column('convenor',db.String)
    capacitor = db.Column('capacitor',db.Integer)
    description = db.Column('description',db.Text)
    deregister_deadline=db.Column('schedule_date',db.DateTime)
    start_date = db.Column('Start_Date',db.DateTime)
    end_date = db.Column('End_Date',db.DateTime)
    fee = db.Column('Fee',db.Float)
    EB_start = db.Column('EB_Start_Date',db.DateTime)
    EB_end = db.Column('EB_end_Date',db.DateTime)
    attendees = db.relationship('user',secondary=event_to_user,backref=db.backref('registers',lazy='dynamic'))
    __mapper_args__={
        'polymorphic_identity':'Event',
        'polymorphic_on':type
    }
    @property
    def n_attendees(self):
        return len(self.attendees)
    @property
    def is_full(self):
        if self.n_attendees==self.capacitor:
            return True
        else:
            return False
    def cal_fee(self,user):
        if user.role !="guest":
            return 0
        else:
            now = datetime.now()
            before_start = self.EB_start-now
            after_end = now - self.EB_end
            if before_start.days < 0 and after_end.days <0:
                return self.fee*0.5
            else:
                return self.fee

class course(event):
    __tablename__ = "course"
    id = db.Column(db.Integer,db.ForeignKey('event.id'),primary_key=True)
    __mapper_args__={
        'polymorphic_identity':'Course',
    }
class seminar(event):
    __tablename__="seminar"
    id = db.Column(db.Integer,db.ForeignKey('event.id'),primary_key=True)
    sessions=db.relationship("session",backref='seminar')
    __mapper_args__={
        'polymorphic_identity':'Seminar',
    }
    @property
    def n_sessions(self):
        return len(self.sessions)
    def add_capacitor(self,session):
        self.capacitor = self.capacitor+session.capacitor
    def get_session_title(self,title):
        for session in self.sessions:
            if session.title == title:
                return session
    def is_attendee(self,user):
        for Session in self.sessions:
            if user in Session.attendees:
                return True
        return False

    @property
    def speakers(self):
        speakers=[]
        for session in self.sessions:
            if session.speaker not in speakers:
                speakers.append(session.speaker)
        return speakers

session_to_event = db.Table('session_to_event',
    db.Column('E-mail',db.String,db.ForeignKey('user.id')),
    db.Column('session_id',db.Integer,db.ForeignKey('session.id'))
)
class session(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    seminar_id = db.Column(db.Integer,db.ForeignKey('seminar.id'))
    title = db.Column(db.String)
    capacitor=db.Column(db.Integer)
    speaker = db.Column(db.String)
    attendees = db.relationship('user',secondary=session_to_event,backref=db.backref('reg_session',lazy='dynamic'))
    def register(self,user):
        self.attendees.append(user)
        if user not in self.seminar.attendees:
            self.seminar.attendees.append(user)
        db.session.commit()
    def deregister(self,user):
        self.attendees.remove(user)
        Seminar = self.seminar
        if Seminar.is_attendee(user) == False:
            Seminar.attendees.remove(user)
        db.session.commit()
    @property
    def n_attendees(self):
        return len(self.attendees)
    @property
    def is_full(self):
        if self.n_attendees==self.capacitor:
            return True
        else:
            return False
    def cal_fee(self,user):
        if self.speaker == user.name:
            return 0
        elif user.role != "guest":
            return 0
        else:
            return self.seminar.cal_fee(user)
        