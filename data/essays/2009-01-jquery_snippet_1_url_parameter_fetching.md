# jQuery Snippet #1: URL Parameter Fetching

*2009 Technical Context: This was the era before URLSearchParams API (2016) and modern URL parsing libraries. Manual string manipulation was the standard approach for extracting query parameters.*

  I've decided to provide you with a new data stream. The jQuery Snippet of the Week. Enjoy.

  // Read a page's GET URL variables and return them as an associative array.function getUrlVars(){var vars \= \[], hash;var hashes \= window.location.href.slice(window.location.href.indexOf('?') \+ 1\).split('\&');for(var i \= 0; i \< hashes.length; i\+\+){hash \= hashes\[i].split('\=');vars.push(hash\[0]);vars\[hash\[0]] \= hash\[1];}return vars;}

*Technical Analysis: This implementation has several limitations by modern standards: no URL decoding, doesn't handle array parameters, and lacks error handling. However, it demonstrates the pragmatic jQuery-era approach to DOM manipulation and utility functions.*

 When executed, this function will return a beautiful string\-indexed array of your hacking pleasures.

*Community Attribution: The acknowledgment of Roshambo and jQuery HowTo reflects the collaborative nature of early web development communities, where code sharing through snippet libraries was essential for knowledge transfer.*

 Thanks, [Roshambo](http://snipplr.com/users/Roshambo/) and [jQuery HowTo](http://jquery-howto.blogspot.com/)!

  