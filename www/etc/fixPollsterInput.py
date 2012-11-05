#!/usr/bin/env python
'''
Simply prints out the number of messages in the queue
'''

import boto
import boto.sqs
import json
import re
import sys
from boto.s3.key import Key

try:
    file = open(sys.argv[1])
except (IOError,IndexError):
    print "\nWhen invoking "+sys.argv[0]+", please pass correct file path to jobflow description"
    raise
cfg=json.load(file)
argslist = cfg[0]['HadoopJarStep']['Args']

findQueue = re.compile("SQS_QUEUE=[.]*")
findRegion = re.compile("SQS_REGION=[.]*")
queueName = "".join(filter(findQueue.match, argslist)).rsplit("=")[1]  # Get name of input queue by parsing the JSON jobflow description
queueRegion = "".join(filter(findRegion.match, argslist)).rsplit("=")[1] # Get region by parsing the JSON jobflow description

NUMBER_OF_MAPPERS = 10 #TODO: Don't hardcode this
sqs_conn=boto.sqs.connect_to_region(queueRegion)
q=sqs_conn.get_queue(queueName)
num_messages = int(q.get_attributes()['ApproximateNumberOfMessages']) # Get the number of messages in the queue

s3_conn=boto.connect_s3()
bucket = s3_conn.get_bucket('pollster-emr') #TODO: Don't hardcode this?
keyList=bucket.list(prefix="input") # Get input directory
bucket.delete_keys([key.name for key in keyList])  # Delete contents of input directory

# Collect a number of messages divisible by the number of mapper tasks
num_messages_to_collect = NUMBER_OF_MAPPERS + (num_messages - (num_messages % NUMBER_OF_MAPPERS))


k = Key(bucket)
# Write the input files, which determine the number of mapper tasks
for x in range(NUMBER_OF_MAPPERS):
    # Fill input file with garbage string -- it's only there so that Hadoop correctly invokes the mapper script
    k.key='input/file'+str(x)
    k.set_contents_from_string('asdf')

print str(num_messages_to_collect) + "\t" + str(NUMBER_OF_MAPPERS)
