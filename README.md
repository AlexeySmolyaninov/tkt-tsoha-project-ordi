# Project OrDi

## General

This application will be able to connect customers and service provider through the digital interface. Customer will be able to audit progress of a task/project made by service provider and stay in touch with him/her in case of some obstacles or notify if changes must be performed.

To better understand the purpose of an app, let's create a scenario of you as a customer wanting to order some car service.

1. You drop your car at the service. Service stuff tells you that he/she will inform you once it's done, but approximately it will take 1,5 hours.

2. Project has been registrated by service provider in the app for a customer to audit the progress.

3. Customer get's a notification that his/her task is DONE, so the car could be picked up.

4. Customer will be able to complete the payment through an app

---

This app shows it's advantage when amount of services you purchase becomes too hard to handle just by simple message service like WhatsApp.

Also if the project consists of multiple steps like building a house, then project could be splitted into multiple steps to be accomplished.

## Actions

- Create User
- Login/Logout from app
- Create, Modify, Delete Project
  - Create, Modify, Delete Tasks Under the project
- Deposit and Withdraw money from the account
- Chat in the project thread

## Database Architecture

![picture alt](https://raw.githubusercontent.com/AlexeySmolyaninov/tkt-tsoha-project-ordi/master/Database_architecture_diagram.png "OrDi Database Architecture")

## Application Link

https://tsoha-ordi.herokuapp.com/

### Release Notes

- **March 28 2021**:

  - You can register, login, logout, open your wallet, deposit
  - DOING: withdraw from wallet
  - NEXT: Implementation of creation of a new project with the subtasks

- **April 04 2021**:
  - New: withdraw from wallet, view transaction in wallet, create projects under "Services by me", list projects in "Services by me"
  - Next: add tasks to project, update project and tasks
