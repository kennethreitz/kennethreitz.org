# Responder: a Familar HTTP Service Framework
*2018*


<iframe class="speakerdeck-iframe" style="border: 0px; background: padding-box rgba(0, 0, 0, 0.1); margin: 0px; padding: 0px; border-radius: 6px; box-shadow: rgba(0, 0, 0, 0.2) 0px 5px 40px; width: 100%; height: auto; aspect-ratio: 560 / 420;" frameborder="0" src="https://speakerdeck.com/player/dd164794f3354742af9e0fc288ec1665" title="Responder: a Familiar HTTP Service Framework" allowfullscreen="true" data-ratio="1.3333333333333333"></iframe>


## Introduction

- **Responder** is introduced as a modern HTTP service framework for Python, drawing inspiration from existing tools and frameworks while aiming to innovate and simplify web development.

## Historical Context

- **Early Web Development in Python:**
  - **1999:** Zope + Plone established Python as a viable option for web development, particularly in government sectors.
  - **2003:** Introduction of WSGI<label for="sn-wsgi-standard" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-wsgi-standard" class="margin-toggle"/><span class="sidenote">WSGI (Web Server Gateway Interface) standardized the interface between Python web applications and web servers, enabling interoperability and the ecosystem of middleware we see today.</span>, which became a standard for Python web frameworks.

- **Key Frameworks:**
  - **2005:** Django emerged as a robust framework for content-driven applications, making many architectural decisions for the developer.
  - **2006:** Pylons offered a more component-oriented approach, competing with Django.
  - **2007:** WebOb and Pyramid provided alternatives, with Pyramid being a more reasonable choice compared to Django.

- **Flask:**
  - Initially created as an April Fool's joke<label for="sn-flask-april-fools" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-flask-april-fools" class="margin-toggle"/><span class="sidenote">Armin Ronacher's April Fool's joke in 2010 became one of the most influential Python web frameworks, demonstrating how simplicity and good design can triumph over comprehensive feature sets.</span>, Flask grew in popularity due to its simplicity and user-friendly API, which rarely required documentation.

## The Future: Responder

- **Responder's Vision:**
  - **2019 and Beyond:** Responder is positioned as a future-forward framework, considering modern web development needs like WebSockets, Server-Sent Events (SSE), and ASGI<label for="sn-asgi-evolution" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-asgi-evolution" class="margin-toggle"/><span class="sidenote">ASGI (Asynchronous Server Gateway Interface) represents the evolution beyond WSGI, enabling support for WebSockets, HTTP/2, and other modern protocols that require asynchronous handling.</span>.

- **Design Intentions:**
  - Include **Requests** as the standard HTTP client.
  - Model Request/Response objects closely after Requests’ objects.
  - Aim to create "the world’s best web framework," taking the project seriously and gauging community interest.

## Conclusion

- **Responder** seeks to build on the strengths of past frameworks while introducing new, user-friendly features. The goal is to provide a robust, modern tool for Python developers, with a focus on simplicity and practicality.
