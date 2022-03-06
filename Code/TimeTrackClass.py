from win32gui import GetForegroundWindow
import psutil
import time
import win32process


class TimeTracker:
    __active_time = {}
    __process_time = {}
    __time_stamp = {}

    def eachAppUsageTime(self,lastApp=""):
            current_app = psutil.Process(win32process.GetWindowThreadProcessId(GetForegroundWindow())[1]).name().replace(".exe", "")
            self.__time_stamp[current_app] = int(time.time())
            time.sleep(1)
            if current_app not in self.__process_time.keys():
                self.__process_time[current_app] = 0
                self.__getOpenApplications()
            if current_app not in self.__active_time.keys():
                self.__active_time[current_app] = self.__time_stamp[current_app]
            self.__process_time[current_app] = self.__process_time[current_app] + int(time.time()) - self.__time_stamp[current_app]
            print(self.__process_time,self.__process_time.__len__())
            self.eachAppUsageTime()

    def __getOpenApplications(self):
        return self.__process_time.__len__()

    #The programmer needs to find the ways to get the time for all the programs running, even when they are not in use.
    def __checkIfProcessRunning(processName):
        # Iterate over the all the running process
        for proc in psutil.process_iter():
            try:
                # Check if process name contains the given name string.
                if processName.lower() in proc.name().lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False
