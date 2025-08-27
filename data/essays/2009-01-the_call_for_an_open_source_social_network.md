# The Call for an Open Source Social Network
*January 2009*





  Lately, I've been tossing some ideas around that I feel would benefit the Social Web as a whole. It’s been going through some rough times lately, and I think it’s time for a change. Or so I thought.My first idea was to create a site that was rather decentralized, allowing all of your content to exist on other sites, but still allowing for you to interact without locking a user in. As it turns out, this site already exists. It is called [FriendFeed](http://friendfeed.com/kennethreitz). *[I love FriendFeed](http://kennethreitz.com/blog/friendfeed-is-awesome/)*. About a week after I decided that I wanted to get into it, [Facebook decided to purchase it](http://kennethreitz.com/blog/friendfeed-is-awesome/). How sad. They claim that it will still be up and running, but we’ll see if that proves to be the case (I have my fingers crossed). Pownce (which was powered by Python / Django) was shut down when it was purchased. I pray this not be the case.

 Think about this now: **Why is that even an option**? Social networking is all about community and building tribes – So why do we need to have an organization in charge of our chosen communication platform?<label for="sn-decentralization" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-decentralization" class="margin-toggle"/><span class="sidenote">Kenneth was advocating for decentralized social networks over a decade before they became mainstream concerns. His vision anticipated the problems of platform lock-in, data ownership, and corporate control that would later drive interest in Mastodon, ActivityPub, and other federated protocols.</span>

 **Here is my proposal**: Create a community\-driven, community\-developed, and community\-controlled social networking site that is truly open source.

 The community could take care of everything from feature development to content control. No random shutting down, buy\-outs, or merges. No more random change of Privacy Policies or Content Ownership battles. No more worries. The only group of people who would be benefitted would be the community itself, not some company. An open minded network full of open minded people working for the better of the community.

  # The Open Web of Flow

 ### **Step One**: Solid Platform Choice

 The platform choice is the most important. You've seen what happens when the wrong tool is chosen for the job: look at Twitter: Bad Planning.<label for="sn-twitter-scaling" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-twitter-scaling" class="margin-toggle"/><span class="sidenote">The "Fail Whale" era of Twitter (2008-2010) became a cautionary tale about scaling web applications. Kenneth's criticism was spot-on—Twitter's early Ruby on Rails architecture struggled with growth, leading to frequent outages. His advocacy for Python would prove prescient as Twitter eventually rewrote much of their infrastructure.</span> We're all familiar with the Fail Whale but we shouldn't. At all. So what do we use? There's an array of options. .NET? HAHA! Did you know that there's even [a social platform built on top of Microsoft's Sharepoint](http://membertomember.com/)? I bet you didn't. I've installed it a number of times. It's fantastic (for people who need it). But we don't. At all. What type of open source project aside Mono is driven by NET developers anyway? They are in an entirely different mindset than us. Anyway, the answer is obvious: Django on a LAMP Stack (Linux \+ Apache \+ MySql \+ Python). We can all agree that Python is freaking amazing.<label for="sn-python-advocacy" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-python-advocacy" class="margin-toggle"/><span class="sidenote">Kenneth's early and passionate advocacy for Python reflects his deep understanding of developer experience and community values. His mention of Google's "unladen swallow" project (an attempt to speed up Python) shows he was tracking cutting-edge developments in the Python ecosystem.</span> And it's certianly not going anywhere any time soon. I think google has proven time\-and time again that Python is the language for just about any job. And when Google's unlayden\-swallow project is complete, all (typically negligible) performance issues will be eliminated. Done.

 ### **Step Two**: Basic Information Architecture

 We need to decide how the whole system will work. FriendFeed has an excellent system in place. Lets use it. Users can tie everything in from all of their other websites and steam it on their profile, and display it all on one page. Everything's streamlined, commentable, hookable, and readily accessible. Google Profiles rock. But that is definitely an abandoned project. Lets mix that with a FriendFeed\-style activity stream. Done.

 ### **Step Three**: Sustainability, Audience, and Accessibility

 How will we pay for it? How will we get people to contribute? How will be get people to use it? Answer: Twitter is getting old and it's getting old fast. It's time for something new. Lets blow them away and they will ALL hop on board. Allow for easy external\-account migration and account creation and we'll be golden.

 ### **Step Four**: Technical Planning and Engineering

 This is all the stuff end users don't have to worry about. Performance. Design. System Administration. Database Engineering. The geek stuff. I mean come on guys, how awesome would it be to be able to make a commit to the Twitter live SVN Branch? Epically awesome.

 ### **Step Five**: Community \+ Collaboration

 Once the community gets going, there will be no stopping it.

 In conclusion, think about what we have to lose? Are you with me?<label for="sn-prophetic-vision" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-prophetic-vision" class="margin-toggle"/><span class="sidenote">Kenneth's call for an open source social network was remarkably prescient. While his specific technical vision (Django on LAMP) reflected 2009 thinking, his core insights about community ownership, decentralization, and the problems of corporate-controlled social media platforms anticipated issues that wouldn't become mainstream concerns until the 2010s and beyond.</span>

  