#!/bin/bash


# Source these so crontab doesn't fail
source /home/ubuntu/.bashrc
source /home/ubuntu/izitbz.sh

cd /home/ubuntu/izitbz
IZITBZ_DATE=`date "+2012-%h-%d-%H-%M"`
export IZITBZ_DATE
JOBFLOW_DESCRIPTION="izitbz.json"
POLLSTER_CFG=$(./etc/fixPollsterInput.py "${JOBFLOW_DESCRIPTION}") # Get number of messages to collect and number of mapper tasks to set
NUM_MESS=$(echo -e "$POLLSTER_CFG" | cut -f 1)
NUM_TASKS=$(echo -e "$POLLSTER_CFG" | cut -f 2)

echo "Collecting ${NUM_MESS} messages across ${NUM_TASKS} map tasks"

echo "Writing Isitbusy output to s3://isitbusyout/output/${IZITBZ_DATE}"
if [ "$1" = "up" ]; then
    if [ "${JOBFLOWID}" = "" ]; then
        echo "WARNING: JOBFLOWID variable not set"
        JOBFLOWID=$(/usr/local/bin/elastic-mapreduce --list --active | grep j | cut -d" " -f 1)
        export JOBFLOWID
        echo "Attempting to use ${JOBFLOWID}..."
    fi
    /usr/local/bin/elastic-mapreduce --jobflow ${JOBFLOWID} --json ${JOBFLOW_DESCRIPTION} --param "<date>=${IZITBZ_DATE}" --param "<nummess>=${NUM_MESS}" --param "<mappers>=${NUM_TASKS}" --param "<sdbDomain>=${SDB_DOMAIN}"

else
    /usr/bin/s3cmd put install-depends.sh s3://isitbusydev/install-depends.sh
    /usr/bin/s3cmd put izitbz-map.py s3://isitbusydev/izitbz-map.py
    /usr/bin/s3cmd put izitbz-red.py s3://isitbusydev/izitbz-red.py
    JOBFLOWID=$(/usr/local/bin/elastic-mapreduce --create --stream --alive --json ${JOBFLOW_DESCRIPTION} --param "<date>=${IZITBZ_DATE}" --param "<nummess>=${NUM_MESS}" --param "<mappers>=${NUM_TASKS}" --param "<sdbDomain>=${SDB_DOMAIN}" --bootstrap-action s3://isitbusydev/install-depends.sh --instance-type "m1.large" | cut -d" " -f 4)
    export JOBFLOWID
    echo "New jobflow $JOBFLOWID"
fi
