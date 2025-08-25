# Heroku 101

<iframe class="speakerdeck-iframe" style="border: 0px; background: padding-box rgba(0, 0, 0, 0.1); margin: 0px; padding: 0px; border-radius: 6px; box-shadow: rgba(0, 0, 0, 0.2) 0px 5px 40px; width: 100%; height: auto; aspect-ratio: 560 / 420;" frameborder="0" src="https://speakerdeck.com/player/a670a060bb6542b0b6fb55955c0e280c" title="Heroku 101 (v2!)" allowfullscreen="true" data-ratio="1.3333333333333333"></iframe>


## Introduction

- **Heroku 101** provides an overview of Heroku's platform-as-a-service (PaaS) offering, highlighting its simplicity and utility for developers.

## Key Concepts

- **Confusion as a Service:**
  - **SaaS (Software as a Service):** For software users, providing more features and transparent updates (e.g., Facebook, Trello).
  - **IaaS (Infrastructure as a Service):** For operations, offering on-demand machine resources (e.g., AWS, Digital Ocean).
  - **PaaS (Platform as a Service):** For developers, offering transparent updates with no need to manage servers<label for="sn-paas-evolution" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-paas-evolution" class="margin-toggle"/><span class="sidenote">PaaS represented a fundamental shift in developer workflow, abstracting away infrastructure concerns and enabling rapid prototyping and deployment that influenced the entire industry.</span> (e.g., Heroku, App Engine).

## Using Heroku with Python

- **Locally:**
  - Create a virtual environment and install dependencies using `pip`.
  - Run a Python web server with `python manage.py runserver 0.0.0.0:8000`.

- **On Heroku:**
  - Install dependencies with `pip` and deploy using a `Procfile`.
  - The `Procfile` specifies the commands that Heroku should run to start your application.

## Understanding Dynos

- **Dyno:**
  - A Dyno is a lightweight process running in a container<label for="sn-containerization" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-containerization" class="margin-toggle"/><span class="sidenote">Heroku's dyno model was an early implementation of containerization concepts that later evolved into Docker and Kubernetes orchestration patterns.</span>, not a traditional server or VM.
  - Dynos can be scaled to handle multi-process web applications using commands like `heroku scale`.

## Managing Applications

- **Run Arbitrary Commands:**
  - Heroku allows running various commands, such as database migrations or opening an interactive Python shell, using `heroku run`.

- **Addon Services:**
  - Heroku provides managed infrastructure resources like Postgres, Redis, and Kafka<label for="sn-addon-ecosystem" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-addon-ecosystem" class="margin-toggle"/><span class="sidenote">The addon ecosystem pioneered the "marketplace" model for cloud services, allowing third-party providers to integrate seamlessly with the platform through standardized APIs.</span>.
  - Addons are easy to integrate and configure within your application.

- **Application Configuration:**
  - Config variables can be set and managed with `heroku config:set`, enabling environment-specific settings.
