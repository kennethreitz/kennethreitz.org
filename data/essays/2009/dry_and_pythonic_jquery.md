# DRY and Pythonic jQuery?

  Apparently, **groovy:spring:java** as **jabs:jquery:javascript**. As if jQuery wasn't short enough already.

 [Jabs](http://github.com/collin/jabs) lets you write this jQuery code:

  jQuery(function() {var $ \= jQuery;

  $("\[default\_value]").blur(function() {var self \= $(this);if(self.val() \=\=\= "") {self.val(self.attr("default\_value"));}}).focus(function() {var self \= $(this);if(self.val \=\=\= self.attr("default\_value")) {self.val("");}}).blur();});

 By typing this:

  $ \[default\_value]:blurif @value \=\=\= ""@value \= @default\_value:focusif @value \=\=\= @default\_value@value \= "".blur

 [HAML](http://haml-lang.com/) tactics FTW. 

  