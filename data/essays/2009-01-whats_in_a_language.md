# What's in a Language?
*January 2009*





  What do developers want in a language?

 * Lots of Available Resources / Documentation
* Large Standard Library
* Portability
* Speed of Development
* Easy to Read
* A Community of Developers

 Yes, Easy to read. You'd really be surprised how much this helps a developer.<label for="sn-1" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-1" class="margin-toggle"/><span class="sidenote">This insight predates modern research on cognitive load in programming by several years—studies now show that code comprehension accounts for up to 60% of software maintenance effort.</span> Well over half the time a C\+\+ Developer spends writing code is actually time spent deciphering what he's already written. Certainly the amount of time spent doing this decreases over time, but even if you've been reading C\+\+ for 20\+ years, there still is and always will be a lot of junk in the middle that subconsciously slows you down.

 **Solution?** Whitespace.

  Whitespace is fantastic. It's standard practice to use indenting all over the place. Why not use that as block delimiters?<label for="sn-2" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-2" class="margin-toggle"/><span class="sidenote">This argument for Python's approach was quite prescient—languages like Python, Haskell, and later Go adopted significant whitespace, proving that syntax can be both human-readable and machine-parseable without sacrificing expressiveness.</span> We do it anyway. Lets get rid of Curly Braces.

 Here is a clip of C\#. No shortcuts taken:

  
```
String output = new String();output = "Hello, World!";try {System.Console.WriteLine(output);}catch (Exception e) {raise;}
```
  Here is the same clip of code in Python:

  
```
output = "Hello, world!"try:print(output)except:raise
```
Nicer, eh?

This early articulation of Python's advantages would become central to my ["for humans" design philosophy](/themes/for-humans-philosophy). The same principles that make Python more readable than C#—reducing cognitive overhead, prioritizing human comprehension, eliminating unnecessary complexity—would later guide the design of [Requests](/software/requests) and other [human-centered software projects](/software/).

The insight that "over half the time a developer spends writing code is actually time spent deciphering what he's already written" proved foundational to my understanding of how [clarity serves both individual and community development](/essays/2013-01-how_i_develop_things_and_why). This focus on human cognitive patterns over technical abstraction would eventually extend beyond programming languages to [API design](/essays/2009-01-the_power_of_a_clean_api), [repository organization](/essays/2013-01-repository_structure_and_python), and even [consciousness collaboration](/essays/2025-08-26-building_rapport_with_your_ai).

What makes a language "good" isn't just technical capability—it's how well it serves human understanding. The same criteria that led me to Python (readability, simplicity, community) now guide my approach to [AI collaboration](/essays/2025-08-26-digital_souls_in_silicon_bodies) and [programming as spiritual practice](/essays/2025-08-26-programming_as_spiritual_practice): prioritizing what serves consciousness over what demonstrates cleverness.

  