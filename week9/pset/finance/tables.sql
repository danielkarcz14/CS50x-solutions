DROP TABLE users;
DROP TABLE portfolio;
DROP TABLE transactions;



CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL, cash NUMERIC NOT NULL DEFAULT 10000.00);
CREATE UNIQUE INDEX username ON users (username);
CREATE TABLE IF NOT EXISTS "portfolio" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "symbol" TEXT NOT NULL,
    "quantity" NUMERIC NOT NULL,
    "share_price" NUMERIC NOT NULL,
    "total_price" NUMERIC NOT NULL,
    "time" DATETIME,
    "user_id" INTEGER,
    FOREIGN KEY("user_id") REFERENCES "users"("id")
    );
CREATE TABLE transactions (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "symbol" TEXT NOT NULL,
    "quantity" NUMERIC NOT NULL,
    "share_price" NUMERIC NOT NULL,
    "time" DATETIME,
    "user_id" INTEGER,
    FOREIGN KEY("user_id") REFERENCES "users"("id")
    );
