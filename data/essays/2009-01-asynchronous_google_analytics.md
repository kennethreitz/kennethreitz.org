# Asynchronous Google Analytics!
*January 2009*

Google Analytics now supports Asynchronous loads, which allow the browser to continue loading content while **ga.js** is being loaded. Now it's safe to put the script tag in the `<head>` for you XHTML STRICT junkies.<label for="sn-async-context" class="margin-toggle sidenote-number"></label>
<input type="checkbox" id="sn-async-context" class="margin-toggle"/>
<span class="sidenote">This 2009 post demonstrates Kenneth's early attention to web performance optimization and his engagement with emerging web standards. The enthusiasm for asynchronous loading reflects the web development community's growing understanding of non-blocking JavaScript patterns that would become fundamental to modern web development.</span>

**Here's the new code to do so:**

```javascript
var _gaq = _gaq || [];
_gaq.push(['_setAccount', 'UA-XXXXX-X']);
_gaq.push(['_trackPageview']);

(function() {
    var ga = document.createElement('script');
    ga.src = ('https:' == document.location.protocol ?
        'https://ssl' : 'http://www') +
        '.google-analytics.com/ga.js';
    ga.setAttribute('async', 'true');
    document.documentElement.firstChild.appendChild(ga);
})();
```

## WordPress Plugin Update

I love this new code clip so much, I decided to write a WordPress Plugin for it. Enjoy!

* [GitHub Project Page](http://github.com/kennethreitz/async-google-analytics-wordpress-plugin)
* [Direct WordPress Plugin](http://github.com/kennethreitz/async-google-analytics-wordpress-plugin/zipball/master)<label for="sn-plugin-analysis" class="margin-toggle sidenote-number"></label>
<input type="checkbox" id="sn-plugin-analysis" class="margin-toggle"/>
<span class="sidenote">The creation of a WordPress plugin demonstrates Kenneth's pattern of sharing useful code with the broader community through open-source contributions. This early GitHub project shows his understanding that valuable code snippets should be packaged and distributed for others to benefit from, a philosophy that would define his later approach to Python package development.</span>