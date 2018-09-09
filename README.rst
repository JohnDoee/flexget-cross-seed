Flexget Cross Seeding
=====================

This plugin can check your local files to see if it matches anything found by Flexget.

Installation
------------

Download `cross-seed.py` and put it in the. `~/.flexget/plugins/` folder. If the folder does not exist, create it.

Usage
-----

The new plugin works by using the filter `cross-seed` that takes a list of paths as arguments.
If the item in the RSS feed is seen in a local folder, then the torrent is downloaded.

Please note that it requires an almost exact match, e.g. `movie_1.mkv` does not match `movie_1` while `MoViE 1.mkV` matches.

Example
-------

Flexget task example:

.. code:: yaml

   example-site:
     rss: "http://example.com/rssfeed.php"
     seen: local # helpful if you have multiple feeds
     cross-seed:
       - "/data/movies/*" # movies structure is /data/movies/movie1
       - "/data/tv/*/*/*" # tv structure is /data/tv/show.name/season.1/episode1
     manipulate:
       - title:
           extract: "NEW: (.+)" # The RSS feed have some additional data we need removed
                                # i.e. the feed says "NEW: movie1"
     download: /data/torrents/example-site/
     exec: ~/autotorrent-env/bin/autotorrent -c ~/autotorrent-env/autotorrent.conf -l example-site-client -r -a /data/torrents/example-site/*.torrent

License
-------

MIT, see LICENSE
