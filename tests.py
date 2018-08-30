import pytest
from init_database import db,create_db
create_db()
from all_user import *
from events import *
from datetime import datetime
from user_error import *

aaa = guest(id="aaa@abc.com",zid="NONE",name="aaa",password="aaa")
bbb = trainee(id="511@unsw.com",zid="511",name="bbb",password="bbb")
ccc = trainer(id="911@unsw.com",zid="911",name="ccc",password="ccc")
db.session.add(aaa)
db.session.add(bbb)
db.session.add(ccc)
db.session.commit()

status="OPEN"
title="seminar"
location="unsw"
convenor="aaa"
capacitor=0
description="xxx"
date_format="%Y-%m-%d"
fee=100.64
start_date=datetime.strptime("2018-5-26",date_format)
end_date = datetime.strptime("2018-6-26",date_format)
EB_start = datetime.strptime("2018-5-26",date_format)
EB_end = datetime.strptime("2018-6-26",date_format)

def test_user():
    aaa = guest(id="aaa@abc.com",zid="NONE",name="aaa",password="aaa")
    bbb = trainee(id="511@unsw.com",zid="511",name="bbb",password="bbb")
    ccc = trainer(id="911@unsw.com",zid="911",name="ccc",password="ccc")
    db.session.add(aaa)
    db.session.add(bbb)
    db.session.add(ccc)
    db.session.commit()
    test = True
    if aaa.role !="guest" or bbb.role!="trainee" or ccc.role!="trainer":
        test = False
    assert test==True
#-----------------------for seminar-------------------------------
def test_post_wrong_open_period():
    start_date=datetime.strptime("2018-5-26",date_format)
    end_date = datetime.strptime("2018-4-26",date_format)
    EB_start = datetime.strptime("2018-5-26",date_format)
    EB_end = datetime.strptime("2018-6-26",date_format)
    s = seminar(status=status,title=title,
            location=location,convenor=convenor,capacitor=capacitor,
            description=description,
            start_date=start_date,
            end_date=end_date,fee=fee,EB_start=EB_start,EB_end=EB_end)
    with  pytest.raises(PeriodError) as error:
        ccc.post_event(s)
    assert str(error.value) == "Negative open period"

def test_post_wrong_EB_perid():
    start_date=datetime.strptime("2018-5-26",date_format)
    end_date = datetime.strptime("2018-6-26",date_format)
    EB_start = datetime.strptime("2018-5-26",date_format)
    EB_end = datetime.strptime("2018-4-26",date_format)
    s = seminar(status=status,title=title,
            location=location,convenor=convenor,capacitor=capacitor,
            description=description,
            start_date=start_date,
            end_date=end_date,fee=fee,EB_start=EB_start,EB_end=EB_end)
    with pytest.raises(PeriodError) as error:
        ccc.post_event(s)
    assert str(error.value) == "Negative Early Bird Period"

def test_post_all_wrong_period():
    start_date=datetime.strptime("2018-5-26",date_format)
    end_date = datetime.strptime("2018-4-26",date_format)
    EB_start = datetime.strptime("2018-5-26",date_format)
    EB_end = datetime.strptime("2018-4-26",date_format)
    s = seminar(status=status,title=title,
            location=location,convenor=convenor,capacitor=capacitor,
            description=description,
            start_date=start_date,
            end_date=end_date,fee=fee,EB_start=EB_start,EB_end=EB_end)
    with  pytest.raises(PeriodError) as error:
        ccc.post_event(s)
    assert str(error.value) == "Negative Open and Early Bird period"
    
    
def test_trainee_post_allowence():
    start_date=datetime.strptime("2018-5-26",date_format)
    end_date = datetime.strptime("2018-6-26",date_format)
    EB_start = datetime.strptime("2018-5-26",date_format)
    EB_end = datetime.strptime("2018-6-26",date_format)
    s = seminar(status=status,title=title,
            location=location,convenor=convenor,capacitor=capacitor,
            description=description,
            start_date=start_date,
            end_date=end_date,fee=fee,EB_start=EB_start,EB_end=EB_end)
    try:
        aaa.post_event(s)
    except AttributeError as error:
        assert 1==1
    else:
        pytest.fail("should not have attribute 'post'")  

Seminar = seminar(status=status,title=title,
        location=location,convenor=convenor,capacitor=capacitor,
        description=description,
        start_date=start_date,
        end_date=end_date,fee=fee,EB_start=EB_start,EB_end=EB_end)
ccc.post_event(Seminar)
def test_correctly_seminar_post():
    assert event.query,filter_by(type="Seminar")[0]==Seminar
#----------------for session -----------------------------------
name = "session"
def test_add_speaker_with_space_in_session():
    speaker = " daniel"
    capacitor = 1
    Session = session(title=name,speaker=speaker,
        seminar_id =Seminar.id ,capacitor=capacitor)
    with pytest.raises(SpeakerError) as error:
        ccc.post_session(Session)
    assert str(error.value) == "Do not have space at the front or end of the speaker"

def test_negative_capacity_in_session():
    speaker = "daniel"
    capacitor = -1
    Session = session(title=name,speaker=speaker,
        seminar_id =Seminar.id ,capacitor=capacitor)
    with pytest.raises(CapacityError) as error:
        ccc.post_session(Session)
    assert str(error.value)=="capacitor should not be negative"

speaker = "daniel"
capacitor = 1
Session = session(title=name,speaker=speaker,capacitor=capacitor,seminar_id=Seminar.id)
ccc.post_session(Session)
def test_add_right_in_session():
    assert session.query.filter_by(id=Session.id)[0]==Session

def test_session_related_to_seminar():
    assert Session.seminar == Seminar
def test_update_seminar_capacity():
    assert Seminar.capacitor == Session.capacitor

#------------------test register----------------------------------------
status="OPEN"
title="seminar-2"
location="unsw"
convenor="ccc"
capacitor=0
description="xxx"
date_format="%Y-%m-%d"
fee=100.64
start_date=datetime.strptime("2018-5-26",date_format)
end_date = datetime.strptime("2018-7-26",date_format)
EB_start = datetime.strptime("2018-5-29",date_format)
EB_end = datetime.strptime("2018-7-26",date_format)
Seminar_2 = seminar(status=status,title=title,
        location=location,convenor=convenor,capacitor=capacitor,
        description=description,
        start_date=start_date,
        end_date=end_date,fee=fee,EB_start=EB_start,EB_end=EB_end)
ccc.post_event(Seminar_2)

capacitor = 1
Session_2 = session(title=name,speaker="Daniel",capacitor=capacitor,seminar_id=Seminar_2.id)
ccc.post_session(Session_2)
Session_3 = session(title="session_3",speaker="Jackson",capacitor=capacitor,seminar_id=Seminar_2.id)
ccc.post_session(Session_3)

Daniel = guest(id="daniel@abc.com",zid="NONE",name="Daniel",password="aaa")
Jackson = guest(id="jackson@abc.com",zid="NONE",name="Jackson",password="aaa")
John = trainee(id="john@unsw.com",zid="NONE",name="John",password="aaa")
Session_2.register(Daniel)#guest-speaker
Session_2.register(Jackson)#guest-non-speaker
Session_2.register(John)#trainee
Session_3.register(Daniel)
def test_register_session_attendee():
    assert Daniel in Session_2.attendees

def test_in_session_register_seminar_attendees():
    assert Daniel in Seminar_2.attendees
#-------------------before early bird test----------------
def test_before_EB_daniel_fee_session_2():
    assert Session_2.cal_fee(Daniel)==0
def test_before_EB_daniel_fee_session_3():
    assert Session_3.cal_fee(Daniel)==100.64

def test_before_EB_jackson_fee_session_2():
    assert Session_2.cal_fee(Jackson)==100.64

def test_before_EB_jackson_fee_session_2():
    assert Session_3.cal_fee(Jackson)==0

def test_before_EB_John_fee():
    assert Session_2.cal_fee(John)==0
#------------------during early bird test-------------------


def test_During_EB_Daniel_fee_session_2():
    EB_start = datetime.strptime("2018-5-25",date_format)
    Seminar_2.EB_start = EB_start
    assert Session_2.cal_fee(Daniel)==0
def test_During_EB_Daniel_fee_session_3():
    EB_start = datetime.strptime("2018-5-25",date_format)
    Seminar_2.EB_start = EB_start
    assert Session_3.cal_fee(Daniel)==100.64/2

def test_During_EB_jackson_fees_session_2():
    EB_start = datetime.strptime("2018-5-25",date_format)
    Seminar_2.EB_start = EB_start
    assert Session_2.cal_fee(Jackson)==100.64/2

def test_During_EB_john_fee():
    EB_start = datetime.strptime("2018-5-25",date_format)
    Seminar_2.EB_start = EB_start
    assert Session_2.cal_fee(John)==0
#---------------------After Early Bird Test-----------------------

def test_After_EB_daniel_fee():
    EB_end = datetime.strptime("2018-4-20",date_format)
    Seminar_2.EB_end = EB_end
    assert Session_2.cal_fee(Daniel)==0

def test_After_EB_jackson_fee():
    EB_end = datetime.strptime("2018-4-20",date_format)
    Seminar_2.EB_end = EB_end
    assert Session_2.cal_fee(Jackson)==100.64

def test_After_EB_john_fee():
    EB_end = datetime.strptime("2018-4-20",date_format)
    Seminar_2.EB_end = EB_end
    assert Session_2.cal_fee(John)==0

#------------------------------normal in-school user test------------------------
def test_dupulication_session():
    Session_4 = session(title="session_3",speaker="Jackson",capacitor=capacitor,seminar_id=Seminar_2.id)
    with pytest.raises(DupulicationError) as error:
        ccc.post_session(Session_4)
    assert str(error.value) =="This session exists"

def test_dupulication_seminar():
    Seminar_3 = seminar(status=status,title=title,
        location=location,convenor=convenor,capacitor=capacitor,
        description=description,
        start_date=start_date,
        end_date=end_date,fee=fee,EB_start=EB_start,EB_end=EB_end)
    with pytest.raises(DupulicationError) as error:
        ccc.post_event(Seminar_3)
    assert str(error.value) =="This event exists"