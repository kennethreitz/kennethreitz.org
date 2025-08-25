# Asynchronous Google Analytics!

> **Note**: This 2009 post demonstrates Kenneth's early attention to web performance optimization and his engagement with emerging web standards. The enthusiasm for asynchronous loading reflects the web development community's growing understanding of non-blocking JavaScript patterns that would become fundamental to modern web development.

  Google Analytics now supports Asyncronous loads, which allow the browser to continue loading content while **ga.js** is being loaded. Now it's safe to put the script tag in the  `<head>` for you XHTML STRICT junkies. 

 **Here's the new code to do so:**

  var \_gaq \= \_gaq \|\| \[];\_gaq.push(\['\_setAccount', 'UA\-XXXXX\-X']);\_gaq.push(\['\_trackPageview']);

  (function() {var ga \= document.createElement('script');ga.src \= ('https:' \=\= document.location.protocol ?'https://ssl' : 'http://www') \+'.google\-analytics.com/ga.js';ga.setAttribute('async', 'true');document.documentElement.firstChild.appendChild(ga);})();

 \#\# WordPress Plugin UpdateI love this new code clip so much, I decided to write a WordpPress Plugin for it. Enjoy!

 * \[GitHub Project Page](http://github.com/kennethreitz/async\-google\-analytics\-wordpress\-plugin)
* \[Direct WordPress Plugin](http://github.com/kennethreitz/async\-google\-analytics\-wordpress\-plugin/zipball/master)

> **Analysis**: The creation of a WordPress plugin demonstrates Kenneth's pattern of sharing useful code with the broader community through open-source contributions. This early GitHub project shows his understanding that valuable code snippets should be packaged and distributed for others to benefit from, a philosophy that would define his later approach to Python package development.

  