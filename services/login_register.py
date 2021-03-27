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
      "(:first_name, :surname, :username, :password)"
    db.session.execute(
      sql, 
      {
        "first_name": first_name,
        "surname": surname,
        "username": username,
        "password": hashed_pw
      }
    )
    db.session.commit()
    result["isRegistered"] = True
    return result
  except:
    result["isRegistered"] = False
    result["message"] = "Something went wrong during registration."
    return result

def login(username, password):
  print("Here is username and PW " + str(username) + str(password))
  result = {"logedIn": False, "message": ""}
  sql = "SELECT password FROM users WHERE username = :username"
  db_result = db.session.execute(sql, {"username": username})
  user = db_result.fetchone()

  if user == None:
    result["logedIn"] = False
    result["message"] = "Username " + str(username) + " is uknown"
    return result
  else:
    hash_value = user[0]
    if check_password_hash(hash_value, password):
      result["logedIn"] = True
      return result
    else:
      result["logedIn"] = False
      result["message"] = "Password isn't correct"
      return result