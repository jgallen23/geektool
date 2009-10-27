#!/usr/bin/env python
import feedparser
import sys

rss_feed = sys.argv[1]#'http://www.instapaper.com/rss/210994/5Da2BWwf1zMmuZMUHCfEGH9Xxk'

d = feedparser.parse(rss_feed)

print "%s %s" % (d.feed.title, len(d['entries']))


