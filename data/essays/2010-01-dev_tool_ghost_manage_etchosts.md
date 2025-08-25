# Dev Tool: Ghost   #manage /etc/hosts

<aside class="sidenote">
<strong>Historical Context:</strong> In 2010, managing local development environments was significantly more manual and error-prone than today. The /etc/hosts file was a critical but tedious piece of the development workflow, and Ruby's ecosystem was pioneering developer productivity tools that would later become standard across all programming languages.
</aside>

  \#\# The Ruby community has really been blowing me away lately with their array of indispensable web development tools.

 \*\*Ghost\*\* is no exception to this rule. It is a simple command line application for adding and removing 127\.0\.0\.1 entries in your \`/etc/hosts\` file. I can't believe I hadn't thought of this sooner.

<aside class="sidenote">
<strong>Developer Insight:</strong> This "why didn't I think of that?" moment captures the essence of good tooling - solving obvious pain points that developers endure daily. Ghost exemplifies the Ruby community's philosophy of creating elegant solutions to common problems, a principle that would later influence package managers and development tools across all ecosystems.
</aside> 

 \#\#\#Example Usage

  $ ghost add mydevsite.local\[Adding] mydevsite.local \-\> 127\.0\.0\.1

  $ ghost add staging\-server.local 67\.207\.136\.164\[Adding] staging\-server.local \-\> 67\.207\.136\.164

  $ ghost listListing 2 host(s):mydevsite.local \-\> 127\.0\.0\.1staging\-server.local \-\> 67\.207\.136\.164

  $ ghost delete mydevsite.local\[Deleting] mydevsite.local

 \#\#\# Installation

 
```
sudo gem install ghost
```
 

---

Yes, it's really that easy. Make sure to checkout the \[GitHub Repo](http://github.com/bjeanes/ghost) to contribute!  