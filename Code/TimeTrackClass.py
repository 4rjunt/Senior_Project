'''
Timer Track Class
Made by: Justin Nunez
Date: 3/9/2022
Description:
'''
import multiprocessing

from win32gui import GetForegroundWindow
import win32gui
import psutil
from datetime import datetime,timedelta
import time
import win32process
import threading
from multiprocessing import Process, Value, Array


class TimeTracker:
    # Dictionary that contains all the applications that the user has opened over time
    __active_applications = {}  # ApplicationPid:ApplicationName
    # Dictionary that contains the active time of all the application that has been open
    __active_time = {}  # ApplicationName:ApplicationTotalTimeActive
    __active_time_shared = Array('i',10)
    __index = Value('i',0)
    # Dictionary that contains the active usage time of all the application that has been open
    __active_usage_time = {}  # ApplicationName:ApplicationUsageTime
    # Dictionary that contains the present time and interact with ^ to give the active usage time of an app
    __time_stamp = {}  # ApplicationName:CurrentTime

    # Variable that store the total amount of time that the user has spent on the computer
    __computer_active_time = 0

    today_date = 0

    # Control variable that shows the current status of the checking active programs process
    __active_checking_enable = False
    # List that contains all the pid of the applications that are being taking care of by a process
    __active_checking_applications = []

    def __init__(self,active_applications={},active_time={},active_usage_time={}):
        #if len(active_applications) > 0:
            #Assignt the arguments passed to the dictionary and start the function to check the active checking apps
        asd = 2
        threading.Thread(target=self.__general_stop_watch,daemon=True).start()
        threading.Thread(target=self.__datetime_today,daemon=True).start()
        self.each_app_usage_time()

    # Execute an algorithm that calculate and store the usage time of all the application that has been open or will be open
    def each_app_usage_time(self):
        # Get the name and pid of the application that the user is currently using
        current_app = psutil.Process(win32process.GetWindowThreadProcessId(GetForegroundWindow())[1]).name().replace(".exe", "")
        current_app_pid = (win32process.GetWindowThreadProcessId(GetForegroundWindow())[1])
        threading.Thread(target=self.__new_program_open,args=(current_app,current_app_pid)).start()
        threading.Thread(target=self.__stop_watch, args=(current_app, current_app_pid)).start()
        if not self.__active_checking_enable:
            Process(target=self.__check_programs_active(),daemon=True).start()
            self.__active_checking_enable = True

    # Creates a new item in the 3 dictionaries
    def __new_program_open(self,currentApp,currentAppPid):
        if currentApp not in self.__active_applications.values():
            self.__active_applications[currentAppPid] = currentApp
            self.__active_usage_time[currentApp] = 0
            self.__active_time[currentApp] = 0
            self.__active_time_shared[self.get_open_applications()]=0

    # Calculate the usage time of the application that the user is currently using
    def __stop_watch(self,currentApp,currentAppPid):
        while currentAppPid == (win32process.GetWindowThreadProcessId(GetForegroundWindow())[1]):
            self.__time_stamp[currentApp] = int(time.time())
            time.sleep(1)
            self.__active_usage_time[currentApp] = self.__active_usage_time[currentApp] + int(time.time()) - self.__time_stamp[currentApp]
        self.each_app_usage_time()

    # Calculate the active time of the application that the user have open
    def __stop_watch2(self, active_program,index=0):
        if index == 0:
            index = self.__index.value
            self.__index.value += 1
        while True:
            current_time = int(time.time())
            time.sleep(.3)
            if active_program in (program.ppid() for program in psutil.process_iter()):
                self.__active_time_shared[index]+= int(time.time()) - current_time
                # Se necesitan sincronizar todas los procesos activos para que en el cambio de tiempo sea el mismo
                # Y se necesita encontrar una manera de crear una funcion que pase todos los valores del array al diccionario
            else:
                break
            print(self.__active_time_shared[:])
        self.__check_if_open_again(active_program,index)
        return

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
                self.__active_checking_applications.append(activePrograms)
                p = Process(target=self.__stop_watch2(activePrograms),daemon=True)
                p.start()
                p.join()

    def __print_all(self):
        while True:
            pass

    # Checks if the process is running again, and if its re-run the stopwatch for that specific program
    def __check_if_open_again(self,program_to_check,index_of_program):
        while True:
            if program_to_check in (program.ppid() for program in psutil.process_iter()):
                self.__stop_watch2(program_to_check,index_of_program)
                return
            time.sleep(1)

    def __datetime_today(self):
        while True:
            self.today_date = datetime.today()
            # Mientras esta funcion corre, otra funcion debe ser la responsable de checar si la fecha cambio
            # Todos los tiempos de uso incluidos el tiempo actual deben ser guardados para cuando el progranma se cierre

    def get_open_applications(self):
        return int(self.__active_applications.__len__())

    def get_active_usage_time(self):
        return self.__active_usage_time

    def get_active_time(self):
        return self.__active_time
