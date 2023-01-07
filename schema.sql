DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS favorite;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE favorite (
    city TEXT NOT NULL,
    u_id INTEGER NOT NULL,
    UNIQUE(city, u_id),
    FOREIGN KEY (u_id) REFERENCES user (id)
);