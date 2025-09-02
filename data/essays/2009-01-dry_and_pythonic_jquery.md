# DRY and Pythonic jQuery?
*January 2009*





Apparently, **groovy:spring:java** as **jabs:jquery:javascript**. As if jQuery wasn't short enough already.<label for="sn-jabs" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-jabs" class="margin-toggle"/><span class="sidenote">This 2009 post captures the era's fascination with domain-specific languages and syntactic sugar—an impulse that would later manifest in CoffeeScript, TypeScript, and modern JavaScript transpilation tools.</span>

 [Jabs](http://github.com/collin/jabs) lets you write this jQuery code:

```javascript
jQuery(function() {
    var $ = jQuery;
    
    $("[default_value]").blur(function() {
        var self = $(this);
        if(self.val() === "") {
            self.val(self.attr("default_value"));
        }
    }).focus(function() {
        var self = $(this);
        if(self.val() === self.attr("default_value")) {
            self.val("");
        }
    }).blur();
});
```

 By typing this:

```coffeescript
$ [default_value]:
  blur:
    if @value === ""
      @value = @default_value
  focus:
    if @value === @default_value
      @value = ""
  .blur
```

 [HAML](http://haml-lang.com/) tactics FTW.<label for="sn-haml" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-haml" class="margin-toggle"/><span class="sidenote">HAML's influence on web development was significant—its indentation-based syntax and DRY principles influenced template engines across many languages, from Slim in Ruby to Pug in JavaScript.</span> 

  