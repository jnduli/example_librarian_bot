DROP TABLE IF EXISTS librarians;
DROP TABLE IF EXISTS books;

CREATE TABLE librarians (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    librarian INTEGER,
    name TEXT NOT NULL,
    FOREIGN KEY (librarian) REFERENCES librarians(id)
);

INSERT INTO librarians (name) VALUES ('john'), ('bonface'), ('andrew');
INSERT INTO books (librarian, name) VALUES (1, 'Sapiens'), (1, 'Courage To Be Disliked'), (1, 'Percy Jackson'), (2, 'Homo Deus'), (2, 'The Bible'), (3, 'The Stoic'), (3, 'Game of Thrones'), (3, 'Harry Potter'), (3, 'Play Things');
