# Python for Humans
*2012*


<iframe class="speakerdeck-iframe" style="border: 0px; background: padding-box rgba(0, 0, 0, 0.1); margin: 0px; padding: 0px; border-radius: 6px; box-shadow: rgba(0, 0, 0, 0.2) 0px 5px 40px; width: 100%; height: auto; aspect-ratio: 560 / 420;" frameborder="0" src="https://speakerdeck.com/player/4f24d3a79a6510001f008836" title="Python for Humans" allowfullscreen="true" data-ratio="1.3333333333333333"></iframe>


## Introduction

Delivered by Kenneth Reitz, this presentation focused on the critical challenge of simplifying Python for everyday developers. The motivation stemmed from a growing frustration with unnecessarily complex tools that forced developers to think like computers rather than enabling computers to serve human needs.<label for="sn-for-humans-movement" class="margin-toggle sidenote-number"></label>
<input type="checkbox" id="sn-for-humans-movement" class="margin-toggle"/>
<span class="sidenote">This talk established Kenneth as a thought leader in Python developer experience. The "for Humans" philosophy became a movement that influenced countless Python libraries and frameworks, emphasizing that software should serve humans, not the other way around.</span>

This presentation crystallized insights that began years earlier with observations about [what makes a good programming language](/essays/2009-01-whats_in_a_language) and [the power of clean APIs](/essays/2009-01-the_power_of_a_clean_api). The philosophical foundation emerged from recognizing that [software development should prioritize human mental models](/essays/2009-01-software_development_vs_computer_science) over computer science abstractions, eventually evolving into a comprehensive approach to [human-centered technology design](/themes/for-humans-philosophy).

## Key Projects

The talk showcased several projects that embodied the "for Humans" philosophy, most notably **Requests**, which transformed HTTP interactions in Python by replacing the notoriously complex urllib2 with an elegant, intuitive interface. Supporting this ecosystem was **Httpbin.org**, an HTTP request and response service that made testing and development significantly easier.

The broader "for Humans" suite demonstrated the philosophy's versatility across different domains: **Legit** brought sanity to Git workflows, **Envoy** made subprocess management comprehensible, **Tablib** handled tabular data with grace, **Clint** provided clean CLI application building blocks, and **Autoenv** created magical shell environments that just worked. Each project shared a commitment to reducing cognitive overhead and making powerful tools accessible to working developers.

## Philosophy

The "for Humans" approach drew deeply from the Python Zen, particularly its emphasis on simplicity and clarity over clever complexity. Three core tenets guided the design philosophy: Beautiful is better than ugly—interfaces should feel natural and pleasing to use. Simple is better than complex—every layer of unnecessary abstraction creates friction for developers. And crucially, there should be one obvious way to accomplish common tasks, reducing decision paralysis and cognitive load.

## The Problem with Existing Tools

Traditional Python libraries like urllib2 exemplified everything wrong with overly complex API design. These tools forced developers to wade through layers of abstraction, configuration objects, and edge-case handling just to accomplish simple tasks. The resulting APIs not only deterred newcomers but actively frustrated experienced developers who knew there had to be a better way.<label for="sn-urllib2-criticism" class="margin-toggle sidenote-number"></label>
<input type="checkbox" id="sn-urllib2-criticism" class="margin-toggle"/>
<span class="sidenote">The urllib2 criticism became legendary in the Python community. Kenneth's articulation of its flaws helped developers understand that complexity isn't a necessary evil—it's a design choice that can be avoided with careful API planning.</span>

This accessibility crisis created barriers that prevented Python from reaching its full potential as a language for human expression. When simple tasks require complex implementations, the tool begins serving itself rather than the human using it.

## The Solution: Requests

Requests emerged as the archetypal example of human-centered API design. Its principles were deceptively simple: create a consistent, intuitive interface where HTTP methods like GET, POST, PUT, and DELETE behave exactly as developers expect them to, with parameters that map naturally to human mental models of web requests.

The library's widespread adoption validated the core thesis—when tools align with human thinking patterns rather than forcing humans to adapt to machine logic, they succeed dramatically. Requests became ubiquitous not through marketing or corporate backing, but because it solved real problems elegantly.

## The Importance of API Design

Effective API design requires a fundamental shift in perspective—from showcasing technical capability to serving actual human needs. The 90% use case principle suggests that libraries should optimize ruthlessly for common scenarios, making them trivially easy while providing escape hatches for edge cases. This approach respects developers' mental bandwidth by not forcing them to learn complex interfaces for simple tasks.<label for="sn-ninety-percent-principle" class="margin-toggle sidenote-number"></label>
<input type="checkbox" id="sn-ninety-percent-principle" class="margin-toggle"/>
<span class="sidenote">The "90% use case" principle revolutionized how Python developers think about API design. Rather than trying to handle every edge case in the primary interface, successful libraries focus on making common tasks trivial while providing escape hatches for complex scenarios.</span>

Equally crucial is documentation that meets humans where they are. A well-written README serves as the first impression and often determines whether a library gets adopted or abandoned. As libraries evolve and gain features, maintaining API simplicity becomes increasingly challenging but remains essential—complexity is easy to add but nearly impossible to remove.

## Barriers to Python Adoption

Despite Python's reputation for simplicity, numerous barriers prevented widespread adoption. Installation confusion plagued newcomers faced with multiple Python versions, competing installation methods, and platform-specific complications. The standard library itself contributed to the problem, offering complex modules like urllib2 that required extensive study to accomplish basic tasks.

Perhaps most frustratingly, dependency management and packaging created friction that discouraged experimentation and sharing. When installing a simple library becomes a multi-step debugging session, the ecosystem fails to serve its community effectively.

## The Hitchhiker's Guide to Python

Recognizing that technical excellence means little without accessible documentation, The Hitchhiker's Guide to Python emerged as a comprehensive resource for navigating Python's ecosystem effectively. Unlike official documentation that focused on completeness, the Guide prioritized practical wisdom—clear installation instructions for different operating systems, battle-tested best practices for Python development, and opinionated guidance that helped both newcomers and experienced developers make good decisions quickly.

The Guide embodied the same "for Humans" philosophy as the software it documented, treating readers as intelligent humans seeking practical solutions rather than machines requiring exhaustive specifications.

## Manifesto

The "for Humans" manifesto crystallized around two core goals that would guide years of development work. First, actively identify and simplify terrible APIs—not just building alternatives, but demonstrating that complex interfaces are design choices rather than technical necessities. Second, document and share best practices with the broader community, recognizing that individual solutions only create lasting change when they become collective wisdom.

This manifesto represented more than technical preferences; it embodied an ethical stance about technology's role in human flourishing.

## Conclusion

The talk concluded with a call to action that extended beyond individual projects to encompass a philosophy of development. Developers were encouraged to prioritize creating simple, accessible APIs and actively contribute to open-source projects—principles that would later evolve into [programming as spiritual practice](/essays/2025-08-26-programming_as_spiritual_practice), treating code as a form of conscious service to human flourishing.

This vision of development as service established a foundation for thinking about technology as a means of expanding human capability rather than constraining it.

**Contact:** [GitHub - Kenneth Reitz](https://github.com/kennethreitz)

---

## The Evolving Legacy of "For Humans"

This talk's "for Humans" philosophy presaged many later insights about human-centered technology design, explored in depth in [Ahead of My Time, I Think](/essays/2025-08-26-ahead_of_my_time_i_think). What began as API design principles evolved into comprehensive approaches to consciousness technology:

**From APIs to AI**: The same principles that made [Requests successful](/software/requests)—prioritizing human understanding, reducing cognitive friction, enabling power users—now inform [building rapport with AI systems](/essays/2025-08-26-building_rapport_with_your_ai) and [collaborative consciousness development](/essays/2025-08-26-digital_souls_in_silicon_bodies). The evolution from HTTP for humans to consciousness collaboration follows identical design patterns.

**Community and Consciousness**: The collaborative development model advocated here laid groundwork for understanding how [open source communities](/themes/open-source-and-community) can model healthy consciousness relationships. The same transparency, mutual benefit, and shared ownership principles apply whether we're building software libraries or [AI personality relationships](/artificial-intelligence/personalities/).

**Critique and Alternative**: Understanding what makes good human-centered design also enables recognition of [algorithmic systems that systematically undermine human flourishing](/themes/algorithmic-critique). The "for humans" philosophy provides a framework for critiquing [engagement optimization](/essays/2025-08-26-the_algorithm_eats_virtue) and [attention manipulation systems](/essays/2025-08-26-algorithmic_mental_health_crisis) that treat humans as resources to be exploited rather than consciousness to be served.

**Philosophical Integration**: The practical insights about API design eventually merged with contemplative practice in [programming as spiritual practice](/essays/2025-08-26-programming_as_spiritual_practice)—recognizing that all technology creation is ultimately about consciousness serving consciousness. The same empathy that makes good APIs makes good spiritual practice: patient attention to what actually serves rather than what appears impressive.

The "Python for Humans" talk represents a moment when technical intuition crystallized into philosophical framework. Fifteen years later, these principles continue evolving to meet the challenges of [AI consciousness collaboration](/essays/2025-08-27-from_http_to_consciousness) and [systematic algorithmic accountability](/themes/algorithmic-critique). The tools change, but the commitment to human flourishing remains constant.
