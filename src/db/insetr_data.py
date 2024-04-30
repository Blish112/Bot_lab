
import os
from model import Building, Schedule, Subject, Class, url_postgresql_sync, Group ,Departure, Program

from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker

cwd = os.getcwd()
files = os.listdir(cwd)  

engine = create_engine(url_postgresql_sync, echo=True)
session = sessionmaker(engine, expire_on_commit=False)

def fill_db(sess):
    def read_csv(filename):
        with open(f".\static_data\{filename}.csv", "r", encoding="utf-8") as f:
            result = [line.strip() for line in f]
        return [r.split(",") for r in result]

    # classes = read_csv("classes")
    # buildings = read_csv("buildings")
    classes= read_csv("classes")
    # subjects=read_csv("subjects")
    #schedules=read_csv("schedule")
    #groups=read_csv("groups")
    #departures=read_csv("departures")
    #programs=read_csv("programs")
    
    # ! Это работает
    with sess() as session:
        with session.begin():
            for s in classes:
                schel = Class(
                    id=int(s[0]),
                    weekday=int(s[1]),
                    class_number=int(s[2]),
                    numerator=True if int(s[3]) == 1 else False,
                    id_subject=int(s[4]),
                    id_schedule=int(s[5]),
                    id_group=int(s[6])         
                )
                
                session.add(schel)

if __name__ == "__main__":
    print("connecting...")
    print("connection established")

    fill_db(session)
    print("db filled with data")
    
    session().close()

    print("session closed")
