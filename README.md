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

## Guide on how to use an app

### Scenario 1 | You want to create a project to client:

- Login to service / if user don't have account register first
- Go to "Services By Me"
- Click green button "Create New Project"
- Fill the data for the project and click "Create Project"
- If you want to add more tasks to the project click on project "Info >>" and full fill with the task you need
- Once the state of the project or task has changes update it in the specific project view

### Scenario 2 | You want to monitor ordered service

- Login to service / if user don't have account register first
- Go to "Services To Me"
- If the project exists then you can click on "Info >>" link to monitor the exact state of the project
- Complete the payment, so that service provider will be rewarded for his duty

### Release Notes

- **March 28 2021**:

  - You can register, login, logout, open your wallet, deposit
  - DOING: withdraw from wallet
  - NEXT: Implementation of creation of a new project with the subtasks

- **April 04 2021**:

  - New: withdraw from wallet, view transaction in wallet, create projects under "Services by me", list projects in "Services by me"
  - Next: add tasks to project, update project and tasks

- **April 11 2021**:

  - New: Service provider can manage tasks under the project, Client can view his order projects as well look at the tasks of the project, Client can complete the payment, Client or Service Provider can hide the Project once it Done + Payed.
  - Next: Implement Chat functionality under the project

- **April 18 2021**:

  - New: Chat functionality is done, as well restyled an app
  - Next: Polishing design, implmenet comone exception handle, fix some minor UX bugs

- **May 9 2021**:
  - Fixed bugs:
<<<<<<< HEAD
    - body tag is fixed (no-repeat effect)
=======
    - <body> is fixed
>>>>>>> 589cb3e62c1c1814cb68beac782c83e01e1fc8e7
    - when user have send a message input text value will be cleared
    - when trying to create already existing user app won't show db error, instead it will show more user readable
    - user can't change project amount to a negative value
    - when a user trying to login with uknown user error message has been changed to 'wrong credentials'
    - user not able to withdraw and deposit negative amount
    - not possible to create a task with negative amount
