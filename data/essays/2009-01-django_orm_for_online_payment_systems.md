# Django ORM for Online Payment Systems?

  I've been spending an increasingly large amount of time with some rapid development frameworks, primarily Django (Python!), Grails (Groovy / Java), and Symfony (PHP)<label for="sn-1" class="margin-toggle sidenote-number"></label>
<input type="checkbox" id="sn-1" class="margin-toggle"/>
<span class="sidenote">Kenneth's framework experimentation in 2009 reflects the polyglot programming movement of the era—before the current dominance of React and Node.js, developers explored diverse languages and paradigms to find the most productive development experience.</span>. I've been enjoying it. Alot. Life has never been better.

 DRY tactics. Code portability. Who likes to repeat themsleves anyway? It’s a great idea.

  My favorite concept to date is the Object Relational Model (ORM). Database\-agnostcisty is fantastic<label for="sn-2" class="margin-toggle sidenote-number"></label>
<input type="checkbox" id="sn-2" class="margin-toggle"/>
<span class="sidenote">Kenneth's enthusiasm for ORMs and abstraction layers would become a defining characteristic of his library design philosophy—from Requests hiding HTTP complexity to Pipenv abstracting dependency management, he consistently sought to eliminate boilerplate.</span>. Not sure what database you want to use? Worry about it later. A client wants to switch to MySQL because SQLServer is costing too much? No problem. How much of my codebase will I have to change? About six charecters. Wow.

 So why not take this concept, and apply it elsewhere? I’m currently doing some work for a startup, and we are having trouble deciding which online payment service to use/support: PayPal, Amazon Payments, or Google Checkout.

  My solution is to write a webPaySystem module that integrates all of these payment systems into one single class<label for="sn-3" class="margin-toggle sidenote-number"></label>
<input type="checkbox" id="sn-3" class="margin-toggle"/>
<span class="sidenote">This early conceptualization of payment system abstraction anticipated the modern fintech API ecosystem—services like Stripe later succeeded by providing exactly this kind of unified, developer-friendly interface that Kenneth envisioned.</span>. But, before I spend the time to write this, I'd like to extend this question to the Python / Django community:

 Would you find this useful in your web (and business desktop) applications?

 Comment and let me know what you think!

  