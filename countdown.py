#!/usr/bin/env python
import sys
from datetime import date

label = sys.argv[1]
dt = sys.argv[2].split("/")
d0 = date.today()
d1 = date(int(dt[2]), int(dt[0]), int(dt[1]))

delta = d1 - d0
print "%s: %s" % (label, delta.days)


