import sqlite3
import sqlite3 as sql

class StorageDataBase:
    __conn = None
    __cursor = None

    def __init__(self):
        self.__conn = sql.connect(":memory:")
        self.__conn.commit()
        self.__cursor = self.__conn.cursor()
        with self.__conn:
            self.__cursor.execute("""CREATE TABLE appsusagetime (
                                        pid integer,
                                        name text,
                                        usagetime integer,
                                        activetime integer
                                        )""")
        self.__check_persistent_database()


    def __check_persistent_database(self):
        try:
            persistent_conn = sql.connect('file:timetrackdatabase.db?mode=rw',uri=True)
            persistent_cursor = persistent_conn.cursor()
            datos = []
            with persistent_conn:
                   persistent_cursor.execute("SELECT * FROM appsusagetime;")
                   datos = persistent_cursor.fetchall()
            persistent_conn.close
            self.__initialize_app_usage_time(datos)
        except sqlite3.OperationalError:
            self.__create_persistent_datebase()


    def __create_persistent_datebase(self):
        persistent_conn = sql.connect('timetrackdatabase.db')
        persistent_cursor = persistent_conn.cursor()
        with persistent_conn:
            persistent_cursor.execute("""CREATE TABLE appsusagetime (
                                                    pid integer,
                                                    name text,
                                                    usagetime integer,
                                                    activetime integer
                                                    )""")
        persistent_conn.close()

    def save_in_persistent(self):
        datos = None
        with self.__conn:
            self.__cursor.execute("SELECT * FROM appsusagetime;")
            datos = self.__cursor.fetchall()
        persistent_conn = sql.connect('timetrackdatabase.db')
        persistent_cursor = persistent_conn.cursor()
        with persistent_conn:
            persistent_cursor.executemany("INSERT INTO appsusagetime VALUES (?,?,?,?)",datos)
        persistent_conn.close()

    def __initialize_app_usage_time(self,list_to_enter):
        with self.__conn:
                self.__cursor.executemany("INSERT INTO appsusagetime VALUES (?,?,?,?)",list_to_enter)

    def update_app_usage_time(self,list_to_update):
        with self.__conn:
            self.__cursor.execute("UPDATE appsusagetime SET usagetime=? WHERE pid like ?",list_to_update)

    def insert_row(self,pid,name,usagetime,activetime):
        i = f"INSERT INTO appsusagetime VALUES ({pid},'{name}',{usagetime},{activetime})"
        with self.__conn:
            self.__cursor.execute(i)

    def print_persistent(self):
        persistent_conn = sql.connect('timetrackdatabase.db')
        persistent_cursor = persistent_conn.cursor()
        with persistent_conn:
            persistent_cursor.execute("SELECT * FROM appsusagetime;")
            datos = persistent_cursor.fetchall()
            print(datos)
        persistent_conn.close()


if __name__ == "__main__":
    a = StorageDataBase()
    #a.print_persistent()
    #a.insert_row(1,"programa1",10,20)
    #a.save_in_persistent()
