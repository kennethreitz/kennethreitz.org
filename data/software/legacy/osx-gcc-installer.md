# osx-gcc-installer

This legacy project solved a major pain point for Mac developers in the early 2010s. Before Apple provided `xcode-select --install`, installing a C compiler required downloading the entire Xcode package—an 8+ GB download that included GUI tools, simulators, and documentation that command-line developers didn't need.

## The Problem

Ruby developers, especially those using Rails with native gem extensions, needed GCC but didn't want to download gigabytes of IDE components. The Rails community was particularly affected since popular gems like `nokogiri` and `json` required compilation.

## The Solution

osx-gcc-installer provided pre-built packages containing just the essential compiler tools:

- **GCC** - GNU Compiler Collection
- **LLVM/Clang** - Apple's preferred compiler toolchain  
- **Developer CLI Tools** - Command-line utilities
- **DevSDK** - Software Development Kit headers

The installer supported OS X 10.6 (Snow Leopard) and 10.7 (Lion), targeting the versions most developers were running at the time.

## Impact

This project helped thousands of developers get productive faster. Its success demonstrated clear user demand for lightweight development tools, contributing to Apple's decision to eventually provide `xcode-select --install` as an official solution.

**Warning:** The installer explicitly cautioned against mixing it with existing Xcode installations, as this could cause "difficult-to-diagnose problems"—a lesson in the complexity of Apple's development toolchain dependencies.

## Legacy

While no longer needed thanks to Apple's official Command Line Tools, osx-gcc-installer represents an important moment in Mac development history when the community stepped in to solve tooling friction that the platform vendor hadn't yet addressed<label for="sn-community-solution" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-community-solution" class="margin-toggle"/><span class="sidenote">This pattern of community solutions influencing official platform decisions became common in the Mac development ecosystem, from package managers like Homebrew to dependency managers like CocoaPods.</span>.

https://github.com/kennethreitz/osx-gcc-installer
