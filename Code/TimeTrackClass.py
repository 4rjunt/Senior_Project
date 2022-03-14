'''
Timer Track Class
Made by: Justin Nunez
Date: 3/9/2022
Description:
'''
from win32gui import GetForegroundWindow
import win32gui
import psutil
from datetime import datetime,timedelta
import time
import win32process
import threading
import multiprocessing


class TimeTracker:
    # Dictionary that contains all the applications that the user has opened over time
    __active_applications = {}  # ApplicationPid:ApplicationName
    # Dictionary that contains the active time of all the application that has been open
    __active_time = {}  # ApplicationName:ApplicationTotalTimeActive
    # Dictionary that contains the active usage time of all the application that has been open
    __active_usage_time = {}  # ApplicationName:ApplicationUsageTime
    # Dictionary that contains the present time and interact with ^ to give the active usage time of an app
    __time_stamp = {}  # ApplicationName:CurrentTime

    # Variable that store the total amount of time that the user has spent on the computer
    __computer_active_time = 0

    __today_date = 0

    # Control variable that shows the current status of the checking active programs process
    __active_checking_enable = False
    # List that contains all the pid of the applications that are being taking care of by a process
    __active_checking_applications = []

    # Constructor
    def __init__(self,active_applications={},active_time={},active_usage_time={}):
        if len(active_applications) > 0:
            #Assignt the arguments passed to the dictionary and start the function to check the active checking apps
            pass
        self.__general_stop_watch()
        self.each_app_usage_time()

    # Execute an algorithm that calculate and store the usage time of all the application that has been open or will be open
    def each_app_usage_time(self):
        # Get the name and pid of the application that the user is currently using
        current_app = psutil.Process(win32process.GetWindowThreadProcessId(GetForegroundWindow())[1]).name().replace(".exe", "")
        current_app_pid = (win32process.GetWindowThreadProcessId(GetForegroundWindow())[1])
        # Run another 2 functions at the same time
        threading.Thread(target=self.__new_program_open,args=(current_app,current_app_pid)).start()
        threading.Thread(target=self.__stop_watch, args=(current_app, current_app_pid)).start()
        if not self.__active_checking_enable:
            multiprocessing.Process(target=self.__check_programs_active,daemon=True).run()
            self.__active_checking_enable = True

    # Creates a new item in the 3 dictionaries
    def __new_program_open(self,currentApp,currentAppPid):
        if currentApp not in self.__active_applications.values():
            self.__active_applications[currentAppPid] = currentApp  # Give the pid of the program and its name
            self.__active_usage_time[currentApp] = 0  # Give the name of the program and the program usage time.
            self.__active_time[currentApp] = 0  # Give the name of the program and the program total time active

    # Calculate the usage time of the application that the user is currently using
    def __stop_watch(self,currentApp,currentAppPid):
        while currentAppPid == (win32process.GetWindowThreadProcessId(GetForegroundWindow())[1]):
            self.__time_stamp[currentApp] = int(time.time())
            time.sleep(1)
            self.__active_usage_time[currentApp] += int(time.time()) - self.__time_stamp[currentApp]
        self.each_app_usage_time()

    # Calculate the active time of the application that the user have open
    def __stop_watch2(self, active_program):
        self.__active_checking_applications.append(active_program)
        while active_program in (program.ppid() for program in psutil.process_iter()):
            current_time = int(time.time())
            time.sleep(1)
            self.__active_time[self.__active_applications[active_program]] += int(time.time()) - current_time
            print(self.__active_time)

    # Calculates the active time of the computer(The time that the computer has been used)
    def __general_stop_watch(self):
        current_time = int(time.time())
        time.sleep(1)
        self.__computer_active_time += int(time.time()) - current_time
        self.__general_stop_watch()


    # Executes an algorithm that check when a program is closed, while calculate the active time of all the programs opened
    def __check_programs_active(self):
        while True:
            for activePrograms in set(self.__active_applications)-set(self.__active_checking_applications):
                p = multiprocessing.Process(target=self.__stop_watch2(activePrograms),daemon=True)
                p.start()
                p.join()

    # Checks if the process is still running, and if its re-run the stopwatch for that specific program,
    # if its not delete it from the dictionary __active_checking_applications
    def __check_if_open(self):
        pass

    # Return the number of opened apps
    def get_open_applications(self):
        return self.__active_applications.__len__()

    # Return the entire dictionary of __active_usage_time
    def get_active_usage_time(self):
        return self.__active_usage_time

    # Return the entire dictionary of __active_time
    def get_active_time(self):
        return self.__active_time
