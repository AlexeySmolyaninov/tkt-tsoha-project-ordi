from app import app
from flask import request, session
from services.services import username_to_userid
from services.message import send_message

@app.route("/messageByClient", methods=["POST"])
def message_by_client():
  data = request.json
  message = data["msg"]
  provider_id = username_to_userid(data["providerUsername"])
  client_id = session["user_id"]
  project_id = data["projectId"]
  message = send_message(message, client_id, provider_id, project_id)
  return message

@app.route("/messageByProvider", methods=["POST"])
def message_by_provider():
  data = request.json
  message = data["msg"]
  client_id = username_to_userid(data["clientUsername"])
  provider_id = session["user_id"]
  project_id = data["projectId"]
  message = send_message(message, provider_id, client_id, project_id)
  return message
