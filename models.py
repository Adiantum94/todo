from cProfile import run
from socket import create_connection
import sqlite3
from sqlite3 import Error


class Todos:
    def create_connection(self):
        db_file='database.db'
        conn = sqlite3.connect(db_file)
        conn.row_factory = sqlite3.Row
        return conn

    def create_table(self,conn):
        conn.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id	integer PRIMARY KEY,
                    title text NOT NULL,
                    description text,
                    done text
                    );
                """)
        
    def all(self, conn):
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM tasks")
        rows = cur.fetchall()
        return rows

    def get(self, id, conn):
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM tasks WHERE id=?", (id,))
        row = cur.fetchone()
        return row

    def create(self, data, conn):
        cur = conn.cursor()
        if 'csrf_token' in data:
            data.pop('csrf_token')
        sql = '''INSERT INTO tasks(title, description, done)
                VALUES(?,?,?)'''
        values = tuple(data.values())
        cur.execute(sql, values)
        conn.commit()

    def update(self, id, data, conn):
        cur = conn.cursor()
        if 'csrf_token' in data:
            data.pop('csrf_token')
        parameters = [f"{k} = ?" for k in data]
        parameters = ", ".join(parameters)
        values = tuple(v for v in data.values())
        values += (id,)
        sql = f''' UPDATE tasks
                                SET {parameters}
                                WHERE id = ?'''
        try:
            cur.execute(sql, values)
            conn.commit()
        except sqlite3.OperationalError as e:
            print(e)

todos = Todos()