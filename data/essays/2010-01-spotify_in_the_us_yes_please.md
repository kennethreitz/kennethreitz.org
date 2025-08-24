# Spotify in the US? Yes please.

  \#\#I spent about 8 hours last night obtaining a Premium Spotify account in the US, and I've never been happier.As you know, \[Spotify](http://spotify.com) is only available in the UK, Spain, and France. So, the only way to signup for an account it to take a trip overseas... virtually.

 \#\# Step 1: Signup for a virtual private server

 Signup for a \[Linode](http://linode.com) account, and buy a 360 VPS. Linode allows you to choose a datacenter when you buy a VPS, and luckily, they have a datacenter in the UK. This will run you $20 a month.

 \#\# Step 2: Install Ubuntu and Boot Your VPS

 Install Ubuntu Server on your new british hackbox. You can SSH in to test it out. Have fun. Make sure openssh\-server is installed. 

 \#\# Step 3: Edit Hosts FileAppend the following lines to your `/etc/hosts` file:

 
```
127.0.0.1 spotify.com127.0.0.1 www.spotify.com[your vps ip] hackbox
```
 \#\# Step 4: Open a Reverse SSH Forwarding Tunnel

 
```
sudo ssh -C root@hackbox -L 443:spotify.com:443sudo ssh -C root@hackbox -L 80:spotify.com:480
```
 Congratulations. You're now a Brit.

 \#\# Step 5: Create an Account

 While creating an account, you are prompted for you postal code. I did some \[google\-fu](http://www.google.com/search?hl\=en\&safe\=off\&client\=safari\&rls\=en\&q\=winchester\+hampshire\+office\&aq\=f\&oq\=\&aqi\=) and used `SO23 8TH` as my postal code for Winchester, Hampshire UK.

 \[Download the client](http://spotify.com/en/download/).

 \#\# Step 6: Enjoy :)

 You now have unlimited access to a library of \~8,000,000 tracks, as if they were on your own computer.

 Once every two weeks, you'll have to reopen your SSH tunnels and login at \[spotify.com](http://spotify.com) to proveyou'll be good to go.

 This restriction is lifted if you signup for a Premium account. I highly recommend this, as it allows you to listen to your music at 320 kbps. I'd tell you how, but I'd rather enjoy the fruits of my hard labor.

  