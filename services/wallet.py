from db import db

def get_amount_from_wallet(username):
  result = {}
  sql = "SELECT id FROM users WHERE username = :username"
  result = db.session.execute(sql, {"username": username})
  user = result.fetchone()
  sql = "SELECT amount FROM financial_accounts WHERE user_id = :user_id"
  result = db.session.execute(sql, {"user_id": user[0]})
  amount = result.fetchone()
  return amount[0]