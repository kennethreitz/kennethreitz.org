# The 12 Factor App

This talk recaps the 12 Factor App methodology, which is a set of best practices for building scalable, maintainable, and portable web applications.

<iframe class="speakerdeck-iframe" style="border: 0px; background: padding-box rgba(0, 0, 0, 0.1); margin: 0px; padding: 0px; border-radius: 6px; box-shadow: rgba(0, 0, 0, 0.2) 0px 5px 40px; width: 100%; height: auto; aspect-ratio: 560 / 420;" frameborder="0" src="https://speakerdeck.com/player/4f22cc6da0a84d0022028725" title="The 12 Factor App." allowfullscreen="true" data-ratio="1.3333333333333333"></iframe>



## Introduction

- **The Twelve-Factor App** is a methodology for building software-as-a-service (SaaS) applications that ensures consistency, scalability, and ease of deployment across different environments.

<span class="sidenote">Kenneth's presentation of the 12-factor methodology at Heroku helped establish these principles as industry standards. The methodology codified practices that Heroku discovered through hosting thousands of applications, making implicit knowledge explicit.</span>

## I. Codebase

- **Single Codebase:**
  - One codebase tracked in version control, deployed in multiple environments.
  - If multiple codebases exist, the system is considered distributed rather than a single app.

## II. Dependencies

- **Explicit Declaration:**
  - Dependencies must be explicitly declared and isolated.
  - The app should not rely on system-wide packages or tools, ensuring portability and consistency.

## III. Config

- **Environment-Based Configuration:**
  - Configuration, including database and service handles, should be stored in the environment, making it easy to manage different deployment environments.

<span class="sidenote">The configuration principle fundamentally changed how developers think about application deployment. By externalizing configuration, applications became truly portable across environments, a concept that seems obvious now but was revolutionary when first articulated.</span>

## IV. Backing Services

- **Treat as Attached Resources:**
  - There should be no distinction between local and third-party services; all are treated as attached resources.

## V. Build, Release, Run

- **Separation of Stages:**
  - The build, release, and run stages should be strictly separated to allow for rollbacks and better release management.

## VI. Processes

- **Stateless Processes:**
  - The app runs as one or more stateless processes, with each process type handling different workloads.

## VII. Port Binding

- **Export Services via Port Binding:**
  - The app should expose services by binding to a port and listening for requests, enabling seamless integration with web servers.

## VIII. Concurrency

- **Scale via Process Model:**
  - Scale the app by assigning workloads to different process types, managed by the operating system’s process manager.

## IX. Disposability

- **Fast Startup and Graceful Shutdown:**
  - The app should be disposable, capable of starting or stopping on short notice to ensure robustness.

## X. Dev/Prod Parity

- **Maintain Similar Environments:**
  - Development, staging, and production environments should be kept as similar as possible to minimize gaps in time, personnel, and tools.

## XI. Logs

- **Treat Logs as Event Streams:**
  - Logs should be treated as continuous event streams, with no concern for their routing or storage by the app itself.

## XII. Admin Processes

- **Run as One-Off Processes:**
  - Administrative tasks should be run as one-off processes in the same environment as the app, using the same code and configuration.

---

For more details, visit [12factor.net](https://12factor.net).
