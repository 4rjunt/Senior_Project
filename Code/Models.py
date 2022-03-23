from sqlalchemy import  create_engine, Column, Integer, String, ForeignKey, Date, Interval, Time
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import Boolean
from datetime import timedelta,time,date
from os.path import exists
from pathlib import Path

Base = declarative_base()

class Usage_Date(Base):
    __tablename__= "UsageDate"
    date = Column(Date,primary_key=True,autoincrement=False,default=date.today())
    programs_used_id = relationship("Usage_Time",cascade="all,delete",backref=backref("Usage_Date"))
    computer_usage_time = Column(Time,default=time(hour=0,minute=0,second=0),nullable=False)

    def __repr__(self) -> str:
        return f"Usage Date object: Date: {self.date}. Computer Usage Time: {self.computer_usage_time}"

class Usage_Time(Base):
    __tablename__ = "UsageTime"
    program_usage_id = Column(Integer,primary_key=True)
    process_id = Column(Integer,unique=True,nullable=False)
    program_name = Column(String(100),nullable=False)
    usage_time = Column(Time,nullable=False)
    active_time = Column(Time,nullable=False)
    date = Column(Date,ForeignKey(Usage_Date.date))

    def __repr__(self) -> str:
        return f"UsageTime object: Program Usage Id: {self.program_usage_id}. PID: {self.process_id}. " \
               f"Program Name: {self.program_name}. Usage Time: {self.usage_time}. Active Time: {self.active_time}"

class Block_Apps(Base):
    __tablename__ = "BlockApps"
    program_pid = Column(Integer,primary_key=True,autoincrement=False)
    program_name = Column(String(100),nullable=False)
    time_to_block = Column(Interval,nullable=False)

    def __repr__(self) -> str:
        return f"BlockApps object: Program PID: {self.program_pid}. Program Name: {self.program_name}." \
               f"Time To Lock:{self.time_to_block}"


if not exists("database\\test.db"):
    engine = create_engine('sqlite:///C:\\Users\\Desktop\\Desktop\\SQLite\\database\\test.db')
    Base.metadata.create_all(engine)