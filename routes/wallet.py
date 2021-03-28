from app import app
from flask import render_template, redirect, session, request
from db import db
from services.wallet import get_amount_from_wallet

@app.route("/wallet")
def wallet():
  if "user" in session:
    username = session["user"]
    amount = get_amount_from_wallet(username)
    #transactions = get_transactions(username)
    return render_template("wallet.html", amount=amount, back_link="/profile/" + username)
  else:
    return redirect("/")

@app.route("/deposit", methods=["POST"])
def deposit():
  if "user" in session:
    username = session ["user"]
    sql = "SELECT fa.id, amount FROM users u " \
      "INNER JOIN financial_accounts fa ON u.id = fa.user_id WHERE u.username = :username"
    f_account = db.session.execute(sql, {"username": username}).fetchone()

    sql = "SELECT id FROM statuses WHERE status = 'deposit'"
    status = db.session.execute(sql).fetchone()

    amount_to_deposit = request.form["amount"]
    # update transaction ledger
    sql = "INSERT INTO transactions (from_acc, to_acc, amount, date, status) " \
      "VALUES (:from_acc, :to_acc, :amount, NOW(), :status)"
    db.session.execute(sql, {"from_acc": f_account[0], "to_acc": f_account[0], "amount": int(amount_to_deposit), "status": status[0]})
    
    # update amount of money
    sql = "UPDATE financial_accounts SET amount = :amount WHERE id = :fc_id"
    db.session.execute(sql, {"amount": f_account[1] + int(amount_to_deposit), "fc_id": f_account[0]})
    db.session.commit()
    return redirect("/wallet")
  else:
    return redirect("/")
