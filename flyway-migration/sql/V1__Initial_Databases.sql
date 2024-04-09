CREATE TABLE user_record (
    username VARCHAR(32) PRIMARY KEY,
    hashed_password TEXT NOT NULL
);