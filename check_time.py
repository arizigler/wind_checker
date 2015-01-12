#!/usr/bin/env python


import datetime

import sys

now = datetime.datetime.now()
t8am = now.replace(hour=8, minute=0, second=0, microsecond=0)
t6pm = now.replace(hour=18, minute=0, second=0, microsecond=0)

if (now < t8am or now > t6pm):
    print 1
    exit(1)
exit(0)

