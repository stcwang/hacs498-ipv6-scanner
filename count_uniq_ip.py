#! /usr/bin/python3

import json
import sys

if len(sys.argv) < 2:
    print("Usage: " + sys.argv[0] + "<traceroute file>")
    exit(1)

# '/datadrive/datasets/ripe/data-store.ripe.net/datasets/atlas-daily-dumps/traceroute-2023-01-27T2300_IPv6-only.jsonl'
file = sys.argv[1]
ipset = set()

with open(file, "r") as f:
    line = f.readline()
    while line:
        obj = json.loads(line)
        if "dst_addr" in obj:
            ipset.add(obj["dst_addr"])
        if "src_addr" in obj:
            ipset.add(obj["src_addr"])
        if "from" in obj:
            ipset.add(obj["from"])
        line = f.readline()

print("Number of unique IPs found:", len(ipset))
