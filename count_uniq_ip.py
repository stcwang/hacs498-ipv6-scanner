#! /usr/bin/python3

import sys

if len(sys.argv) < 2:
    print("Usage: " + sys.argv[0] + "<traceroute file>")
    exit(1)

# '/datadrive/datasets/ripe/data-store.ripe.net/datasets/atlas-daily-dumps/traceroute-2023-01-27T2300_IPv6-only.jsonl'
file = sys.argv[1]

with open(file, "r") as f:
    line = f.readline()
    while line:
        line = f.readline()