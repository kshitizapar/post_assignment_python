import sqlite3

class DBConnection:
    def connect(self,server):
        return sqlite3.connect(server['db'])




