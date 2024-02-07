import pymssql
from DashLog import DashLog

class Dbconnection():
    def __init__(self):
        print("connection")

class MSSQL(Dbconnection):
    
    
    def __init__(self):
        # Connection zur authapi Datenbank
        self.authapi_config = {
            'host': 'db',
            'user': 'sa',
            'password': 'Ke123456',
            'database': 'authapi',
            'port': '1433'
        }

        # Connection zur MAV Datenbank
        self.MAV_config = {
            'host': 'host.docker.internal',
            # 'host': '127.0.0.1',
            'user': 'sa',
            'password': 'Ke123456',
            'database': 'MAV',
            'port': '1444'
        }

        self.dashlog = DashLog()

    def get_queried_data(self, dictornary, sql, params=[], db='authapi'):

        res = None
        try:

            if db == 'authapi':
                config = self.authapi_config
            elif db == 'MAV':
                config = self.MAV_config

            with pymssql.connect(**config) as conn:
                print(conn)
                with conn.cursor(as_dict=dictornary) as cursor:
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
