from importlib.metadata import SelectableGroups
from sqlalchemy import create_engine, engine, update
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from Models import Usage_Date, Usage_Time, Block_Apps
from sqlite3 import ProgrammingError
from datetime import date as ActualDate


class Controller:
    def __init__(self) -> None:
        engine = create_engine(
            'sqlite:///C:\\Users\\Desktop\\Desktop\\SQLite\\database\\test.db'
        )
        Session = sessionmaker(bind=engine)
        self.__session = Session()

    def add_date(self):
        date = self.session.query(Usage_Date).filter(Usage_Date.date == ActualDate.today()).first()
        if date is None:
            today_date = ActualDate.today
            new_date = Usage_Date(date=today_date)
            self.__session.add(new_date)
            self.__session.commit()
        else:
            raise ProgrammingError("Date already exists")

    def get_dates(self,_date=None):
        if _date is None:
            return Usage_Date.date
        else:
            dates = self.__session.query(Usage_Date).filter(Usage_Date.date==_date).first()
            return dates
    
    def add_new_program(self,_process_id,_program_name,_usage_time,_active_time):
        program = Usage_Time(process_id=_process_id,
                           program_name=_program_name, usage_time = _usage_time,
                           active_time=_active_time)

        self.__session.add(program)
        self.__session.commit()

    def add_block_program(self,_program_pid,_program_name,_time_to_block):
        program_to_block = Block_Apps(program_pid=_program_pid,program_name=_program_name,time_to_block=_time_to_block)
        self.__session.add(program_to_block)
        self.__session.commit()

    def update_programs_time(self):
        #update(Usage_Time).where
        pass

if __name__ == "__main__":
    c = Controller()
