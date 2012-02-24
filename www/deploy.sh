#!/bin/bash

# Updates server with the latest codebase.

INSTANCE=$(ec2-describe-instances | grep -A4 izitbz | grep running | cut -f2)
FILENAME="controlgroup.tar.gz"
echo "WARNING -- going to terminate izitbz EC2 webserver $INSTANCE!"

git archive --output $FILENAME master
s3cmd put $FILENAME s3://isitbusydev/src/$FILENAME
rm $FILENAME

ec2-terminate-instances $INSTANCE
