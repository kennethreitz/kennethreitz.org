# Fish as Default Shell on Windows 10

  ## Step 1: Install Fish

 Because the Linux Subsystem for Windows 10 is a full Ubuntu operating system, all software packages available for Ubuntu are installable on your Windows machine now! Here's some simple steps to install the latest stable release of fish, the world's greatest shell:

 
```
$ sudo apt-add-repository ppa:fish-shell/release-2$ sudo apt-get update$ sudo apt-get install fish
```
   ![](http://images.squarespace-cdn.com/content/v1/665498111876725f7613f1e6/1719666490597-H4C46DD7OJ7U3P4B0MHC/7e2ac-e25b8-image-asset.png)![]()   ## Step 2: Make it your default shell

 Everything in the Linux Subsystem for Windows 10 is oriented around Bash, so you have to tell bash to automatically launch fish at startup, by placing the following in your `~/.bashrc`:

 
```
# Launch Fishif [ -t 1 ]; thenexec fishfi
```
 That's it! 

  