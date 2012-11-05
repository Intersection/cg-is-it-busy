#!/usr/bin/env python
import fileinput
import boto
import simplejson as json
import time
import os

datapoint = {}
merged_input = {}

sdb_name=os.environ['SDB_DOMAIN']
sdb_conn=boto.connect_sdb()
db=sdb_conn.get_domain(sdb_name) # Connect to the Izitbz SimpleDB domain

def pad_count(count):
    '''
    Prefix the MAC address "count" for each db entry so that each count attribute is of consistent length,
    in order to be compatible with SimpleDB's lexicographical comparisons
    '''

    final_num_digits = 8 # The number of digits the output string should contain
    digs=len(str(count))
    prefix=''
    for x in range(final_num_digits - digs):
        prefix = prefix+'0'
    return prefix+str(count)

for line in fileinput.input():
    try:
        datapoint=json.loads(line)
    except ValueError:
        # print "Line not valid JSON"
        continue
    for beacon in datapoint:
        for time_int in datapoint[beacon]:
            if beacon not in merged_input:
                merged_input[beacon] = {}
            if time_int not in merged_input[beacon]:
                merged_input[beacon][time_int]=datapoint[beacon][time_int]
            else:
                merged_input[beacon][time_int]=list(set(merged_input[beacon][time_int]).union(set(datapoint[beacon][time_int]))) # Merges the latest datapoint with existing lists of addresses per time interval per node


for beacon in merged_input:
    for time_int in merged_input[beacon]:
        time.sleep(.05)
        count = len(merged_input[beacon][time_int]) # Count the number of MAC addresses in the list 
        item_str = beacon+'-'+time_int
        item = db.get_item(item_str)

        # If db entry doesn't exist, create it
        if not item:
            item=db.new_item(item_str)
            item['base_station'] = beacon
            item['time_int'] = time_int
            item['count'] = pad_count(count)
        # Update db value if the latest count is bigger
        elif count > int(item['count']):
            item['count'] = pad_count(count) # If our count is bigger than the existing, it is more up to date
         # If the db entry is already up to date, move on
        else:
            continue

        item.save() # commit changes to SimpleDB
