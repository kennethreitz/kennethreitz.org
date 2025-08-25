# DRY and Pythonic jQuery?

Apparently, **groovy:spring:java** as **jabs:jquery:javascript**. As if jQuery wasn't short enough already.<label for="sn-jabs" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-jabs" class="margin-toggle"/><span class="sidenote">This 2009 post captures the era's fascination with domain-specific languages and syntactic sugar—an impulse that would later manifest in CoffeeScript, TypeScript, and modern JavaScript transpilation tools.</span>

 [Jabs](http://github.com/collin/jabs) lets you write this jQuery code:

  jQuery(function() {var $ \= jQuery;

  $("\[default\_value]").blur(function() {var self \= $(this);if(self.val() \=\=\= "") {self.val(self.attr("default\_value"));}}).focus(function() {var self \= $(this);if(self.val \=\=\= self.attr("default\_value")) {self.val("");}}).blur();});

 By typing this:

  $ \[default\_value]:blurif @value \=\=\= ""@value \= @default\_value:focusif @value \=\=\= @default\_value@value \= "".blur

 [HAML](http://haml-lang.com/) tactics FTW.<label for="sn-haml" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-haml" class="margin-toggle"/><span class="sidenote">HAML's influence on web development was significant—its indentation-based syntax and DRY principles influenced template engines across many languages, from Slim in Ruby to Pug in JavaScript.</span> 

  