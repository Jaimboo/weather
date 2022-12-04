DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS favorite;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE favorite (
    code INTEGER NOT NULL,
    u_id INTEGER NOT NULL,
    FOREIGN KEY (u_id) REFERENCES user (id)
);