from db import db

def send_message(message, from_user, to_user, project_id):
  sql = "INSERT INTO messages (message, from_user, to_user, project_id, date) " \
    "VALUES (:message, :from_user, :to_user, :project_id, NOW()) RETURNING id, message"
  message = db.session.execute(
    sql,
    {
      "message": message,
      "from_user": from_user,
      "to_user": to_user,
      "project_id": project_id
    }
  ).fetchone()
  db.session.commit()
  return {
    "id": message[0],
    "msg": message[1]
    }

def get_messages(project_id):
  sql = "SELECT from_user, to_user, message FROM messages " \
    "WHERE project_id = :project_id " \
    "ORDER BY date DESC"
  messages = db.session.execute(sql, {"project_id": project_id}).fetchall()
  return messages