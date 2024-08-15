# The Future of Python Dependencies Management

<iframe class="speakerdeck-iframe" style="border: 0px; background: padding-box rgba(0, 0, 0, 0.1); margin: 0px; padding: 0px; border-radius: 6px; box-shadow: rgba(0, 0, 0, 0.2) 0px 5px 40px; width: 50%; height: auto; aspect-ratio: 560 / 420;" frameborder="0" src="https://speakerdeck.com/player/ee6c0016a8f44dd98900659d225b6925" title="The Future of Python Dependency Management" allowfullscreen="true" data-ratio="1.3333333333333333"></iframe>


## Introduction

- **Pipenv** is presented as the future of Python dependency management, offering a streamlined approach compared to traditional methods like `pip` and `virtualenv`.

## History and Challenges of Python Packaging

- **Initial Problems:**
  - PyPi (formerly "The Cheeseshop") was just an index, not a comprehensive package host.
  - Packages were often hosted externally, and PyPi ran on a single server.
  - Manual processes and global installations led to poor user experiences.

- **Evolution:**
  - **Pip** replaced `easy_install` as the primary package manager.
  - **Virtualenv** became a standard for creating isolated environments.
  - **Requirements.txt** files were introduced to track dependencies.

- **Challenges with Existing Tools:**
  - **Virtualenv** had a steep learning curve and was difficult for newcomers.
  - **Requirements.txt** files often had an impedance mismatch between what was installed and what was needed, leading to non-deterministic builds.

## The Problem with Current Practices

- **Virtualenv Downsides:**
  - Difficult abstraction for beginners.
  - Manual and unnatural to use without additional tools like `virtualenv-wrapper`.

- **Requirements.txt Issues:**
  - Two types of dependency files are needed:
    - One for unpinned dependencies (e.g., "Flask").
    - One for pinned, all-inclusive dependencies.

- **No Lockfile:**
  - Python lacked a lockfile for deterministic dependency management, unlike other communities (e.g., Node.js, PHP).

## The Solution: Pipfile and Pipenv

- **Pipfile:**
  - A new standard designed to replace `requirements.txt`.
  - **Pipfile** is a TOML file that is easy to read and write.
  - It includes two sections: `[packages]` for production and `[dev-packages]` for development dependencies.

- **Pipfile.lock:**
  - A machine-readable JSON file that contains pinned dependencies and acceptable hashes for each release, ensuring deterministic builds.

- **Challenges with Pipfile:**
  - Pipfile is not yet integrated into `pip`, and full integration may take time due to resource constraints.

## Pipenv: The Recommended Tool

- **Pipenv Features:**
  - Officially recommended by Python.org.
  - Automates virtualenv management and uses Pipfile/Pipfile.lock for dependency management.
  - Ensures deterministic builds and performs hash check verification during installation.

- **User Testimonials:**
  - **Jannis Leidel** (former pip maintainer) praises Pipenv for replacing manual virtualenv and pip calls.
  - **Justin Myles Holmes** commends Pipenv for being an abstraction that engages the mind, not just the filesystem.

## Conclusion

- Pipenv is portrayed as a significant advancement in Python dependency management, offering a more intuitive and deterministic approach compared to traditional methods.
