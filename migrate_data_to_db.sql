INSERT INTO domains (id, domain) values (1, 'project');
INSERT INTO domains (id, domain) values (2, 'finance');


INSERT INTO statuses (id, status, domain) VALUES (1, 'created', 1);
INSERT INTO statuses (id, status, domain) VALUES (2, 'in progress', 1);
INSERT INTO statuses (id, status, domain) VALUES (3, 'done', 1);
INSERT INTO statuses (id, status, domain) VALUES (4, 'blocked', 1);

INSERT INTO statuses (id, status, domain) VALUES (5, 'deposit', 2);
INSERT INTO statuses (id, status, domain) VALUES (6, 'withdraw', 2);
INSERT INTO statuses (id, status, domain) VALUES (7, 'transaction', 2);
