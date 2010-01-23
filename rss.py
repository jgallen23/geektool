#!/usr/bin/env python
import feedparser
import sys

rss_feed = sys.argv[1]

d = feedparser.parse(rss_feed)

print "%s (%d)" % (d.feed.title, len(d['entries']))
for entry in d['entries']:
    print entry.title.encode('ascii', 'ignore')


