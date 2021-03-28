from app import app
from flask import render_template, redirect, session
from db import db
from services.wallet import get_amount_from_wallet

@app.route("/wallet")
def wallet():
  if "user" in session:
    username = session["user"]
    amount = get_amount_from_wallet(username)
    return render_template("wallet.html", amount=amount, back_link="/profile/" + username)
  else:
    return redirect("/")