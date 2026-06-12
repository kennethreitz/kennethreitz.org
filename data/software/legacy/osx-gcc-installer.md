# osx-gcc-installer: A Compiler Without the 8 GB

In the early 2010s, getting a C compiler on a Mac meant downloading all of Xcode: more than 8 GB of IDE, simulators, and documentation, just to compile a Ruby gem. osx-gcc-installer packaged the compiler toolchain alone, and for a couple of years it was how a large slice of the Mac developer community got working.

## The Problem

Rails developers felt this hardest. Popular gems like `nokogiri` and `json` had native extensions that required compilation, so every new laptop and every new teammate hit the same wall: an enormous download, an Apple Developer account, and an afternoon lost to setup, all for a few hundred megabytes of actual tools.

## The Solution

Pre-built packages containing only the essentials:

- **GCC**: the GNU Compiler Collection.
- **LLVM/Clang**: Apple's preferred toolchain.
- **Command-line developer tools**: the utilities builds actually invoke.
- **DevSDK**: the headers needed to compile against the system.

It supported OS X 10.6 Snow Leopard and 10.7 Lion, the versions most developers were running. Download, install, `gem install nokogiri`, done.

The installer came with a sincere warning against mixing it with an existing Xcode installation, which could cause difficult-to-diagnose problems. Repackaging a platform vendor's toolchain is inherently a duct-tape solution. It was the right duct tape for the moment.

## The Happy Ending

Apple eventually shipped `xcode-select --install`, an official lightweight way to get the command-line tools. The project became obsolete in the best possible way: the platform absorbed the fix.<label for="sn-community-solution" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-community-solution" class="margin-toggle"/><span class="sidenote">Community tooling pressuring the platform into doing the right thing became a recurring Mac pattern: Homebrew for packages, CocoaPods for dependencies. The community builds the proof of demand, and sometimes the vendor listens.</span>

That's worth pausing on. The goal of filling a gap is to make the gap disappear, not to own it forever. Thousands of developers got productive faster for a few years, Apple noticed the demand was real, and then nobody needed my installer anymore. I count that as a complete success.

## Resources

- [Source Code on GitHub](https://github.com/kennethreitz/osx-gcc-installer): preserved for history.

## Related

- [**The Legacy Shelf**](/software/legacy): other projects that finished their work.
- [**Requests**](/software/requests): the same instinct, removing friction between developers and their work.
