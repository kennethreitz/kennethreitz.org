# Announcing Httpbin.org
*January 2011*





  The development of [Requests](https://python-requests.org/), the Python HTTP Module for Humans, led to some annoying testing practices. Relying on random websites and services in order to test different capabilities of the HTTP client became annoying quickly.<label for="sn-testing-problem" class="margin-toggle sidenote-number"></label>
<input type="checkbox" id="sn-testing-problem" class="margin-toggle"/>
<span class="sidenote">This practical frustration with HTTP testing reflects a broader problem in software development: the dependency on external services makes tests fragile and unreliable. Kenneth's solution demonstrates the "scratch your own itch" principle that drives many successful open source projects.</span>[PostBin.org](http://postbin.org/) was perfect for testing POST request behavior, but is usless for other situations. I was hoping to extend its functionality to other request types, but it turns out that PostBin runs on the Google App Engine platform. No.

 Thus, [httpbin.org](http://httpbin.org/) was born.

 ## Example Endpoints

 To get a feel for what **HttpBin** does, here are a few endpoint examples:

 `$ curl http://httpbin.org/ip` :

 
```
{"origin": "::ffff:24.127.96.129"}
```
 `$ curl http://httpbin.org/user-agent` :

 
```
{"user-agent": "curl/7.19.7 (universal-apple-darwin10.0) libcurl/7.19.7 OpenSSL/0.9.8l zlib/1.2.3"}
```
 `$ curl http://httpbin.org/get` :

 
```
{"args": {},"headers": {"Accept": "*/*","Connection": "close","Content-Length": "","Content-Type": "","Host": "httpbin.org","User-Agent": "curl/7.19.7 (universal-apple-darwin10.0) libcurl/7.19.7 OpenSSL/0.9.8l zlib/1.2.3","X-Forwarded-For": "::ffff:24.127.96.129","X-Forwarded-Protocol": ""},"origin": "::ffff:24.127.96.129","url": "http://httpbin.org/get"}
```
 `$ curl -I http://httpbin.org/status/418` :<label for="sn-teapot" class="margin-toggle sidenote-number"></label>
<input type="checkbox" id="sn-teapot" class="margin-toggle"/>
<span class="sidenote">HTTP status code 418 "I'm a teapot" comes from RFC 2324, an April Fools' Day RFC about the Hyper Text Coffee Pot Control Protocol. Including this whimsical status code in HTTPBin demonstrates Kenneth's appreciation for the playful side of internet protocols.</span>

 
```
HTTP/1.1 418 I'M A TEAPOTServer: nginx/0.7.67Date: Mon, 13 Jun 2011 04:25:38 GMTConnection: closex-more-info: http://tools.ietf.org/html/rfc2324Content-Length: 135
```
 ## Moving Forward

 **HttpBin** will be packaged and released on PyPi soon, for local development use and requests\-tests runs on [ci.kennethreitz.com](http://ci.kennethreitz.com/). I need to determine a portable pattern for this.

 In the coming weeks, I'd like to add a few new new endpoints: `/deflate`, `/basic-auth`,*\&c*. Contributions are welcome.

 I'm considering adding optional request logging / history to the service, powered by Redis. A new `/post` request, for example, would be redirected to a new URL (e.g.`/post/c1548ed`) that can be POSTed to repetitively. This will give **HttpBin** feature parity with postbin.

 ## Source Code

 **HttpBin** is open source (ISC Licensed), powered by [Flask](http://flask.pocoo.org/), [Werkzeug](http://werkzeug.pocoo.org/), and good intentions.

 * [Code on GitHub](https://github.com/kennethreitz/httpbin)
* [httpbin.org](http://httpbin.org/)

  