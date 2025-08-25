# Remote TextMate Development via SSH and Rsync

  I am a huge fan of [TextMate](http://kennethreitz.com/blog/if-textmate-42/ "TextMate is God"). In my opinion, it is by far the greatest text editor ever conceived by mankind.<label for="sn-textmate-era" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-textmate-era" class="margin-toggle"/><span class="sidenote">TextMate defined the modern code editor experience with innovations like snippets, bundles, and fuzzy file searching—features now standard in editors like VS Code and Sublime Text. This 2009 perspective captures the pre-cloud development era when local tooling was paramount.</span> It has a couple of shortcomings, however. One of which is that it has no built\-in FTP or SFTP support. Remote file editing is a bit of a bear here if you like to view folders in the project drawer on the side.![](http://media.kennethreitz.com/images/textmate-logo.png)

 **Options for remote editing with TextMate:**

 * Cyberduck FTP client
* MacFUSE \+ SSHFS
* Rsync \+ SSH

 ## Cyberduck

 **The [Cyberduck](http://david.olrik.dk/files/Synchronize_remote_directory_rsync_ssh.zip) option is very very useful. While in the FTP client, you simply click "Edit in TextMate" and the client will download the file for you, open it in your editor, and – here's the awesome part – it automatically uploads the file every time you save it.<label for="sn-cyberduck-workflow" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-cyberduck-workflow" class="margin-toggle"/><span class="sidenote">This save-and-sync workflow predates modern solutions like Live Share or remote development containers, showcasing the ingenuity required for remote development before cloud-native tooling.</span> This works great when working with one file at a time. The drawback, however, is when working with large projects. Toggling between many files can be an albatross without the project drawer (cyberduck understandably doesn't allow you to edit an entier folder), so MacFUSE is the next logical choice.**

 ## MacFUSE \+ SSHFS

 [MacFUSE](http://www.pqrs.org/tekezo/macosx/sshfs/) \+ SSHFS works great, and allows you to mount an SSH folder as a mountpoint on your local system. VERY USEFUL. You can open this folder with TextMate.<label for="sn-filesystem-mounting" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-filesystem-mounting" class="margin-toggle"/><span class="sidenote">FUSE (Filesystem in Userspace) represents an elegant solution to remote development—making remote directories appear local. The performance issues described here highlight the network latency challenges that would later drive the development of more sophisticated remote development solutions.</span> This is perfect for smaller projects. However, with larger projects, this makes opening the folder in TextMate almost unbearable as it checks the status of every single file. Too slow :P

 ## Rsync \+ SSH

 **So here's the final solution: Rsync \+ SSH. This allows me to automatically sync my working copy with my server and allow for snappy file interactions without having insane latencies for starting up and bandwidth hogging!**<label for="sn-rsync-solution" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-rsync-solution" class="margin-toggle"/><span class="sidenote">Rsync's differential sync algorithm—transferring only changed portions of files—made it ideal for remote development workflows. This approach of maintaining local copies while syncing changes presaged modern distributed version control systems like Git.</span>

 To remotely sync over SSH, run the following code:

 
```
rsync -avz -e ssh remoteuser@remotehost:/remote/dir /target/dir/
```
 **Hint**: If your remote working copy is a subverson checkout, you can add 
```
--cvs-exclude
```
  into the rsync parameters, and it will exclude the ".svn" folders!



 You can then open this directory in TextMate and make all the changes you want, and then sync after ! There is also a wonderful TextMate Bundle for [Remote Rsync \+ SSH within TextMate](http://david.olrik.dk/files/Synchronize_remote_directory_rsync_ssh.zip).

 [Development](http://technorati.com/tag/Development), [OSX](http://technorati.com/tag/OSX), [rsync](http://technorati.com/tag/rsync), [TextMate](http://technorati.com/tag/TextMate)  