import pymssql
from DashLog import DashLog

class Dbconnection():
    def __init__(self):
        print("connection")

class MSSQL(Dbconnection):
    
    
    def __init__(self):
        self.ip = 'db'
        self.pw = 'Ke123456'
        self.db = 'test'
        self.user = 'sa'
        self.port = '1433'  # Standardmäßig verwendet MSSQL den Port 1433
        self.dashlog = DashLog()

    def get_queried_data(self, as_dict, sql, params=[]):
        res = None
        try:
            with pymssql.connect(host=self.ip, user=self.user, password=self.pw, database=self.db, port=self.port) as conn:
                with conn.cursor(as_dict=as_dict) as cursor:
                    cursor.execute(sql, params)
                    res = cursor.fetchall()
        except pymssql.Error as err:
            res = False
            self.dashlog.send_log(2,f"Die Abfrage konnte nicht ausgeführt werden: {err}")
            print(f"Die Abfrage konnte nicht ausgeführt werden: {err}")

        return res

    def modify_queried_data(self,as_dict ,sql , params=[]):
        res = None
        try:
            with pymssql.connect(host=self.ip, user=self.user, password=self.pw, database=self.db, port=self.port) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, params)
                    res = cursor.lastrowid or True
                    conn.commit()
        except pymssql.Error as err:
            res = False
            self.dashlog.send_log(2,f"Die Abfrage konnte nicht ausgeführt werden: {err}")
            print(f"Die Abfrage konnte nicht ausgeführt werden: {err}")

        return res
