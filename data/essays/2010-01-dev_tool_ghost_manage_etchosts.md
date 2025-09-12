# Dev Tool: Ghost - Manage /etc/hosts
*January 2010*

## The Ruby community has really been blowing me away lately with their array of indispensable web development tools.

**Ghost** is no exception to this rule. It is a simple command line application for adding and removing 127.0.0.1 entries in your `/etc/hosts` file. I can't believe I hadn't thought of this sooner<label for="sn-obvious-solution" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-obvious-solution" class="margin-toggle"/><span class="sidenote">This "why didn't I think of that?" moment captures the essence of good tooling - solving obvious pain points that developers endure daily.</span>.

### Example Usage

```bash
$ ghost add mydevsite.local
[Adding] mydevsite.local -> 127.0.0.1

$ ghost add staging-server.local 67.207.136.164
[Adding] staging-server.local -> 67.207.136.164

$ ghost list
Listing 2 host(s):
mydevsite.local -> 127.0.0.1
staging-server.local -> 67.207.136.164

$ ghost delete mydevsite.local
[Deleting] mydevsite.local
```

### Installation

```bash
sudo gem install ghost
```

---

Yes, it's really that easy. Make sure to checkout the [GitHub Repo](http://github.com/bjeanes/ghost) to contribute!