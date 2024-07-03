DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS savings_plan;

CREATE TABLE user(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    email TEXT NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE savings_plan (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    plans_name TEXT NOT NULL,
    monthly_amount INTEGER NOT NULL,
    extra_deposit INTEGER,
    time_of_saving INTEGER NOT NULL,
    total_amount FLOAT NOT NULL,
    created_at DATE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id)
);