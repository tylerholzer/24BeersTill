import sqlite3

class SqliteDB():
    def __init__(self):
        self.conn=sqlite3.connect('24beerstill.db')
        self.create_tables()

    def disconnect(self):
        self.conn.close()

    def create_tables(self):
        c = self.conn.cursor()

        c.execute(
            'CREATE TABLE IF NOT EXISTS users ( '
                'email TEXT PRIMARY KEY, '
                'pw_hash TEXT, '
                'first TEXT, '
                'last TEXT '
            ');'
        )

        c.execute(
            'CREATE TABLE IF NOT EXISTS groups ( '
                'id INTEGER PRIMARY KEY, '
                'name TEXT NOT NULL, '
                'start_date INTEGER NOT NULL, '
                'creator TEXT, '
                'FOREIGN KEY(creator) REFERENCES users(email) '
            ');'
        )

        c.execute(
            'CREATE TABLE IF NOT EXISTS group_members ( '
                'group_id INTEGER, '
                'email TEXT, '
                'has_accepted INTEGER NOT NULL CHECK(has_accepted in (0,1)), '
                'PRIMARY KEY(group_id, email), '
                'FOREIGN KEY(group_id) REFERENCES groups(id), '
                'FOREIGN KEY(email) REFERENCES users(email) '
            ');'
        )

        c.execute(
            'CREATE TABLE IF NOT EXISTS beers ( '
                'brewery TEXT NOT NULL, '
                'beer TEXT NOT NULL, '
                'group_id INTEGER NOT NULL, '
                'added_by TEXT NOT NULL, '
                'FOREIGN KEY(group_id) REFERENCES groups(id), '
                'FOREIGN KEY(added_by) REFERENCES users(email) '
            ');'
        )

        self.conn.commit()

    def get_pw_hash(self, email):
        c=self.conn.cursor()
        c.execute('SELECT pw_hash FROM users WHERE email=?', [email])
        result = c.fetchone()
        if result is not None:
            return result[0]
        return None

    def create_user(self, email, pw_hash, first, last):
        c=self.conn.cursor()
        c.execute('INSERT INTO users VALUES ( ?, ?, ?, ?)', [email, pw_hash, first, last])
        self.conn.commit()
