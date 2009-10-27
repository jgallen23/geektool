#!/usr/bin/env python
import sys
import imaplib

email = sys.argv[1]
password = sys.argv[2]

imap = imaplib.IMAP4_SSL("imap.gmail.com", 993)
imap.login(email, password)

count = imap.select("[Gmail]/Starred")[1][0]

print "Starred Email: %s" % count


