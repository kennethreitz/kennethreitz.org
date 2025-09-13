# Python, Requests, & The Standard Library
*2013*

<iframe class="speakerdeck-iframe" style="border: 0px; background: padding-box rgba(0, 0, 0, 0.1); margin: 0px; padding: 0px; border-radius: 6px; box-shadow: rgba(0, 0, 0, 0.2) 0px 5px 40px; width: 100%; height: auto; aspect-ratio: 560 / 420;" frameborder="0" src="https://speakerdeck.com/player/68f22f0841734d848315c618111b13ea" title="Python, Requests, &amp; The Standard Library" allowfullscreen="true" data-ratio="1.3333333333333333"></iframe>


## Introduction

- **Requests vs Standard Library** discusses the stance of the Requests project regarding its potential inclusion in Python’s standard library, exploring the implications and reasoning behind the decision.

## Requests Overview

- **Features:**
  - Prioritizes security and design.
  - Optimized interfaces for best practices in SSL, connection pooling, encoding, headers, etc.
  - Simplifies interaction with web services.

- **Popularity:**
  - Requests is the most downloaded Python package, with around 42 million downloads from PyPi.
  - Regularly suggested for inclusion in the standard library.

## Arguments for Inclusion

- **Social Responsibility:**
  - Including Requests in the standard library could be seen as the "right thing" to do, given its critical role in the Python ecosystem.

- **Sustainability:**
  - Inclusion could facilitate funding for core contributors, ensuring the project’s long-term sustainability.

- **Chardet:**
  - Chardet, a dependency of Requests, is highlighted as a strong candidate for standard library inclusion due to its utility in character encoding detection.

## Arguments Against Inclusion

- **Independence:**
  - Requests' value lies in its superiority over the standard library; inclusion would diminish its ability to innovate and quickly respond to security incidents or spec changes.

<span class="sidenote">This argument proved prescient. The debate over Requests' standard library inclusion highlighted fundamental questions about Python's development philosophy and the role of third-party packages in a language ecosystem.</span>

- **Flexibility:**
  - Inclusion in the standard library could limit the project’s ability to release updates and improvements promptly.

## Broader Questions

- **Standard Library Goals:**
  - The document questions the current goals of the standard library and whether inclusion is necessary in the era of tools like `ensurepip`.

- **Critical Infrastructure:**
  - Requests is considered critical infrastructure for the Python community, but its inclusion in the standard library might make it less adaptable to change.

## Conclusion

- **Final Stance:**
  - The document leans against including Requests in the standard library, emphasizing the need for the project to remain agile and independent to continue serving the Python community effectively.
