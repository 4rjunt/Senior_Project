'''
Database Controller
Made by: Justin Nunez
Date: 3/10/2022
Description: Its the object that creates a connection with the database
'''
from time import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,scoped_session
from sqlalchemy.orm.session import Session
from Models import Usage_Date, Usage_Time, Block_Apps
from datetime import date as ActualDate
from datetime import time
from os.path import exists
import os

class Controller:

    # Create a session to interact with the database 
    def __init__(self) -> None:
        engine = create_engine(
            'sqlite:///Save\\Kairos.db'
        )
        self.__session = scoped_session(sessionmaker(bind=engine))         

    # Add an element to the NotUsableApps file, if the file doesn't exist creates one 
    def update_not_usable_applications(self,not_usable_applications=None,mode=0):
        if not exists("Save"):
            os.mkdir("Save")
        wfile = open("Save\\NotUsableApps.txt","a")
        if mode==0:
            for program in not_usable_applications:
                file = open("Save\\NotUsableApps.txt","r")
                file.close()
                lines = file.readlines()
                for line in lines:
                    index=lines.index(line)
                    lines[index]=line.strip()
                if program not in lines:
                    wfile.write(program+"\n")
            wfile.close()    
        else:
            file = open("Save\\NotUsableApps.txt","r")
            lines = file.readlines()
            for line in lines:
                index=lines.index(line)
                lines[index]=line.strip()
            file.close()
            return lines

    # Add a date to the datebase
    def add_date(self,_date):
        new_date = Usage_Date(date = _date)
        self.__session.add(new_date)
        self.__session.commit()

    # Returns all the dates of the database, or only one if specified
    def get_dates(self,_date=None):
        if _date is None:
            return Usage_Date.date
        else:
            dates = self.__session.query(Usage_Date).filter(Usage_Date.date==_date).first()
            return dates
    
    # Update a specific date in the database
    def update_dates(self,_date,_time):
            self.__session.query(Usage_Date).filter(Usage_Date.date==_date).update({'computer_usage_time':_time})
            self.__session.commit()
    
    # Add a new program in the database, if a date specified, the program is added with that date else is added with today's date
    def add_new_program(self,_process_id,_program_name,_usage_time,_active_time,_date=None):
        if _date is None:
            today_date = ActualDate.today()
        else:
            today_date = _date
        program = Usage_Time(process_id=_process_id,
                           program_name=_program_name, usage_time = _usage_time,
                           active_time=_active_time,date = today_date)
        self.__session.add(program)
        self.__session.commit()

    # Returns the programs of one specific date
    def get_times_programs(self,_date):
        programs = self.__session.query(Usage_Time).filter(Usage_Time.date ==_date).all()
        return programs

    # Add a block program in the database
    def add_block_program(self,_program_name,_time_to_block):
        program_to_block = Block_Apps(program_name=_program_name,time_to_block=_time_to_block)
        self.__session.add(program_to_block)
        self.__session.commit()

    # Update a list of programs in the database
    def update_programs_time(self,process_id_name,_Usage_time,_Active_time,_Date):
        for program in process_id_name.values():
            Exists = self.__session.query(Usage_Time).filter(Usage_Time.date==_Date,Usage_Time.program_name==program).first()
            if Exists is not None:
                self.__session.query(Usage_Time).filter(Usage_Time.date==_Date,Usage_Time.program_name==program).update({'usage_time': _Usage_time[program]})
                self.__session.query(Usage_Time).filter(Usage_Time.date==_Date,Usage_Time.program_name==program).update({'active_time': _Active_time[program]})
                self.__session.commit()           
            else:
                process_id = None
                for key in process_id_name.keys():
                    if process_id_name[key] == program:
                        process_id = key
                        break
                self.add_new_program(_process_id=process_id,_program_name=program,_usage_time=_Usage_time[program],_active_time=_Active_time[program],_date=_Date)
    
    # Either delete or update a block program in the database 
    # If update is chosen, a list of programs can be updated
    def update_block_programs(self,_program_pid_name,_Time_to_block,mode=0):
            if mode==0:
                delete_row = self.__session.query(Block_Apps).filter(Block_Apps.program_name==_program_pid_name).first()
                self.__session.delete(delete_row)
                self.__session.commit()
            else:
                index = 0
                for program in _program_pid_name:
                    self.__session.query(Block_Apps).filter(Block_Apps.program_name==program).update({'time_to_block':_Time_to_block[index]})
                    index+=1
                self.__session.commit()
    
    # Return all the block programs in the database, or only one if specified
    def get_block_program(self,_program_name=None):
        if _program_name is None:
            programs = self.__session.query(Block_Apps.program_name,Block_Apps.time_to_block).all()
            if not programs:
                programs = None 
        else:
            programs = self.__session.query(Block_Apps).filter(Block_Apps.program_name ==_program_name).first()
        return programs


if __name__ == "__main__":
    c = Controller() 
    asdas = time(hour=0,minute=0,second=0)
    c.add_date()
    c.add_new_program(_process_id=0,_program_name="0", _usage_time=asdas,_active_time=asdas)
    programs = c.get_times_programs(ActualDate.today())
    print(programs)