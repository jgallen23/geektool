#!/usr/bin/env python
import feedparser
import sys

rss_feed = sys.argv[1]

d = feedparser.parse(rss_feed)

print "%s %s" % (d.feed.title, len(d['entries']))


