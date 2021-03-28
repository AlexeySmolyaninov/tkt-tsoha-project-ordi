CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  first_name TEXT NOT NULL,
  surname TEXT NOT NULL,
  username TEXT NOT NULL UNIQUE,
  password TEXT NOT NULL 
);

CREATE TABLE financial_accounts (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users NOT NULL,
  amount INTEGER DEFAULT 0
);

CREATE TABLE domains (
  id SERIAL PRIMARY KEY,
  domain TEXT NOT NULL
);

CREATE TABLE statuses (
  id SERIAL PRIMARY KEY,
  status TEXT NOT NULL,
  domain INTEGER REFERENCES domains NOT NULL
);

CREATE TABLE transactions (
  id SERIAL PRIMARY KEY,
  from_acc INTEGER REFERENCES financial_accounts NOT NULL,
  to_acc INTEGER REFERENCES financial_accounts NOT NULL,
  amount INTEGER NOT NULL,
  date TIMESTAMP,
  status INTEGER REFERENCES statuses NOT NULL
);