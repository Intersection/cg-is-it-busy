# Is It Busy?

Is It Busy is a method for determining how "busy" or "active" a space is based on the number of unique Wi-Fi devices in the air at any given point in time.

# How does it work?

1. Every five minutes, a router updates an Amazon SimpleDB domain with the number of unique MAC addresses it counted for that time interval
1. A webapp tells you whether or not it is more or less "busy" than average for that router, based on how many unique addresses the router counted

# Router drone

Refer to the `router-drone` directory for router drone source code.

# Web interface

Refer to the `www` directory for web interface source code.
