from app import app
from flask import render_template, redirect, session, request
from db import db
from services.wallet import get_amount_from_wallet, deposit_to_wallet, get_transactions, withdraw_from_wallet

@app.route("/wallet")
def wallet():
  if "user" in session:
    username = session["user"]
    fa_id_and_amount = get_amount_from_wallet(username)
    transactions = get_transactions(fa_id_and_amount["fa_id"])
    return render_template(
      "wallet.html", 
      amount=fa_id_and_amount["amount"],
      transactions=transactions,
      back_link="/profile")
  else:
    return redirect("/")

@app.route("/deposit", methods=["POST"])
def deposit():
  if "user" in session:
    amount_to_deposit = request.form["depositAmount"]
    username = session["user"]
    deposit_to_wallet(amount_to_deposit, username)
    return redirect("/wallet")
  else:
    return redirect("/")

@app.route("/withdraw", methods=["POST"])
def withdraw():
  if "user" in session:
    amount_to_withdraw = request.form["withdrawAmount"]
    username = session["user"]
    withdraw_from_wallet(amount_to_withdraw, username)
    return redirect("/wallet")
  else:
    return redirect("/")