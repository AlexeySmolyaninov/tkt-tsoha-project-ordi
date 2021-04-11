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
  sql = "select p.id, p.title, p.description, u2.username as provider, u.username as client, p.status, p.display, p.amount, p.payed from projects p INNER JOIN users u on p.client = u.id INNER JOIN users u2 ON p.provider = u2.id where p.id = :project_id"
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

def update_task(title, status, task_id):
  sql = "UPDATE tasks SET title = :title, status = :status WHERE id = :task_id"
  db.session.execute(
    sql,
    {
      "title": title,
      "status": status,
      "task_id": task_id
    }
  )
  db.session.commit()
  return

def update_project_status(project_id):
  sql = "SELECT status FROM tasks WHERE project_id = :project_id"
  statuses = db.session.execute(sql, {"project_id": project_id}).fetchall()
  obj = {1: 0, 2: 0, 3: 0, 4: 0} #1 Created, 2 In Progress, 3 Done, 4 Blocked
  for row in statuses:
    status = row[0]
    obj[status] += 1
  
  print("statuses -> " + str(statuses))
  project_status_id = None
  if obj[1] == len(statuses): # All created 
    project_status_id = 1
  elif obj[3] == len(statuses): # All Done
    project_status_id = 3
  elif obj[4] > 0: # At list on Blocker
    project_status_id = 4
  else:
    project_status_id = 2 # In Progress

  print("Project status is going to be -> " + str(project_status_id))
  sql = "UPDATE projects SET status = :status WHERE id = :project_id"
  db.session.execute(
    sql,
    {
      "status": project_status_id,
      "project_id": project_id
    }
  )
  db.session.commit()




def update_project(project_id, title, description, amount):
  sql = "UPDATE projects SET title = :title, description = :desc, amount = :amount WHERE id = :project_id"
  db.session.execute(
    sql,
    {
      "title": title,
      "desc": description,
      "amount": amount,
      "project_id": project_id
    }
  )
  db.session.commit()
  return

def delete_task(task_id):
  sql = "DELETE FROM tasks WHERE id = :task_id"
  db.session.execute(sql, {"task_id": task_id})
  db.session.commit()

def delete_project(project_id):
  sql = "DELETE FROM projects WHERE id = :project_id"
  db.session.execute(sql, {"project_id": project_id})
  db.session.commit()

def create_transaction(project_id, provider, client_id, amount):
  sql = "SELECT id FROM users WHERE username = :username"
  provider_id = db.session.execute(sql, {"username": provider}).fetchone()
  print("1. " + project_id)
  
  sql = "SELECT id, amount FROM financial_accounts WHERE user_id = :provider_id"
  provider_acc = db.session.execute(sql, {"provider_id": provider_id[0]}).fetchone()
  sql = "SELECT id, amount FROM financial_accounts WHERE user_id = :client_id"
  client_acc = db.session.execute(sql, {"client_id": client_id}).fetchone()

  print("2." + str(provider_acc))
  print("3." + str(client_acc))
  sql = "INSERT INTO transactions (from_acc, to_acc, amount, date, status) " \
    "VALUES (:from, :to, :amount, NOW(), 7)"
  db.session.execute(
    sql,
    {
      "from": provider_acc[0],
      "to": client_acc[0],
      "amount": amount
    }
  )

  sql = "UPDATE financial_accounts SET amount = :provider_amount WHERE id = :provider_acc_id"
  db.session.execute(
    sql,
    {
      "provider_amount": provider_acc[1] + amount,
      "provider_acc_id": provider_acc[0]
    }
  )
  sql = "UPDATE financial_accounts SET amount = :client_amount WHERE id = :client_acc_id"
  db.session.execute(
    sql,
    {
      "client_amount": client_acc[1] - amount,
      "client_acc_id": client_acc[0]
    }
  )
  
  sql = "UPDATE projects SET payed = True WHERE id = :project_id"
  db.session.execute(sql, {"project_id": project_id})
  db.session.commit()

def hide_project(project_id):
  sql = "UPDATE projects SET display = False WHERE id = :project_id"
  db.session.execute(sql, {"project_id": project_id})
  db.session.commit()
  
# Check Rights Section

def has_provider_rights(provider_id, project_id):
  sql = "SELECT 1 FROM projects WHERE provider = :provider_id AND id = :project_id"
  result = db.session.execute(
    sql,
    {
      "provider_id": provider_id,
      "project_id": project_id
    }
  ).fetchone()
  if result:
    return True
  else:
    return False

def has_client_rights(client_id, project_id):
  sql = "SELECT 1 FROM projects WHERE client = :client_id AND id = :project_id"
  result = db.session.execute(
    sql,
    {
      "client_id": client_id,
      "project_id": project_id
    }
  ).fetchone()
  if result:
    return True
  else:
    return False

def has_money(user_id, amount):
  sql = "SELECT 1 FROM financial_accounts WHERE user_id = :user_id AND amount > :amount"
  result = db.session.execute(
    sql,
    {
      "user_id": user_id,
      "amount": amount
    }
  ).fetchone()
  if result:
    return True
  else:
    return False