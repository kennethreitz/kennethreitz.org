# Sublime Text 3 Love
*January 2013*

I'm happy to announce that [Sublime Text 2](http://www.sublimetext.com/2) [**edit:** post valid for Sublime Text 3] was officially released today! This is awesome news. I've spend 12+ hours a day for the past year and a half in Sublime Text 2. It is indeed sublime.

## Why should you try it?

* It's light and fast.
* It's cross-platform.
* Chrome-like tabs.
* Split window layouts!
* It's not vaporware.
* It supports TextMate Bundles and Themes!
* It's fully scripted with an embedded Python interpreter, making it nicely extensible.

## Beautiful

My editor looks like this:

![](https://d233eq3e3p3cv0.cloudfront.net/max/842/0*ZE4cOiqiRGcr86wk.png)

This is comprised of a few things:

### Soda Dark Theme 

This is a nice alternative to the default "skin" of Sublime. It comes in both light and dark flavors. You can grab it [on GitHub](https://github.com/buymeasoda/soda-theme/).

### Tomorrow Night 

[Tomorrow Night](https://github.com/chriskempson/tomorrow-theme/tree/master/textmate) is my current favorite color scheme for syntax highlighting. I've cycled through around with quite a few in the past, but this one is really something special.

### Ubuntu Mono 

I'm pretty passionate about monospace typefaces. Over the years, I've been a heavy supporter of Monaco, MS Consalas, Inconsolas, Menlo, and finally Ubuntu Mono.

Simply the greatest programming font ever made. [Download it here](http://font.ubuntu.com/).

### Configuration

I've optimized my settings for Python development.

* Hidden sidebar.
* Disabled minimap.
* Disabled fold buttons.
* All whitespace drawn.
* Auto-trim trailing whitespace.
* PEP8-esque line rulers (79 for code, 72 for docstrings).

Here's my user config file:

```json
{
    "auto_complete": false,
    "close_windows_when_empty": false,
    "color_scheme": "Packages/User/Tomorrow-Night.tmTheme",
    "draw_white_space": "all",
    "find_selected_text": true,
    "fold_buttons": false,
    "font_face": "Ubuntu Mono",
    "font_options": ["subpixel_antialias"],
    "font_size": 13.0,
    "highlight_line": true,
    "rulers": [72, 79],
    "theme": "Soda Dark.sublime-theme",
    "translate_tabs_to_spaces": true,
    "trim_trailing_white_space_on_save": true,
    "folder_exclude_patterns": [".svn", ".git", ".hg", "CVS", "_build", "dist", "build", "site"]
}
```

## Tips

Here's a quick list of things that I didn't pick up on immediately when migrating from vim.

### Subl

Sublime text has nice mate-esque commandline launcher called 'subl' hidden in its distribution. To make it available universally:

```bash
$ ln -s /Applications/Sublime\ Text\ 2.app/Contents/SharedSupport/bin/subl /usr/local/bin/subl
```

Once Installed, you can run it anywhere to open a fresh project/window:

```bash
$ subl .
```

Due to muscle memory burn-in, I also recommend:

```bash
alias mate='subl -w'
```

## Shortcuts

**Shift + Command + P: Command Palette**

This nifty window pops up and gives you a list of available commands in your current context (e.g. Package Control: Install Package).

**Command + T: Go to File**

Pretty standard stuff. Jumps to the file you select.

**Command + R: Go to Symbol**

Use this to hop to any symbol definition in your current file.

**Command + P: Go to Anything**

Use this to hop to any file, symbol, or line in your current project.

## Location

On OS X, the location of the Sublime configuration is:

```
~/Library/Application Support/Sublime Text 2/
```

## Plugins

While Sublime does support Textmate Bundles, it also has a robust Python-powered plugin and extension system that allows for some very cool plugins that weren't possible with TextMate.

### Package Control

The first thing you need to install is [Package Control](http://wbond.net/sublime_packages/package_control). It's essentially Homebrew for Sublime packages. It'll save you tons of time.

### Sublime Linter

This wonderful plugin gives you instant feedback about the code you're writing, as you're writing it. It has fantastic PyLint + PEP8 support out of the box. You can install it via Package Control. Learn more [on GitHub](https://github.com/SublimeLinter/SublimeLinter).

### Sublime CodeIntel

Maintained by the same developer as SublimeLint, CodeIntel gives you IDE-style functionality with intelligent code completion, import suggestions, and go-to definition support.

It's really nice to have sometimes. I typically have it disabled. Give it a spin and see what you think. You can install it via Package Control. Learn more [on GitHub](https://github.com/Kronuz/SublimeCodeIntel).

### kCode and More

This old plugin is a remnant of my old PHP + Textmate work. If you write a lot of Python scripts, the 'env' and 'enc' snippets will save you a lot of typing:

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
```

The repo is [available on GitHub](https://github.com/kennethreitz/kcode.tmbundle).

Other great plugins available via Package Control include HTML Encode, Gist, and Restructured Text.

Happy hacking!

---

*This passion for editor optimization and development aesthetics reflects deeper themes about [programming as spiritual practice](/essays/2025-08-26-programming_as_spiritual_practice)—creating environments that support consciousness and flow state.*