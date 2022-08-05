DROP TABLE IF EXISTS badges;

CREATE TABLE badges (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    badge TEXT,
    students TEXT);