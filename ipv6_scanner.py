#! /usr/bin/python3

import simPing as ping

# Part 1: verify seeds

# Actual file '/datadrive/homework/scanner-seeds.txt'
seed_file_name = '/datadrive/homework/scanner-seeds-small.txt' 
seed_list = open(seed_file_name, 'r').readlines()

sp = ping.initialize()

# ping each seed
for i in seed_list:
    ip = i.rstrip('\n')
    active = ping.ping(sp, ip)

    if not active:
        print('Error: Seed ' + ip + ' is not active')
        exit(1)



