# Todo

This project was generated with [Angular CLI](https://github.com/angular/angular-cli) version 8.3.20.

## Development server

Run `ng serve` for a dev server. Navigate to `http://localhost:4200/`. The app will automatically reload if you change any of the source files.

## Code scaffolding

Run `ng generate component component-name` to generate a new component. You can also use `ng generate directive|pipe|service|class|guard|interface|enum|module`.

## Build

Run `ng build` to build the project. The build artifacts will be stored in the `dist/` directory. Use the `--prod` flag for a production build.

## Running unit tests

Run `ng test` to execute the unit tests via [Karma](https://karma-runner.github.io).

## Running end-to-end tests

Run `ng e2e` to execute the end-to-end tests via [Protractor](http://www.protractortest.org/).

## Further help

To get more help on the Angular CLI use `ng help` or go check out the [Angular CLI README](https://github.com/angular/angular-cli/blob/master/README.md).





# SOFTWARE REQUIREMENTS SPECIFICATION for Angular-powered ToDo-List

## Contents

- 1 Introduction
   - 1.1 Purpose
   - 1.2 Intended Audience and Reading Suggestions.
   - 1.3 Project Scope.
   - 1.4 References.
- 2 Overall Description
   - 2.1 Product Perspective
   - 2.2 Product Functions
   - 2.3 User Classes and Characteristics
   - 2.4 Operating Environment
   - 2.5 Design and Implementation Constraints
   - 2.6 User Documentation
   - 2.7 Assumptions and Dependencies
- 3 External Interface Requirements
   - 3.1 User Interfaces
   - 3.2 Software Interfaces
- 4 System Features
   - 4.1 Frontend/GUI
      - 4.1.1 Description and Priority.
   - 4.2 Client-Server API.
      - 4.2.1 Description and Priority.
   - 4.3 Server-Database API.
   - 4.4 Appendix A: To Be Determined List


## Revision History

```
Name Date Reason For Changes Version
Björn Biester 04.01.2020 first version 0.0.
Björn Biester 29.01.2020 basic structure 0.0.
```

## 1 Introduction

### 1.1 Purpose

This SRS covers the description and identification of the ”Angular-powered ToDo-List”-
project started by Björn Biester as a substitution for the application ”Wunderlist”, which
will be discontinued by the 6th of Mai 2020. The basic function should be the creation,
organisation and structuring of several tasks (ToDos).

### 1.2 Intended Audience and Reading Suggestions.

This document is meant for all interested programmers and designers which are inter-
ested in contributing to this project. I suggest to read the scope and the description of
functionality. I don’t expect this application to gain too much complexity, so this SRS
will probably be a bit overkill.

### 1.3 Project Scope.

The goal is to create a selfhostable server-client based application that allows the user
to create todos, provide additional information for them and organize them in different
lists. The client will be web-based angular application. The server will be written in
python. The use of a database is also in scope, but not exactly planned yet.

### 1.4 References.

The GitHub repository linked to this project could be found here:Link


## 2 Overall Description

### 2.1 Product Perspective

As stated in the purpose, this project should replace the application ”Wunderlist”, which
will be discontinued by the 6th of Mai 2020. After 6th of Mai, ”Wunderlist” will be
replaced officially with Microsoft’s ”ToDo”. I don’t like the functionality and the third-
party integration of ”ToDo”, so this project was created.

### 2.2 Product Functions

A user should be able to create a task, assign it to a list, provide details to the task, set
due times and notifications. After he finished all things he should be able to mark it as
complete and delete it if wanted to.

### 2.3 User Classes and Characteristics

Users can be of many types. Due to the easyness of the project concept nearly everybody
should be able to intuitively use the application.

### 2.4 Operating Environment

This client will operate in all common browser.
The server will run on every system, which supports the installation of python3 and
higher. Depending on the ongoing design and programming, the host will also need a
database

### 2.5 Design and Implementation Constraints

This project should be scaleable, so system requirements are only relevant on server-side
if you plan to use this for a high amount of users.

### 2.6 User Documentation

There will be a basic online documentation which will explain the usage of the applica-
tion.


### 2.7 Assumptions and Dependencies

Main used third-party dependencies will be:

- Node.js for the npm package-manager
- Python
- Angular (including Angular CLI)
- Typescript
- git-scm for code version history
- Bootstrap for styling
- HTML


## 3 External Interface Requirements

### 3.1 User Interfaces

Most of the GUI will be made with Bootstrap and Angular Material. this means most
of the layout will be given by the Frameworks themselves.
Any custom style themes will be orientated by those frameworks.

### 3.2 Software Interfaces

On the server-side is planned to support Windows Server and Ubuntu Server. On the
client-side all common web browser will be supported.


## 4 System Features

Provided Services are mainly the API to communicate between the client and the server
and the API between server and database.

### 4.1 Frontend/GUI

#### 4.1.1 Description and Priority.

Priority: Normal
Will provide all needed functions to display the todo which will be handed over from
the API

### 4.2 Client-Server API.

#### 4.2.1 Description and Priority.

Priority: Normal
This API will provide the communication interface to provide all needed data for the
client to display the todos. Classes already known to be needed:

- ToDo
- ToDo-List

Methods already known to be needed:

- GetListNames
- Get ToDos in a given List
- Get ToDo with details

### 4.3 Server-Database API.

Priority: Low This API will handle all queries and communication with the database to
store the lists and todos


## 5 Appendices

### 4.4 Appendix A: To Be Determined List

- use of database
