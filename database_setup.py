import sqlite3


class DBWrapper:

    database = None
    dbaseName = 'library.sqlite'

    def get_db(self):
        if self.database is None:
            self.database = sqlite3.connect(self.dbaseName)
        return self.database

    def init_db(self):
        with open('schema.sql', 'r', encoding='utf-8') as f:
            self.get_db().executescript(f.read())

    def select_content(self, query, params=()):
        conn = self.get_db()
        return conn.cursor().execute(query, params).fetchall()

    @property
    def librarians(self):
        query = 'SELECT * from librarians'
        return self.select_content(query)

    @property
    def books(self):
        query = 'SELECT * from books'
        return self.select_content(query)

    def get_librarian_books(self, librarian):
        query = 'SELECT * from books WHERE librarian = ?'
        return self.select_content(query, (librarian,))

    def insert_query(connection, query, params=None):
        cursor = connection.cursor()
        cursor.execute(query, params)
        connection.commit()
        cursor.close()

    def __del__(self):
        if self.database is not None:
            self.database.close()


if __name__ == '__main__':
    db = DBWrapper()
    db.init_db()
    print(db.librarians)
    print(db.books)
    print(db.get_librarian_books(1))
