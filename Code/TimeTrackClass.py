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


class TimeTracker:
    # Dictionary that contains all the applications that the user has opened over time
    # __active_applications[ApplicationPid] = ApplicationPid:ApplicationName
    __active_applications = {}
    # Dictionary that contains the active time of all the application that has been open
    # __active_time[ApplicationName] = ApplicationName:ApplicationTotalTimeActive
    __active_time = {}
    # Dictionary that contains the active usage time of all the application that has been open
    # __active_usage_time[ApplicationName] = ApplicationName:ApplicationUsageTime
    __active_usage_time = {}
    # Dictionary that contains the present time and interact with ^ to give the active usage time of an app
    # __time_stamp[ApplicationName] = ApplicationName:CurrentTime
    __time_stamp = {}

    __active_checking_enable = False
    __active_checking_applications = []

    # Execute an algorithm that calculate and store the usage time of all the application that has been open or will be open
    def each_app_usage_time(self):
        # Get the name and pid of the application that the user is currently using
        current_app = psutil.Process(win32process.GetWindowThreadProcessId(GetForegroundWindow())[1]).name().replace(".exe", "")
        current_app_pid = (win32process.GetWindowThreadProcessId(GetForegroundWindow())[1])
        # Run another 2 functions at the same time
        threading.Thread(target=self.__new_program_open,args=(current_app,current_app_pid)).start()
        threading.Thread(target=self.__stop_watch, args=(current_app, current_app_pid)).start()
        if not self.__active_checking_enable:
            self.__check_programs_active()
            self.__active_checking_enable = True

    # Creates a new item in the 3 dictionaries, the first dictionary contain the name of the program and its pid
    # The second one contain the name of the program and the program total time active,
    # And the third one contain the name of the program and the program usage time.
    def __new_program_open(self,currentApp,currentAppPid):
        if currentApp not in self.__active_applications.values():
            self.__active_usage_time[currentApp] = 0
            self.__active_applications[currentAppPid] = currentApp
            self.__active_time[currentApp] = timedelta(0,0,0)

    # Calculate the usage time of the application that the user is currently using
    def __stop_watch(self,currentApp,currentAppPid):
        while currentAppPid == (win32process.GetWindowThreadProcessId(GetForegroundWindow())[1]):
            self.__time_stamp[currentApp] = int(time.time())
            time.sleep(1)
            self.__active_usage_time[currentApp] = self.__active_usage_time[currentApp] + int(time.time()) - \
                                                  self.__time_stamp[currentApp]
            print(self.__active_usage_time)
        self.each_app_usage_time()


    # Executes an algorithm that check when a program is closed, while calculate the active time of all the programs opened
    def __check_programs_active(self):
        for activePrograms in set(self.__active_applications)-set(self.__active_checking_applications):
            threading.Thread(target=self.__stop_watch2,args=[activePrograms]).start()
            self.__check_programs_active()

    # Calculate the active time of the application that the user have open
    def __stop_watch2(self,active_program):
        self.__active_checking_applications.append(active_program)
        while active_program in (program.ppid() for program in psutil.process_iter()):
            current_time = datetime.now()
            time.sleep(1)
            self.__active_time[self.__active_applications[active_program]] = \
                self.__active_time[self.__active_applications[active_program]]+datetime.now()-current_time
            #print(self.__active_time)

    # Return the number of opened apps
    def get_open_applications(self):
        return self.__active_applications.__len__()

    # Return the entire dictionary of __active_usage_time
    def get_active_usage_time(self):
        return self.__active_usage_time

    # Return the entire dictionary of __active_time
    def get_active_time(self):
        return self.__active_time
