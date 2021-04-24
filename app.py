from flask import render_template, redirect, request, session, url_for
from flask import Flask
from os import getenv

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

@app.before_request
def check_auth():
  path_with_no_auth = ["/", "/register", "/register/"]
  if request.path not in path_with_no_auth:
    if "user" not in session:
      print("You must login to the service first")  
      return redirect("/")

import routes.login_register
import routes.profile
import routes.wallet
import routes.services
import routes.messages

@app.errorhandler(Exception)
def all_exception_handler(error):
  print(str(error))
  return render_template(
    "profile.html",
    message = "Error occured, please contact admin"
  )