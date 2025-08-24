# osx-gcc-installer

This legacy project is no longer maintained, but at one point it was used by many, especially in the Rails community, to install GCC on OSX.

At the time, Apple only provided a version of GCC bundled with Xcode<label for="sn-xcode-size" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-xcode-size" class="margin-toggle"/><span class="sidenote">Xcode in the early 2010s was a massive download that included GUI tools, simulators, and documentation that most command-line developers didn't need, making it inefficient for simple compilation tasks.</span>, so every developer had to install an 8 GiB package just to get a C compiler. This project provided a lightweight alternative.

**Fun fact:** this project directly helped to inspire the `$ xcode-select --install` command<label for="sn-xcode-select-impact" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-xcode-select-impact" class="margin-toggle"/><span class="sidenote">The success and widespread adoption of osx-gcc-installer demonstrated the clear need for lightweight command-line tools, leading Apple to eventually provide this official solution that downloads only the essential development tools.</span> we all use today.

https://github.com/kennethreitz/osx-gcc-installer
