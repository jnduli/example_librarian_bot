DROP TABLE IF EXISTS librarians;
DROP TABLE IF EXISTS books;

CREATE TABLE librarians (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    librarian INTEGER,
    name TEST NOT NULL,
    FOREIGN KEY (librarian) REFERENCES librarians(id)
);

INSERT INTO librarians (name) VALUES ('john'), ('bonface'), ('andrew');
INSERT INTO books (librarian, name) VALUES (1, 'Sapiens'), (2, 'Homo Deus'), (3, 'The Stoic');
