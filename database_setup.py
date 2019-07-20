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
        query = 'SELECT name from librarians'
        return self.select_content(query)

    @property
    def books(self):
        query = 'SELECT books.name, librarians.name from books INNER JOIN librarians ON books.librarian=librarians.id'
        return self.select_content(query)

    def get_librarian_books(self, librarian):
        query = 'SELECT books.name from books INNER JOIN librarians ON books.librarian=librarians.id WHERE librarians.name = ?'
        books = self.select_content(query, (librarian,))
        return [book[0] for book in books]

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
    print('Getting librarian books')
    print(db.get_librarian_books('john'))
    books = db.get_librarian_books('john')
    print(','.join(books))
    reply_keyboard = [['Librarians', 'Books']]
    print(reply_keyboard)
    bd = db.librarians
    sth = [[ b[0] for b in bd]]
    print(sth)
