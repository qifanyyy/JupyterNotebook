import sqlite3


class Database:
    error_message = ""

    def __init__(self):
        try:
            self.create_table()
        except Exception:
            self.error_message = "Error while creating statistics table. Maybe it already exists or you cannot connect to database"
            print(self.error_message)

    @staticmethod
    def create_table():
        conn = sqlite3.connect('database.db')
        conn.execute('CREATE TABLE statistics (sta_id INTEGER PRIMARY KEY, sta_size INTEGER, sta_time FLOAT, sta_nb_mult INTEGER, sta_strassen BIT)')
        conn.close()

    def reset_table(self):
        conn = sqlite3.connect('database.db')
        conn.execute('DROP TABLE statistics')
        conn.close()
        self.create_table()

    def add_record(self, size, time, nb_mult, strassen):
        try:
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO statistics (sta_size, sta_time, sta_nb_mult, sta_strassen) VALUES(?, ?, ?, ?)"
                            , (size, time, nb_mult, strassen))
                con.commit()
                print("Inserting record", size, time, nb_mult, strassen)
        except Exception:
            con.rollback()
            self.error_message = "Error while inserting record"
            print(self.error_message)

    @staticmethod
    def list_strassen_stats():
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row

        cur = conn.cursor()
        cur.execute("select * from statistics where sta_strassen = 1 order by cast(sta_size as INTEGER)")

        strassen_rows = cur.fetchall()

        return strassen_rows

    @staticmethod
    def list_classical_stats():
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row

        cur = conn.cursor()
        cur.execute("select * from statistics where sta_strassen = 0 order by cast(sta_size as INTEGER)")

        classical_rows = cur.fetchall()

        return classical_rows

    @staticmethod
    def init_connection():
        return sqlite3.connect('database.db')
