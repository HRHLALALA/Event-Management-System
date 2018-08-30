from events import *

class MemberError(Exception):
    def __init__(self,message):
        self.message = message

class PeriodError(Exception):
    def __init__(self,message):
        self.message = message

class SpeakerError(Exception):
    def __init__(self,message):
        self.message = message

class CapacityError(Exception):
    def __init__(self,message):
        self.message = message

class DupulicationError(Exception):
    def __init__(self,message):
        self.message = message

