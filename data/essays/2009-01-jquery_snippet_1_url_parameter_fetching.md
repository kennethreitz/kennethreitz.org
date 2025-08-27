# jQuery Snippet #1: URL Parameter Fetching

*2009 Technical Context: This was the era before URLSearchParams API (2016) and modern URL parsing libraries. Manual string manipulation was the standard approach for extracting query parameters.*

  I've decided to provide you with a new data stream. The jQuery Snippet of the Week. Enjoy.

  // Read a page's GET URL variables and return them as an associative array.function getUrlVars(){var vars \= \[], hash;var hashes \= window.location.href.slice(window.location.href.indexOf('?') \+ 1\).split('\&');for(var i \= 0; i \< hashes.length; i\+\+){hash \= hashes\[i].split('\=');vars.push(hash\[0]);vars\[hash\[0]] \= hash\[1];}return vars;}


 When executed, this function will return a beautiful string\-indexed array of your hacking pleasures.


 Thanks, [Roshambo](http://snipplr.com/users/Roshambo/) and [jQuery HowTo](http://jquery-howto.blogspot.com/)!

  
