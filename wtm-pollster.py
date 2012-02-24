#!/usr/bin/env python

import hashlib
import fileinput
import re
import json

nodename = "access_point_1"
salt = "a8dn28dm3187"


for line in fileinput.input():
    datapoint = {'metric': 'SignalStrength', 'tags': {'NodeName': nodename}}
    tcpdump = line.split(' ')

    datapoint['timestamp'] = float(tcpdump[0])
    datapoint['value'] = int(re.sub('dB', '', tcpdump[8]))
    
    for field in tcpdump:
        if field.startswith('BSSID:'):
            datapoint['tags']['BSSIDHash'] = hashlib.md5(re.sub('BSSID:', '', field) + salt).hexdigest()
        if field.startswith('DA:'):
            datapoint['tags']['DAHash'] = hashlib.md5(re.sub('DA:', '', field) + salt).hexdigest()
        if field.startswith('SA:'):
            datapoint['tags']['SAHash'] = hashlib.md5(re.sub('SA:', '', field) + salt).hexdigest()

            
            

    print json.dumps(datapoint)
                             
                          
