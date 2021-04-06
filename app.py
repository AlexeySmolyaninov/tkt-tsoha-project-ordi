from flask import render_template, request
from flask import Flask
from os import getenv

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

import routes.login_register
import routes.profile
import routes.wallet
import routes.services