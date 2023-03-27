#! /usr/bin/python3

import sys
import simPing as ping
import ipv6helper as v6

# program takes in the probe budget
if len(sys.argv) < 2: 
    print("usage: " + sys.argv[0] + " <probe budget>")
    exit(1)
    
budget = int(sys.argv[1])
if len(sys.argv) == 3 and sys.argv[2] == '-t':
    test = True
else:
    test = False

# two helpers for adding and subtracting from IPs
def ip_plus(ip): 
    ind = 7
    tmp = ip
    while ind >= 0 and ip[ind] + 1 == 2**16:
        ind -= 1
    
    if ind < 0: 
        return (0,) * 8 # loop around
    
    return ip[:ind] + (ip[ind] + 1,) + (0,) * (7-ind)

def ip_minus(ip): 
    ind = 7
    tmp = ip
    while ind >= 0 and ip[ind] - 1 == -1:
        ind -= 1
    
    if ind < 0: 
        return (2**16 - 1,) * 8 # loop around
    
    return ip[:ind] + (ip[ind] - 1,) + (2**16-1,) * (7-ind)

# helper for getting network
def network(ip):
    ipnum = v6.strToV6(ip)
    return v6.v6ToStr(ipnum[:4] + (0,) * 4)

# Part 1: verify seeds

# Actual file '/datadrive/homework/scanner-seeds.txt'
seed_file_name = '/datadrive/homework/scanner-seeds-small.txt' if test else '/datadrive/homework/scanner-seeds.txt'
seed_list = open(seed_file_name, 'r').readlines()
seedset = set()

sp = ping.initialize()

# ping each seed
for i in seed_list:
    ip = i.rstrip('\n')
    active = ping.ping(sp, ip)

    if not active:
        print('Error: Seed ' + ip + ' is not active')
    else:
        seedset.add(ip)

# Part 2: generate hit list

hitlist = set()

# number of IPs around each seed, rounded up
perseed = int(budget / len(seed_list) + 1)

for s in seedset: 
    seednum = v6.strToV6(s)
    above = seednum
    below = seednum
    
    currct = 0
    split = True

    # finds the <perseed> closest addresses that have not been added to the hitlist
    while currct < perseed: 
        # we'll look at both above and below addresses 
        if (split): 
            above = ip_plus(above)
            currstr = v6.v6ToStr(above)
        else: 
            below = ip_minus(below)
            currstr = v6.v6ToStr(below) 

        split = not split 

        if currstr not in hitlist and currstr not in seedset:
            hitlist.add(currstr) 
            currct += 1
                        
# hitlist may be longer than budget, so we'll truncate it 
hitlist = list(hitlist)[:budget]

# Part 3: scan hit list
activeHitlist = set()
networks = {}

for i in hitlist:
    i_network = network(i)
    if ping.ping(sp, i):
        activeHitlist.add(i)
        if i_network not in networks:
            networks[i_network] = 1
        elif networks[i_network] != 0:
            networks[i_network] = networks[i_network] + 1

    else:
        # no response, network not aliased
        networks[i_network] = 0

# Part 4: detect aliased networks

numaliased = 0
aliasedips = 0

# if we only have a few data points, don't assume network is aliased
for n in networks: 
    if networks[n] >= 5: # we will use a cutoff of 5
        numaliased += 1
        aliasedips += networks[n]

# report results 
print("Number of probes:", budget)
print("Number of aliased networks:", numaliased)
print("Number of new non-aliased addresses found:", len(activeHitlist) - aliasedips)