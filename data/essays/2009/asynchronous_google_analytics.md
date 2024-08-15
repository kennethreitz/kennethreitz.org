# Asynchronous Google Analytics!

  Google Analytics now supports Asyncronous loads, which allow the browser to continue loading content while **ga.js** is being loaded. Now it's safe to put the script tag in the  `<head>` for you XHTML STRICT junkies. 

 **Here's the new code to do so:**

  var \_gaq \= \_gaq \|\| \[];\_gaq.push(\['\_setAccount', 'UA\-XXXXX\-X']);\_gaq.push(\['\_trackPageview']);

  (function() {var ga \= document.createElement('script');ga.src \= ('https:' \=\= document.location.protocol ?'https://ssl' : 'http://www') \+'.google\-analytics.com/ga.js';ga.setAttribute('async', 'true');document.documentElement.firstChild.appendChild(ga);})();

 \#\# WordPress Plugin UpdateI love this new code clip so much, I decided to write a WordpPress Plugin for it. Enjoy!

 * \[GitHub Project Page](http://github.com/kennethreitz/async\-google\-analytics\-wordpress\-plugin)
* \[Direct WordPress Plugin](http://github.com/kennethreitz/async\-google\-analytics\-wordpress\-plugin/zipball/master)

  