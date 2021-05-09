from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from db import db

def register(first_name, surname, username, password, password2):
  result = {"isRegistered": False, "message": ""}

  if password != password2:
    result["isRegistered"] = False
    result["message"] = "Passwords are not identical"
    return result

  try:
    hashed_pw = generate_password_hash(password)
    sql = "INSERT INTO users (first_name, surname, username, password) VALUES " \
      "(:first_name, :surname, :username, :password) RETURNING id"
    result_db = db.session.execute(
      sql, 
      {
        "first_name": first_name,
        "surname": surname,
        "username": username,
        "password": hashed_pw
      }
    )
    user = result_db.fetchone()
    sql = "INSERT INTO financial_accounts (user_id, amount) VALUES (:user_id, :amount)"
    db.session.execute(sql, {"user_id": user[0], "amount": 0})
    db.session.commit()
    session["user_id"] = user[0]
    result["isRegistered"] = True
    return result
  except Exception as error:
    print(error)
    result["isRegistered"] = False
    if username in str(error):
      result["message"] = "User with username " + username + " already exists."
    else:
      result["message"] = "Something went wrong during registration"
    return result

def login(username, password):
  result = {"logedIn": False, "message": ""}
  sql = "SELECT password, id FROM users WHERE username = :username"
  db_result = db.session.execute(sql, {"username": username})
  user = db_result.fetchone()

  if user == None:
    result["logedIn"] = False
    result["message"] = "Wrong credentials"
    return result
  else:
    hash_value = user[0]
    if check_password_hash(hash_value, password):
      session["user_id"] = user[1]
      result["logedIn"] = True
      return result
    else:
      result["logedIn"] = False
      result["message"] = "Password isn't correct"
      return result