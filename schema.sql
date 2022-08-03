DROP TABLE IF EXISTS posts;

CREATE TABLE badges (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    badge BLOB,
    students TEXT);