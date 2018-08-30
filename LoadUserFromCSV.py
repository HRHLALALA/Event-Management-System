from all_user import *
import csv
from init_database import db
def loadcsv():
    trainer_1 = trainer(name="aaa",zid="aaa",id="aaa",password="aaa")
    db.session.add(trainer_1)
    trainee_1 = trainee(name="bbb",zid="bbb",id="bbb",password="bbb")
    db.session.add(trainee_1)
    with open('user.csv') as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)
        for row in f_csv:
            if row[4] == "trainer":
                Trainer = trainer(name=row[0],zid=row[1],id=row[2],password=row[3])
                db.session.add(Trainer)
            else:
                Trainee = trainee(name=row[0],zid=row[1],id=row[2],password=row[3])
                db.session.add(Trainee)
        db.session.commit()
