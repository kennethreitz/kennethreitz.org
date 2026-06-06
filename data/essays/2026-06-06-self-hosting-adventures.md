# Self-Hosting Adventures

*June 2026*

The last essay I wrote about [mercury](/essays/2026-06-05-a_server_called_mercury) was the clean version. One evening, six sites, a tidy migration, a satisfied ending. This is the other version. The one where you keep going, because it turns out self-hosting is not a project you finish. It is a hobby you keep, and a hobby reveals itself slowly.

So here is the actual catalog. The things I am trying to accomplish, some done, some half-done, some currently on fire.

## Everything I own, on hardware I rent but control

The north star hasn't changed: anything that was living at the pleasure of a managed platform should live on the box instead. Websites first, because those were easy. Then the things that are harder and matter more.

## My photographs, twice

I run a photo site, and its library is about 166 gigabytes of originals and thumbnails. For a while it lived on a fast block-storage volume, which is the most expensive way to store cold images that has ever been devised. So I moved it to object storage, where static files belong, and watched the volume bill shrink.<label for="sn-vol" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-vol" class="margin-toggle"/><span class="sidenote">The surprise of self-hosting at any scale is that storage, not compute, is the bill. The server is lunch money. The disks are the mortgage.</span>

Separately, there is the bigger want: a copy of my entire iCloud photo library, all 839 gigabytes of it, somewhere Apple cannot lock me out of. Not because I expect to be locked out. Because the whole point of owning your data is that you no longer have to expect anything. The backup is the insurance policy against a phone call you hope never comes.

## My files, mirrored to a cheap box

iCloud Drive gets the same treatment, synced down to a storage box that costs about the price of a sandwich per month and exists purely to hold copies. The same files I already have, in a second place I control, reachable from a little web file browser at a domain I own. Redundant by design. Boring on purpose. Boring is the goal.

## My analytics, answering to no one

I used to run Gauges, a lovely little analytics product that has now been sold twice. Before that, the usual Google tag. Both are gone. Everything reports to a self-hosted dashboard now, cookieless, on my own disk, where the only party studying my traffic is me.<label for="sn-an" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-an" class="margin-toggle"/><span class="sidenote">I found two sites still quietly pinging the dead Gauges tracker weeks after I thought I'd removed it. Self-hosting does not eliminate cruft. It just makes the cruft yours to find.</span>

## My code, kept close

Twenty years of repositories, mirrored from GitHub to my own git server every few hours. GitHub remains origin, for now. The mirror is insurance, same as the photos. A pattern is forming, and the pattern is: keep a copy of everything that matters somewhere a corporation cannot reach.

## The part where it caught fire

I should be honest that none of this is smooth. While moving the photos, a backup process quietly filled the server's root disk to the last byte, which broke the orchestration layer, which took the dashboard and a couple of sites down with it. I found it, freed the space, and everything healed in minutes. No data was lost.

I keep coming back to a thing I believe about systems: the goal is not flawless, it is *recoverable*. Flawless is a fantasy you tell yourself before the incident. Recoverable is what you actually have after. A setup that breaks and heals is worth more than one you merely hope won't break, because only one of them has been tested.

## What this is really about

It is not about saving money. Add up the server and the volumes and the object storage and the boxes and it lands somewhere north of what the convenient version would cost. It is not about reliability either. A team of professionals keeps the managed platforms up better than I keep mine up at midnight in my pajamas.

It is about the difference between a tool you use and a tool you depend on. A platform you depend on can change its prices, change its owners, change its mind. A box you control can only do what you tell it, including break, which at least is honest. The adventures are the cost of that honesty, and I am finding I would rather pay it in afternoons than in trust.

The setup is never done. That is not a bug. That is the hobby.
