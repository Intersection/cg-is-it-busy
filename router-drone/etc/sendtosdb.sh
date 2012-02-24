#!/bin/sh

SIGNATURE=`openssl dgst -sha1 -hmac ${2} -binary /tmp/root/tmpfile.tmp | openssl enc -base64 | sed 's/\//\%2F/g' | sed 's/\+/\%2B/g' | sed 's/=/\%3D/g'`
/tmp/smbshare/usr/bin/wget -O - http://sdb.amazonaws.com/?${1}\&Signature\=${SIGNATURE} > /dev/null
