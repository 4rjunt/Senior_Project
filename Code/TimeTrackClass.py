from win32gui import GetForegroundWindow
import win32gui
import psutil
from datetime import datetime,timedelta
import time
import win32process
import threading


class TimeTracker:
    # Dictionary that contains all the applications that the user has opened over time
    __active_applications = {}
    # Dictionary that contains the active time of all the application that has been open
    __active_time = {}
    # Dictionary that contains the active usage time of all the application that has been open
    __active_usage_time = {}
    # Dictionary that contains the present time and interact with ^ to give the active usage time of an app
    __time_stamp = {}

    def each_app_usage_time(self):
        # Get the name of the application that the user is currently using
        current_app = psutil.Process(win32process.GetWindowThreadProcessId(GetForegroundWindow())[1]).name().replace(".exe", "")
        # Get the pid of the application that the user is currently using
        current_app_pid = (win32process.GetWindowThreadProcessId(GetForegroundWindow())[1])
        # Run another functions at the same time
        threading.Thread(target=self.__new_program_open,args=(current_app,current_app_pid)).start()
        threading.Thread(target=self.__stop_watch, args=(current_app, current_app_pid)).start()

        # This will be running all the time in the background, so it doesn't matter that doesn't run now
        #self.__check_programs_active()

    def __new_program_open(self,currentApp,currentAppPid):
        if currentApp not in self.__active_applications.values():
            self.__active_usage_time[currentApp] = 0
            self.__active_applications[currentAppPid] = currentApp
            self.__active_time[currentApp] = (time.time())
            self.__get_open_applications()

    def __check_programs_active(self):
        for activePrograms in self.__active_applications:
            if activePrograms not in (program.ppid() for program in psutil.process_iter()):
                print(str(self.__active_applications[activePrograms]) + " has been closed")

    def __stop_watch(self,currentApp,currentAppPid):
        while currentAppPid == (win32process.GetWindowThreadProcessId(GetForegroundWindow())[1]):
            self.__time_stamp[currentApp] = int(time.time())
            time.sleep(1)
            self.__active_usage_time[currentApp] = self.__active_usage_time[currentApp] + int(time.time()) - \
                                                    self.__time_stamp[currentApp]
            print(self.__active_usage_time)
        self.each_app_usage_time()

    def __get_open_applications(self):
        return self.__active_applications.__len__()
