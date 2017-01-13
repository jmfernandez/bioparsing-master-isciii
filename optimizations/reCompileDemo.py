#!/usr/bin/env python

import re
import time

line="En un lugar de la mancha de cuyo nombre no quiero acordarme"
numtimes = 1000000

print "Demo removing {0} times the spaces from '{1}'".format(numtimes,line)

before = time.time()
for num in range(numtimes):
    line2 = re.compile(r"\s+").sub('',line)
after = time.time()

print "Compiling always took ",after-before," seconds"

before = time.time()
expr = re.compile(r"\s+")
for num in range(numtimes):
    line2 = expr.sub('',line)
after = time.time()

print "Compiling once took ",after-before," seconds"
