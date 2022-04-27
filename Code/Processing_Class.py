'''
Processing Class
Made by: Justin Nunez
Date: 12/9/2021
Description: Script contains 2 algorithms, one count usage time of the computer, and its programs
the other one communicates with the windows registry and block programs ask by the user 
'''
from Controller import *
from win32gui import GetForegroundWindow
import psutil
from datetime import timedelta,date,datetime
import time
import win32process
import threading
import multiprocessing
import winreg as wreg 

# Communication with the database
database_controller = Controller()

class TimeTracker:
    # Dictionary that contains all the applications that the user has opened over time
    active_applications = None  # ApplicationPid:ApplicationName
    # Dictionary that contains the active time of all the application that has been openF
    active_time = None  # ApplicationName:ApplicationTotalTimeActive
    # Dictionary that contains the active usage time of all the application that has been open
    active_usage_time = None  # ApplicationName:ApplicationUsageTime

    # Variable that store the total amount of time that the user has spent on the computer
    computer_active_time = timedelta(hours=0,minutes=0,seconds=0)

    __initial_date = date.today()

    # Control variable that shows the current status of the checking active programs process
    __active_checking_enable = False
    # List that contains all the pid of the applications that are being taking care of by a process
    __active_checking_applications = []
    # List that contains names of applications that should not be used by the class
    __not_usable_applications = database_controller.update_not_usable_applications(mode=1) 

    # Initialize the object, and populates the dictionaries with the databases info 
    def __init__(self,manager):
        self.active_applications = manager.dict()
        self.active_usage_time = manager.dict()
        self.active_time = manager.dict()
        dates = database_controller.get_dates(_date=date.today())
        if dates != None:
            self.computer_active_time = dates.computer_usage_time
            programs = database_controller.get_times_programs(date.today())
            for program in programs:
                self.active_applications[program.process_id] = program.program_name
                self.active_time[program.program_name]=program.active_time
                self.active_usage_time[program.program_name]=program.usage_time
        else:
            database_controller.add_date(_date=date.today())
        threading.Thread(target=self.__general_stop_watch,daemon=True).start()
        threading.Thread(target=self.__datetime_today,daemon=True).start()
        self.each_app_usage_time()

    # Execute an algorithm that calculate and store the usage time of all the application that has been open or will be open
    def each_app_usage_time(self):
        while True:
            try:
        # Get the name and pid of the application that the user is currently using
                current_app = psutil.Process(win32process.GetWindowThreadProcessId(GetForegroundWindow())[1]).name().replace(".exe", "")
                current_app_pid = (win32process.GetWindowThreadProcessId(GetForegroundWindow())[1])
                if current_app not in self.__not_usable_applications:
                    break
            except:
                pass
        if current_app_pid in self.active_applications:
            threading.Thread(target=self.__stop_watch, args=(current_app, current_app_pid)).start()
        else:
            threading.Thread(target=self.__new_program_open,args=(current_app,current_app_pid)).start()
        if not self.__active_checking_enable:
            self.__active_checking_enable = True
            multiprocessing.Process(target=self._check_programs_active,args=()).start()
            multiprocessing.Process(target=self._periodically_save,args=()).start()

    # Creates a new item in the 3 dictionaries
    def __new_program_open(self,currentApp,currentAppPid):
        if currentApp not in self.active_applications.values():
            database_controller.add_new_program(_process_id=currentAppPid,_program_name=currentApp,_usage_time=timedelta(hours=0,minutes=0,seconds=0),_active_time=timedelta(hours=0,minutes=0,seconds=0))
            self.active_applications[currentAppPid] = currentApp
            self.active_usage_time[currentApp] = timedelta(hours=0,minutes=0,seconds=0)
            self.active_time[currentApp] = timedelta(hours=0,minutes=0,seconds=0)
            self.__stop_watch(_currentApp=currentApp,_currentAppPid=currentAppPid)

    # Calculate the usage time of the application that the user is currently using
    def __stop_watch(self,_currentApp,_currentAppPid):
        while _currentAppPid == (win32process.GetWindowThreadProcessId(GetForegroundWindow())[1]):
            _time = datetime.now()
            current_time = timedelta(hours=_time.hour,minutes=_time.minute,seconds=_time.second)
            time.sleep(1)
            _time = datetime.now()
            self.active_usage_time[_currentApp] = self.active_usage_time[_currentApp] + timedelta(hours=_time.hour,minutes=_time.minute,seconds=_time.second) - current_time
        self.each_app_usage_time()

    # Calculate the active time of the application that the user have open
    def _stop_watch2(self, active_program,active_program_pid):
        while True:
            try:
                _time = datetime.now()
                current_time = timedelta(hours=_time.hour,minutes=_time.minute,seconds=_time.second)
                if active_program_pid not in (program.ppid() for program in psutil.process_iter()):
                    break
                _time = datetime.now()
                self.active_time[active_program]= self.active_time[active_program] + timedelta(hours=_time.hour,minutes=_time.minute,seconds=_time.second) - current_time
            except:
                pass
        self.__check_if_open_again(active_program,active_program_pid)

    # Calculates the active time of the computer(The time that the computer has been used)
    def __general_stop_watch(self):
        while True:
            _time = datetime.now()
            current_time = timedelta(hours=_time.hour,minutes=_time.minute,seconds=_time.second)
            time.sleep(1)
            _time = datetime.now()
            self.computer_active_time += timedelta(hours=_time.hour,minutes=_time.minute,seconds=_time.second) - current_time

    # Executes an algorithm that check when a program is closed, while calculate the active time of all the programs opened
    def _check_programs_active(self):
        while True:
                for activePrograms in (set(self.active_applications.keys())-set(self.__active_checking_applications)):
                    self.__active_checking_applications.append(activePrograms)
                    multiprocessing.Process(target=self._stop_watch2,args=(self.active_applications[activePrograms],activePrograms),daemon=True).start()                
                time.sleep(1)

    # Checks if the process is running again, and if its re-run the stopwatch for that specific program
    def __check_if_open_again(self,program_to_check,pid_program_to_check):
        while True:
            if program_to_check in (program.ppid() for program in psutil.process_iter()):
                self._stop_watch2(program_to_check,pid_program_to_check)
                break
            time.sleep(2)

    # Check if the date change, saves all the data and restart the stop_watch
    def __datetime_today(self):
        while True:
            self.__today_date = date.today()
            if self.__today_date != self.__initial_date:
                database_controller.update_programs_time(process_id_name=self.active_applications,
                _Usage_time=self.active_usage_time,_Active_time=self.active_time,_Date=self.__initial_date)
                database_controller.update_dates(self.__initial_date,self.computer_active_time)
                self.__initial_date = self.__today_date
                database_controller.add_date(_date=self.__initial_date)
                self.active_applications.clear()
                self.active_usage_time.clear()
                self.active_time.clear()
                self.computer_active_time = timedelta(hours=0,minutes=0,seconds=0)
            time.sleep(1)

    # Periodically save all the times of the programs and the usage of the computer
    def _periodically_save(self):
        while True:
            time.sleep(300)
            database_controller.update_programs_time(process_id_name=self.active_applications,
                 _Usage_time=self.active_usage_time,_Active_time=self.active_time,_Date=self.__initial_date)
            database_controller.update_dates(self.__initial_date,self.computer_active_time)

    # Let add records to the txt File, Add applications that are not usable by the user, but appear on use 
    def add_not_usable_application(self,not_usable_app):
        self.__not_usable_applications.append(not_usable_app)
        database_controller(not_usable_application=self.__not_usable_applications)

class Block_Apps:
    # Dictionary that contains all the applications that are actually blocked
    programs_block = {} #ApplicationName:BlockedTime

    # Populates the dictionary with the info of the database
    def __init__(self):
        blocked_programs = database_controller.get_block_program()
        if blocked_programs is not None:
            for program in blocked_programs:
                self.programs_block[program.program_name] = program.time_to_block

    # Block a program, add it to the data base and if the user enter a time ot block executes a timer
    def block_program(self,program_name,_time=None):
        if program_name not in self.programs_block.keys():
            index=0
            for program in self.programs_block:
                index+=1 
                if program == program_name:
                    break
            if index == 0:
                index = 1
            try:
                key = wreg.CreateKey(wreg.HKEY_CURRENT_USER, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer")
                wreg.SetValueEx(key, 'DisallowRun',0, wreg.REG_DWORD, 0x00000001)
                _key = wreg.CreateKey(key,'DisallowRun')
                wreg.SetValueEx(_key, str(index),0, wreg.REG_SZ, f"{program_name}.exe")
                _key.Close()
                key.Close()
                os.system(f"taskkill /f /im {program_name}.exe")
                database_controller.add_block_program(program_name,_time)
            except:
               pass 
            if _time is not None:
                threading.Thread(target=self.program_block_timer,args=(program_name,_time),daemon=True).start()
            self.programs_block[program_name]=_time
            return None
        else:
            return "That program is already blocked"

    # Calculates the remaining time of a blocked program to be unlock
    def program_block_timer(self,_program_name,time_to_block):
        while time_to_block > timedelta(hours=0,minutes=0,seconds=0):
            time.sleep(1)
            time_to_block -= timedelta(hours=0,minutes=0,seconds=1)
        self.unblock_program(_program_name)
    
    # Unlock a program and delete it from the database
    def unblock_program(self,program_name):
        try:
            key = wreg.CreateKey(wreg.HKEY_CURRENT_USER, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer")
            wreg.SetValueEx(key, 'DisallowRun',0, wreg.REG_DWORD, 0x00000001)
            _key = wreg.CreateKey(key,'DisallowRun')
            wreg.DeleteValue(_key, "1")
            _key.Close()
            key.Close()
            os.system(f"taskkill /f /im {program_name}.exe")
            database_controller.update_block_programs(_program_pid_name=program_name,_Time_to_block=None,mode=0)
        except:
            pass

    # Periodically update all the block programs of the database  
    def _periodically_save(self):
        while True:
            time.sleep(300)
            database_controller.update_block_programs(self.programs_block.keys(),self.programs_block.values())

if __name__ == "__main__":
    manager = multiprocessing.Manager()
    timeTracker = TimeTracker(manager)
    while True:
        print(timeTracker.active_usage_time.values(),timeTracker.active_time.values())
        time.sleep(.5)