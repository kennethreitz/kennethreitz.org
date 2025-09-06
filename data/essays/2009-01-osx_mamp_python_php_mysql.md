# OSX + MAMP + Python + PHP + MySQL
*January 2009*





If you're a web developer who uses MAMP in conjunction with anything other than PHP, I'm sure you've had quite a large bit of frustration involving multiple MySQL instances.

Not any more! This simple chain of commands will save you days upon days of troubles:

```bash
$ sudo rm /tmp/mysql.sock
$ sudo ln -s /Applications/MAMP/tmp/mysql/mysql.sock /tmp/mysql.sock
```

I only wish I had found this sooner.

Enjoy.