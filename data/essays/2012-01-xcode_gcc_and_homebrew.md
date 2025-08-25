# Xcode, GCC, and Homebrew

   # Open source is incredible.

     Several months ago, I got fed up with having to download Xcode to build my software. I took the Xcode installer, ripped out all of the parts I didn’t need, and made a nice installer for GCC. It ended up being \~200MB in size. It took 2 minutes to download.

 [OSX\-GCC\-Installer](https://github.com/kennethreitz/osx-gcc-installer/) was born.{{< sidenote >}}This project became essential for Mac developers who needed GCC without the massive Xcode download. It predated Apple's official Command Line Tools and filled a crucial gap in the developer ecosystem, particularly for Homebrew users.{{< /sidenote >}} Perfect.

 Unfortunately, I couldn’t include the 10\.6/7 SDKs due to [licensing restrictions](http://www.amazon.com/gp/product/0596517963/ref=as_li_ss_tl?ie=UTF8&amp;tag=bookforkind-20&amp;linkCode=as2&amp;camp=1789&amp;creative=390957&amp;creativeASIN=0596517963). These SDKs include CoreAudio, CoreData, OpenGL, and more. Most software that isn’t build specifically for OSX would build perfectly. Unfortunately, some software added some needless system dependencies, though (I’m looking at you, Node).

 I stuck it up on GitHub, and much to my delight, it became a pretty big hit. It solved a lot of headaches for a lot of people.

 Today, the project has 1649 watchers on GitHub and has been downloaded 53,400 times. That’s **13\.7 Terabytes** of transfer. Thanks, GitHub, for the generous hosting.

 Homebrew did their best to support the project, but the official stance was “if you buy a Mac, you buy the whole package”, pointing everyone to install full Xcode if they had any problems. Far from ideal, but I was content.

 ## Apple’s Interest

 Meanwhile, Apple reached out to me to discuss some details about OSX\-GCC\-Installer.{{< sidenote >}}This direct engagement from Apple was remarkable - a grassroots developer project had grown influential enough to prompt official corporate attention and ultimately change how Apple distributed development tools.{{< /sidenote >}} They took an interest in shipping something official, but they weren't sure of the proper approach to take to support projects like Homebrew.

 I hopped on the phone, explained the specific needs of Homebrew, the restrictions with the proprietary headers and licensing, and what the ideal situation would be.

 Months passed and I didn’t hear anything. Until today.

 ## Command Line Tools for Xcode

 Today, Apple added a beautiful new package to their official developer tools suite:**Command Line Tools for Xcode.** It’s a 171 MB download that includes all of the tools a Homebrew should ever need. Best of all, it contains the proprietary headers that I couldn’t ship myself.

 You can [download and try it out](http://developer.apple.com/downloads) today. All you need is a free Apple ID.

 You’ll want to uninstall Xcode first:

 
```
$ sudo /Developer/Library/uninstall-devtools —mode=all
```
 Major props to Apple for making this happen.

 ## The Future

 This is an incredible day for the Homebrew community. You can now setup a complete OS X develop environment with a single 171\.7 MB package download. It’s official. It’s legal. It’ll be maintained.

 Homebrew is going to officially support the package too.

 Max Howell:

 
> To stave off further questions, yes, you can use the “Command Line Tools for Xcode” package with Homebrew. And we will support it.

 Mike McQuaid:

 
> We will recommend you don’t use Xcode from the App Store but instead the command\-line\-tools package (which can also be installed from inside of Xcode and lives happily alongside it).

 Open source is incredible.

     