CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  first_name TEXT NOT NULL,
  surname TEXT NOT NULL,
  username TEXT NOT NULL UNIQUE,
  password TEXT NOT NULL 
);

CREATE TABLE financial_accounts (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users,
  amount INTEGER DEFAULT 0
);