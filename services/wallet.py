from db import db
from flask import session

def get_amount_from_wallet(username):
  sql = "SELECT fa.id, fa.amount FROM financial_accounts fa " \
     "INNER JOIN users u ON fa.user_id = u.id WHERE u.username = :username"
  financial_account = db.session.execute(sql, {"username": username}).fetchone()
  return {"fa_id": financial_account[0], "amount": financial_account[1]}

def get_transactions(fa_id):
  sql = "SELECT from_acc, to_acc, status, date, amount FROM transactions " \
    "WHERE from_acc = :fa_id OR to_acc = :fa_id " \
    "ORDER BY date DESC"
  transactions = db.session.execute(sql, {"fa_id": fa_id}).fetchall()
  return transactions


def deposit_to_wallet(amount_to_deposit, username):
  sql = "SELECT fa.id, amount FROM users u " \
    "INNER JOIN financial_accounts fa ON u.id = fa.user_id WHERE u.username = :username"
  f_account = db.session.execute(sql, {"username": username}).fetchone()

  sql = "SELECT id FROM statuses WHERE status = 'deposit'"
  status = db.session.execute(sql).fetchone()

  # update transaction ledger
  sql = "INSERT INTO transactions (from_acc, to_acc, amount, date, status) " \
    "VALUES (:from_acc, :to_acc, :amount, NOW(), :status)"
  db.session.execute(sql, {"from_acc": f_account[0], "to_acc": f_account[0], "amount": int(amount_to_deposit), "status": status[0]})
  
  # update amount of money
  sql = "UPDATE financial_accounts SET amount = :amount WHERE id = :fc_id"
  db.session.execute(sql, {"amount": f_account[1] + int(amount_to_deposit), "fc_id": f_account[0]})
  db.session.commit()
  return

def withdraw_from_wallet(amount_to_withdraw, username):
  sql = "SELECT fa.id, amount FROM users u " \
    "INNER JOIN financial_accounts fa ON u.id = fa.user_id WHERE u.username = :username"
  f_account = db.session.execute(sql, {"username": username}).fetchone()

  sql = "SELECT id FROM statuses WHERE status = 'withdraw'"
  status = db.session.execute(sql).fetchone()

  # update transaction ledger
  sql = "INSERT INTO transactions (from_acc, to_acc, amount, date, status) " \
    "VALUES (:from_acc, :to_acc, :amount, NOW(), :status)"
  db.session.execute(sql, {"from_acc": f_account[0], "to_acc": f_account[0], "amount": int(amount_to_withdraw), "status": status[0]})
  
  # update amount of money
  sql = "UPDATE financial_accounts SET amount = :amount WHERE id = :fc_id"
  db.session.execute(sql, {"amount": f_account[1] - int(amount_to_withdraw), "fc_id": f_account[0]})
  db.session.commit()
  return