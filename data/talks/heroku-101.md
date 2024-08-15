# Heroku 101

<iframe class="speakerdeck-iframe" style="border: 0px; background: padding-box rgba(0, 0, 0, 0.1); margin: 0px; padding: 0px; border-radius: 6px; box-shadow: rgba(0, 0, 0, 0.2) 0px 5px 40px; width: 50%; height: auto; aspect-ratio: 560 / 420;" frameborder="0" src="https://speakerdeck.com/player/a670a060bb6542b0b6fb55955c0e280c" title="Heroku 101 (v2!)" allowfullscreen="true" data-ratio="1.3333333333333333"></iframe>


## Introduction

- **Heroku 101** provides an overview of Heroku's platform-as-a-service (PaaS) offering, highlighting its simplicity and utility for developers.

## Key Concepts

- **Confusion as a Service:**
  - **SaaS (Software as a Service):** For software users, providing more features and transparent updates (e.g., Facebook, Trello).
  - **IaaS (Infrastructure as a Service):** For operations, offering on-demand machine resources (e.g., AWS, Digital Ocean).
  - **PaaS (Platform as a Service):** For developers, offering transparent updates with no need to manage servers (e.g., Heroku, App Engine).

## Using Heroku with Python

- **Locally:**
  - Create a virtual environment and install dependencies using `pip`.
  - Run a Python web server with `python manage.py runserver 0.0.0.0:8000`.

- **On Heroku:**
  - Install dependencies with `pip` and deploy using a `Procfile`.
  - The `Procfile` specifies the commands that Heroku should run to start your application.

## Understanding Dynos

- **Dyno:**
  - A Dyno is a lightweight process running in a container, not a traditional server or VM.
  - Dynos can be scaled to handle multi-process web applications using commands like `heroku scale`.

## Managing Applications

- **Run Arbitrary Commands:**
  - Heroku allows running various commands, such as database migrations or opening an interactive Python shell, using `heroku run`.

- **Addon Services:**
  - Heroku provides managed infrastructure resources like Postgres, Redis, and Kafka.
  - Addons are easy to integrate and configure within your application.

- **Application Configuration:**
  - Config variables can be set and managed with `heroku config:set`, enabling environment-specific settings.
