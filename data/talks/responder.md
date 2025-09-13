# Responder: a Familar HTTP Service Framework
*2018*


<iframe class="speakerdeck-iframe" style="border: 0px; background: padding-box rgba(0, 0, 0, 0.1); margin: 0px; padding: 0px; border-radius: 6px; box-shadow: rgba(0, 0, 0, 0.2) 0px 5px 40px; width: 100%; height: auto; aspect-ratio: 560 / 420;" frameborder="0" src="https://speakerdeck.com/player/dd164794f3354742af9e0fc288ec1665" title="Responder: a Familiar HTTP Service Framework" allowfullscreen="true" data-ratio="1.3333333333333333"></iframe>


## Introduction

**Responder** was introduced as a modern HTTP service framework for Python that drew inspiration from the rich history of Python web development while aiming to innovate and dramatically simplify the web development experience. This framework represented both an evolution of existing patterns and a fresh perspective on what Python web development could become in the modern era.

## Historical Context

The presentation traced **Python's web development evolution** from its earliest days. In **1999**, Zope and Plone established Python as a viable web development platform, particularly in government sectors where Python's clarity proved valuable. The **2003** introduction of WSGI created a crucial standardization moment.

<label for="sn-wsgi-standard" class="margin-toggle sidenote-number"></label>
<input type="checkbox" id="sn-wsgi-standard" class="margin-toggle"/>
<span class="sidenote">WSGI (Web Server Gateway Interface) standardized the interface between Python web applications and web servers, enabling interoperability and the ecosystem of middleware we see today.</span>

**Key frameworks** emerged in rapid succession: **Django** (2005) as a comprehensive framework for content applications, **Pylons** (2006) with a component-oriented approach, and **Pyramid** (2007) as a balanced alternative.

**Flask** deserves special recognition for its unique origin and impact.

<label for="sn-flask-april-fools" class="margin-toggle sidenote-number"></label>
<input type="checkbox" id="sn-flask-april-fools" class="margin-toggle"/>
<span class="sidenote">Armin Ronacher's April Fool's joke in 2010 became one of the most influential Python web frameworks, demonstrating how simplicity and good design can triumph over comprehensive feature sets.</span>

Initially an April Fool's joke, Flask's elegant simplicity and intuitive API made it extraordinarily popular—developers could often guess correct usage patterns without consulting documentation.

## The Future: Responder

**Responder's vision** positioned it as a future-forward framework for **2019 and beyond**, designed to address modern web development requirements including WebSockets, Server-Sent Events (SSE), and ASGI support.

<label for="sn-asgi-evolution" class="margin-toggle sidenote-number"></label>
<input type="checkbox" id="sn-asgi-evolution" class="margin-toggle"/>
<span class="sidenote">ASGI (Asynchronous Server Gateway Interface) represents the evolution beyond WSGI, enabling support for WebSockets, HTTP/2, and other modern protocols that require asynchronous handling.</span>

The **design philosophy** embodied Kenneth's "for Humans" approach by including **Requests** as the standard HTTP client and modeling Request/Response objects after Requests' beloved interface patterns. This ensured immediate familiarity for developers already using Requests.

The ambitious goal was explicitly stated: create "the world's best web framework." This represented a serious commitment to excellence, serving as both community interest gauge and platform for cutting-edge web development patterns.

## Conclusion

**Responder** represented an ambitious synthesis of Python web development's rich history with a clear vision for its future. By building on proven strengths while introducing innovative, user-friendly features, the project aimed to provide Python developers with a robust, modern tool maintaining the community's core values of simplicity and practicality.

This framework embodied the evolutionary approach characterizing Kenneth's broader work: respect for the past, clear assessment of current limitations, and bold innovation toward a more human-centered future.
