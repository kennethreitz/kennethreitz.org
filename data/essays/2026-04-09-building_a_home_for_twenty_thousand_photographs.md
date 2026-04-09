# Building a Home for Twenty Thousand Photographs

*April 2026*

Three days ago I wrote about [sixty thousand images and nowhere to put them](/essays/2026-04-06-sixty_thousand_images_and_nowhere_to_put_them). The essay was a lament — a meditation on creative work without a platform, on the death of photo-sharing communities, on the gap between having a body of work and having a place for it to live.

Then I built the place.

**[photos.kennethreitz.org](https://photos.kennethreitz.org)** is live. Twenty thousand photographs, organized by camera, lens, city, year, and AI-generated tags. Every image has EXIF metadata extracted, GPT-4o-generated titles and descriptions, and is discoverable through the gear that made it. The whole thing was built in a single extended session with Claude — from empty Django project to deployed production site with infinite scroll, a photo manager, and a word cloud of three thousand tags.

I want to talk about how it works, because the architecture reveals something interesting about where software is going.

## The Stack

![](/photography/random/L1006175.jpg)

The foundation is Django 6 on Python 3.14, deployed on Fly.io. PostgreSQL for data and as the Celery broker (no Redis in production — one less service to manage). Tigris for S3-compatible object storage. HTMX for interactivity. Vanilla JavaScript only where absolutely necessary — drag-and-drop upload, the photo manager's multi-select.

No frontend framework. No React, no Vue, no build step. Django templates render HTML, HTMX handles infinite scroll, the browser does the rest. This is a deliberate choice rooted in the same philosophy that drove Requests: match the mental model. A photography site should feel like looking at photographs, not like operating a web application.

The server renders pages. The browser displays them. Scroll down, more images appear. Click one, see it large with its EXIF data. That's it. The complexity lives in the pipeline, not the presentation.

## The Pipeline

Every image that enters the system passes through a ten-step pipeline:

1. Validate format and size
2. Extract EXIF metadata
3. Normalize camera and lens names (because EXIF strings are chaos — "NIKON CORPORATION NIKON D850" and "Nikon D850" need to resolve to the same canonical record)
4. Compute a perceptual hash for visual deduplication
5. Generate three thumbnail sizes
6. Create the EXIF data record with the raw JSON preserved
7. Reverse geocode GPS coordinates to a city (offline, using a local dataset — no API rate limits)
8. Apply cleanup rules (delete images from certain dates, clear incorrect EXIF timestamps, block GPS coordinates from countries I've never visited)
9. Mark as processed
10. Dispatch an async AI description task

Steps 1-9 happen synchronously during upload. Step 10 fires off a Celery task that sends the thumbnail to GPT-4o-mini and gets back a structured JSON response: an artistic title, a two-sentence description, and five to ten tags.<label for="sn-structured" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-structured" class="margin-toggle"/><span class="sidenote">OpenAI's structured output with JSON schema enforcement means the response is always valid JSON with exactly the fields you need. No parsing hacks, no "please respond in JSON" prompting. The schema is the contract.</span>

The cleanup rules are the part I'm most proud of, architecturally. They're defined in two places — a management command for batch operations, and inline in the pipeline for real-time enforcement. Delete rules remove images from years with bad data. Fix rules clear incorrect timestamps. Privacy rules make certain dates private. City rules block GPS coordinates that geocode to countries I've never been to (bad EXIF data from camera clock drift, not actual travel). The same rules apply whether you're importing ten thousand images from a hard drive or uploading one from the web interface.

## The AI Layer

Every photograph gets an AI-generated title, description, and set of tags. The titles are short and evocative — "Golden Hour Over the Valley", "Urban Geometry in Shadow", "Whispers of the Waterfront". The descriptions are two to three sentences. The tags are single lowercase words: *architecture*, *shadow*, *reflection*, *monochrome*, *street*.

This matters more than it might seem. My Flickr exports had filenames like "Pro Photos - 7025 of 11810.jpeg". The original Leica files were "L1006175.jpg". Neither tells you anything about what's in the image. The AI layer transforms an archive of opaque filenames into a searchable, browsable, discoverable collection.

The tag cloud alone — three thousand tags, sized by frequency, filterable as you type — turns the archive from a chronological dump into something you can explore by subject. Click *cobblestone* and see every street I ever walked on with interesting ground. Click *silhouette* and see a decade of figures against light.

Search spans titles, AI descriptions, and tags simultaneously. Type "rain" and you get every image the AI recognized rain in, across every camera and city and year. That's not something I could have built by hand with twenty thousand images.

## The Import

The bulk import command (`import_folder`) was the workhorse. Point it at a directory, it recurses through subdirectories, hashes each file against the database to skip duplicates, uploads originals to Tigris, and dispatches processing. A single worker doing one image at a time, because the remote Postgres can't handle concurrent connections over a Fly proxy without exhausting the connection pool.

The auto-skip is smarter than it looks. It preloads all existing filenames from the database in a single query, normalizes them (spaces to underscores, case-insensitive), and skips matches instantly — no disk I/O required for known images. Only genuinely new files get hashed. For a re-run against twenty thousand existing images and a few hundred new ones, the skip phase takes seconds.

Perceptual deduplication catches what content hashing misses. Two different exports of the same photograph — one from Flickr at 1600px, one from the original at full resolution — have different SHA-256 hashes but nearly identical perceptual hashes. The deduplication pass compares hamming distances and removes the duplicate while preserving collection memberships, tags, and AI metadata on the surviving copy.

## The Geography

GPS coordinates in EXIF data are a gift and a curse. A gift because they let you build a browsable map of everywhere you've ever photographed. A curse because camera clocks drift, and suddenly you have sixty photographs allegedly taken in western China when you were actually in Virginia.

The solution is a four-level filter. The `City.from_coordinates()` method rejects coordinates that geocode to countries on an exclusion list. The processing pipeline checks the same list. The geocode management command skips them during batch operations. And the cleanup command catches anything that slipped through. Four independent checks, same list, same result. Belt, suspenders, and two extra belts.

India required special handling — I've actually been to Bangalore and Mysore, so the filter allows those cities while rejecting everything else in the country. Substring matching, because the reverse geocoder returns "Bangalore Urban" as the admin2 region, not "Bangalore" as the city name.

The cities page groups locations by continent, country, and state (for the US), with an interactive dark-themed map showing gold markers sized by image count. Click a marker, see the city name and a link to browse its photos. It's the kind of feature that makes the archive feel *alive* — not just a collection of images but a map of a life.

## What I Learned

The most interesting thing about this project isn't the technology. It's what happens when you give twenty thousand photographs AI-generated metadata and make them searchable.

Patterns emerge that I never saw in fourteen years of shooting. The AI notices things I didn't — recurring compositional tendencies, subjects I'm drawn to unconsciously, a bias toward certain kinds of light that I wasn't aware of until I could search for it. The tag cloud is a mirror. It shows you what you see when you look at the world.

Photography is seeing. Software is building tools for seeing. This project sits at the intersection — a tool I built to see my own seeing, organized by the instruments that made it possible.

The sixty thousand images have a home now. Not all of them — cleanup rules and curation brought the public count to around twenty thousand — but the ones that matter. Browsable by [camera](https://photos.kennethreitz.org/cameras/), [lens](https://photos.kennethreitz.org/lenses/), [city](https://photos.kennethreitz.org/cities/), [year](https://photos.kennethreitz.org/years/), and [tag](https://photos.kennethreitz.org/tags/). Every image discoverable. Every photograph findable by the gear that made it or the subject it captured.

The platform I was looking for didn't exist. So I built it.

---

*The site is live at [photos.kennethreitz.org](https://photos.kennethreitz.org). The code is at [github.com/kennethreitz/photos.kennethreitz.org](https://github.com/kennethreitz/photos.kennethreitz.org).*
