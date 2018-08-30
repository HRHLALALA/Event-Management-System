
from flask_login import UserMixin
import csv
from init_database import db
from user_error import *
class user(UserMixin,db.Model):
    __tablename__='user'
    id = db.Column('id',db.String,primary_key=True) ##email
    zid = db.Column('zid',db.String)
    name=db.Column('name',db.String)
    password=db.Column('password',db.String)
    role = db.Column('role',db.String)
    __mapper_args__={
        'polymorphic_identity':'user',
        'polymorphic_on':role
    } 
        

class trainer(user):
    __tablename__='trainer'
    id = db.Column(db.String,db.ForeignKey('user.id'),primary_key=True)
    __mapper_args__={
        'polymorphic_identity':'trainer',
    }
    def post_event(self,Event):
        from route import ems
        diff_period= Event.start_date - Event.end_date
        diff_EB = Event.EB_start-Event.EB_end
        if diff_period.days<0 and diff_EB.days >0:
            raise PeriodError("Negative Early Bird Period")
        if diff_period.days>0 and diff_EB.days <0:
            raise PeriodError("Negative open period")
        if diff_period.days>0 and diff_EB.days >0:
            raise PeriodError("Negative Open and Early Bird period")
        if Event.capacitor<0:
            raise CapacityError("capacitor should not be negative")
        if ems.get_event_title(Event.title)!=None:
            raise DupulicationError("This event exists")
        db.session.add(Event)
        db.session.commit()
    def post_session(self,Session):
        from route import ems
        if Session.speaker[0]==" " or Session.speaker.endswith(" "):
            raise SpeakerError("Do not have space at the front or end of the speaker")
        if Session.capacitor<0:
            raise CapacityError("capacitor should not be negative")
        if ems.dupulicate_session(Session):
            raise DupulicationError("This session exists")
        db.session.add(Session)
        db.session.commit()
        Seminar = Session.seminar
        Seminar.add_capacitor(Session)

class trainee(user):
    __tablename__='trainee'
    id = db.Column(db.String,db.ForeignKey('user.id'),primary_key=True)
    __mapper_args__={
        'polymorphic_identity':'trainee',
    }

class guest(user):
    __tablename__='guest'
    id =db.Column(db.String,db.ForeignKey('user.id'),primary_key=True)
    __mapper_args__={
        'polymorphic_identity':'guest'
    }