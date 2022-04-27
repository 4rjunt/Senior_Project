'''
Database Table Models
Made by: Justin Nunez
Date: 3/1/2022
Description: Create the blueprints of the database and the tables inside of it 
'''
from sqlalchemy import  create_engine, Column, Integer, String, ForeignKey, Date, Interval, Time
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from datetime import timedelta,date
from os.path import exists
import os

Base = declarative_base()

# Definition of tables with its values for the database

class Usage_Date(Base):
    __tablename__= "UsageDate"
    date = Column(Date,primary_key=True,autoincrement=False,default=date.today())
    programs_used_id = relationship("Usage_Time",cascade="all,delete",backref=backref("Usage_Date"))
    computer_usage_time = Column(Interval,nullable=False,default=timedelta(hours=0,minutes=0,seconds=0))

    def __repr__(self) -> str:
        return f"Usage Date object: Date: {self.date}. Computer Usage Time: {self.computer_usage_time}"

class Usage_Time(Base):
    __tablename__ = "UsageTime"
    program_usage_id = Column(Integer,primary_key=True)
    process_id = Column(Integer,unique=True,nullable=False)
    program_name = Column(String(100),nullable=False)
    usage_time = Column(Interval,nullable=False)
    active_time = Column(Interval,nullable=False)
    date = Column(Date,ForeignKey('UsageDate.date'))

    def __repr__(self) -> str:
        return f"UsageTime object: Program Usage Id: {self.program_usage_id}. PID: {self.process_id}. " \
               f"Program Name: {self.program_name}. Usage Time: {self.usage_time}. Active Time: {self.active_time}"

class Block_Apps(Base):
    __tablename__ = "BlockApps"
    program_blocked_id = Column(Integer,primary_key=True)
    program_name = Column(String(100),nullable=False)
    time_to_block = Column(Interval,nullable=False,default=timedelta(hours=0,minutes=0,seconds=0))

    def __repr__(self) -> str:
        return f"BlockApps object: Program PID: {self.program_pid}. Program Name: {self.program_name}." \
               f"Time To Lock:{self.time_to_block}"

# Check if the folder exists, if not creates one
if not exists("Save"):
    os.mkdir("Save")

# Check if the database exists, if not create one
if not exists("Save\\Kairos.db"):
    engine = create_engine('sqlite:///Save\\Kairos.db')
    Base.metadata.create_all(engine)