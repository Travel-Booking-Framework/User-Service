CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    nationalCode CHAR(10) UNIQUE NOT NULL,
    hashedPassword TEXT NOT NULL
);
