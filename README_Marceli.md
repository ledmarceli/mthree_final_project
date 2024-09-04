# Income Tax Calculator App 

Authors: Marceli Ciesielski, John Dela Cruz, Eduar Mancera
This project was submitted as a final project assignment at the mthree academy training on the 6th of September 2024.

## Marceli Contributions

Front-End HTML CSS files, backend Python file, selenium testing file, Dockerfile, SQL Lite

## Table of Contents

- [Introduction](#introduction)
- [Front-End](#front-end)
- [Back-End](#back=end)
- [Docker](#docker)
- [Jenkins](#jenkins)
- [Kubernetes](#kubernetes)
- [Grafana](#grafana)
- [Testing](#testing)

## Introduction

This app provides a simple income tax calculator with a user-friendly interface to collect and process user information. The data entered by the user is processed by a Python script on the server side, with the results saved in a database and displayed back to the user. While the web-app's functionality is straightforward, it is supported by a robust and multi-level infrastructure designed for scalability, continuous integration, and monitoring.

The application is containerized using Docker, ensuring consistency across development, testing, and production environments. The deployment process is managed using Kubernetes, which orchestrates the containers, providing high availability and scalability. Jenkins is integrated into the setup to automate the build, and deployment pipelines, enabling continuous integration and delivery. Additionally, Grafana is used for real-time monitoring of the application, providing insights into performance metrics, resource usage, and overall system health.

## Front-End

The front-end of the application consists of simple HTML and CSS files found in /python_scripts/templates and /python_scripts/static respectively. These two provide a basic and user-friendly interface to communicate with the user and send the information provided through an HTML form to the backend script.

## Back-End

The back-end of the application is located in a single file found in /python_scripts/app.py. This script loads the database, reads and processes the user input, updates the database and sends the processed data to the result page. 