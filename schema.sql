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
  date TIMESTAMP NOT NULL,
  status INTEGER REFERENCES statuses NOT NULL
);

CREATE TABLE projects (
  id SERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  description TEXT,
  provider INTEGER REFERENCES users NOT NULL,
  client INTEGER REFERENCES users NOT NULL,
  date TIMESTAMP NOT NULL,
  amount INTEGER NOT NULL,
  payed BOOLEAN DEFAULT FALSE,
  status INTEGER REFERENCES statuses NOT NULL,
  display BOOLEAN DEFAULT TRUE
);

CREATE TABLE tasks (
  id SERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  status INTEGER REFERENCES statuses NOT NULL,
  project_id INTEGER REFERENCES projects NOT NULL
);

CREATE TABLE messages (
  id SERIAL PRIMARY KEY,
  from_user INTEGER REFERENCES users NOT NULL,
  to_user INTEGER REFERENCES users NOT NULL,
  project_id INTEGER REFERENCES projects NOT NULL,
  date TIMESTAMP NOT NULL
)