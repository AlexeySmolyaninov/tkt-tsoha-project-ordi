from db import db

def get_users(provider):
  sql = "SELECT id, username FROM users WHERE username NOT LIKE :provider"
  result = db.session.execute(sql, {"provider": provider})
  users = result.fetchall()
  return users

def username_to_userid(username):
  sql = "SELECT id FROM users WHERE username LIKE :username"
  user = db.session.execute(sql, {"username": username}).fetchone()
  return user[0]


def create_project(title, description, provider, client, amount, payed, status, display):
  #create project + task
  sql = "INSERT INTO projects (title, description, provider, client, date, amount, payed, status, display) " \
    "VALUES (:title, :description, :provider, :client, NOW(), :amount, :payed, :status, :display) RETURNING id"
  result = db.session.execute(
    sql,
    {
      "title": title,
      "description": description,
      "provider": provider,
      "client": client,
      "amount": amount,
      "payed": payed,
      "status": status,
      "display": display
    }
  )

  newProject = result.fetchone()

  sql = "INSERT INTO tasks (title, status, project_id, date) " \
    "VALUES (:title, :status, :project_id, NOW())"
  db.session.execute(
    sql,
    {
      "title": title,
      "status": status,
      "project_id": newProject[0]
    }
  )
  db.session.commit();
  return

def get_projects_by_me(provider_id):
  sql = "SELECT p.title, u.username, LEFT(p.description, 20) AS desc, p.status, p.payed, p.id, p.amount FROM projects p INNER JOIN users u ON p.client = u.id WHERE p.provider = :provider_id AND display = True"
  projects = db.session.execute(
    sql,
    {
      "provider_id": provider_id
    }
  ).fetchall()
  return projects

def get_projects_to_me(my_id):
  sql = "SELECT p.title, u.username, LEFT(p.description, 20) AS desc, p.status, p.payed, p.id, p.amount FROM projects p " \
     "INNER JOIN users u ON p.provider = u.id WHERE p.client = :client_id AND display = True"
  projects = db.session.execute(
    sql,
    {
      "client_id": my_id
    }
  ).fetchall()
  return projects

def get_project(id):
  sql = "select p.id, p.title, p.description, u2.username as provider, u.username as client, p.status, p.display from projects p INNER JOIN users u on p.client = u.id INNER JOIN users u2 ON p.provider = u2.id where p.id = :project_id"
  project = db.session.execute(
    sql,
    {
      "project_id": id
    }
  ).fetchone()
  return project

def get_tasks(project_id):
  sql = "SELECT id, title, status, date FROM tasks WHERE project_id = :project_id ORDER BY date"
  tasks = db.session.execute(sql, {"project_id": project_id}).fetchall()
  return tasks

def create_task(title, status, project_id):
  sql = "INSERT INTO tasks (title, status, project_id, date) " \
    "VALUES (:title, :status, :project_id, NOW())"
  db.session.execute(
    sql,
    {
      "title": title,
      "status": status,
      "project_id": project_id
    }
  )
  db.session.commit()
  return