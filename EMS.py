from all_user import *
from events import *

class EMS:
    def __init__(self):
        self._users = user.query.order_by(user.id).all()
        self._events = event.query.order_by(event.id).all()
    @property
    def users(self):
        self._users=user.query.order_by(event.id).all()
        return self._users
    @property
    def events(self):
        self._events = event.query.order_by(event.id).all()
        return self._events 
        
    def valid_user(self,email,password):
        valid_user = user.query.filter_by(id=email,password=password).first()
        if valid_user is not None:
                return valid_user
        return None

    def get_user_id(self,id):
        valid_user=user.query.filter_by(id=id).first()
        if valid_user is not None:
            return valid_user
        return None
    def get_event_title(self,title):
        return event.query.filter_by(title = title).first()
    def dupulicate_session(self,Session):
        check=session.query.filter_by(title=Session.title).first()
        if check != None  and check.seminar_id == Session.seminar_id:
            return  True
        else:
             return False
        

    def get_event_id(self,id):
        return event.query.filter_by(id=id),first()
    def valid_events(self):
        valids = event.query.filter_by(status="OPEN").all()
        for valid in valids:
            if valid.type == "Seminar":
                if valid.n_sessions==0:
                    valids.remove(valid)
        return valids
    def add_guest(self,guest):
        if guest.name.endswith(" ") or guest.name.startswith(" "):
            raise MemberError("You should not have space at from or end of the name")
        if "@" not in guest.id:
            raise MemberError("invalid E-mail address")
        user = self.valid_user(guest.id,guest.password)
        if user is not None:
            raise MemberError("This User Name exsists")
        db.session.add(guest)
        db.session.commit()
    

            
