# Unix-style Windows Development Environment Adventures

  Things I've learned thus far, while developing on Windows:

![](http://images.squarespace-cdn.com/content/v1/665498111876725f7613f1e6/1719666497154-6VAFLR03ZNAAXG3QI98N/95b31-dbec8-image-asset.png)![]()   * [Cmder](http://cmder.net/) is an excellent terminal emulator, and the best one I've found for Windows. Highly recommended.
* The Ubuntu Subsystem for Windows 10 is really quite stellar \-\- It's a full\-blown Ubuntu operating system running along\-side your Windows stuff.

 Development:

 * I built Python 2\.7\.13 from source, after apt\-get installing 'build\-essential' and friends.
* The Linux home directory resides at **C:UsersUSERNAMEAppDataLocalLxsshomeUSERNAME**.
* The **C:** filesystem is available at **/mnt/c.**
* It's much better to symlink from Linux into Windows filepaths, if you plan to edit your code in both environments. If you go the other way around, lots of strange permission errors occur.

 Overall, things are going pretty well! I managed to develop and ship a release of Pipenv today on this machine, and while things weren't nearly as smooth as they are for me on a Mac, they were certianly workable!
