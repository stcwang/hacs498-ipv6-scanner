#! /usr/bin/python3

import sys
import simPing as ping
import ipv6helper as v6

# program takes in the probe budget
if len(sys.argv) < 1: 
    print("usage: " + sys.argv[0] + " <probe budget>")
    exit(1)
    
budget = int(sys.argv[1])

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

# Part 1: verify seeds

# Actual file '/datadrive/homework/scanner-seeds.txt'
seed_file_name = '/datadrive/homework/scanner-seeds-small.txt' 
seed_list = open(seed_file_name, 'r').readlines()
seedset = set()

sp = ping.initialize()

# ping each seed
for i in seed_list:
    ip = i.rstrip('\n')
    seedset.add(ip)
    active = ping.ping(sp, ip)

    if not active:
        print('Error: Seed ' + ip + ' is not active')
        exit(1)

# Part 2: generate hit list

count = 0 
hitlist = set()
change = 0

# since we're rounding up, we should only need to loop more than once
# if we have seeds that are close and end up having overlapping ranges
while count < budget: 
    # number of IPs around each seed, rounded up
    perseed = int((budget - count) / len(seed_list) + 1)
    
    for s in seedset: 
        seednum = v6.strToV6(s)
        above = seednum
        below = seednum
        
        # so we'll look at new ips on a second loop 
        for _ in range(change):
            above = ip_plus(above)
            below = ip_minus(below) 
        
        for i in range(perseed): 
            # we'll look at both above and below addresses 
            if (i > perseed // 2): 
                above = ip_plus(above)
                currstr = v6.v6ToStr(above)
            else: 
                below = ip_minus(below)
                currstr = v6.v6ToStr(below) 

            if currstr not in hitlist and currstr not in seedset:
                hitlist.add(currstr) 
                count += 1
                
    change = perseed // 2 + 1

# hitlist may be longer than budget, so we'll truncate it 
hitlist = list(hitlist)[:budget]
    
# Part 3: scan hit list

# Part 4: detect aliased networks
