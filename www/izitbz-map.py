#!/usr/bin/env python
import fileinput
import simplejson as json

MINUTES_PER_TIME_INT = 15 # The number of minutes to consider a single, independent time interval
datapoint = {}
routers={}

def getTimeInt(timestamp):
    '''Return the correct time interval for this timestamp'''
    timeint = MINUTES_PER_TIME_INT * 60 # Number of seconds in 15 minutes
    interval = timestamp - (timestamp % timeint)
    return interval

def fillRouterDict(dp):
    '''Parse out info from datapoint, and sort it into routers dictionary'''
    try:
        beacon=dp['NodeName']
    except KeyError:
    # print not valid izitbz input
        return
    time_interval=getTimeInt(dp['timestamp'])
    sa=dp['SA']

    if beacon in routers:
        if time_interval in routers[beacon]:
            if sa not in routers[beacon][time_interval]: # Only add SA to list if it is not already there
                routers[beacon][time_interval].append(sa) 
        else:
            routers[beacon][time_interval]=[sa]
    else:
        routers[beacon]={}
        routers[beacon][time_interval]=[sa]

for line in fileinput.input():
    try:
        datapoint=json.loads(line)
    except ValueError:
        # print "Line not valid JSON"
        continue
    fillRouterDict(datapoint)

print json.dumps(routers)
