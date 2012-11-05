This is a Is-It-Busy drone written in Lua, tested on a WRT54GL (v1.1) running dd-wrt.

# What will it do?

When the drone is running, it will count unique MAC addresses and write the number of unique addresses to an SQS queue in the cloud.

# Dependencies

This client was tested in the following environment:
* Linksys WRT54GL v1.1
* dd-wrt v24 (mini generic build)
* lua version 5.0.2
* wget version 1.11

Note that running the `wtm-configure-env.sh` script described below will try to install the necessary software dependencies for you.

# Install

1. Install [`dd-wrt`](http://dd-wrt.com/site/index) on a router
1. Place router into Wireless Client mode, and connect the router to an access point with Internet access
1. Enable SSH access/administration and enable the JFFS2 partition
1. Run `scp -r . root@<router-IP-address>:'
1. SSH into the router
1. `cd' into 'wtm-router', run `source ./wtm-configure-env.sh' and IGNORE ALL ERRORS FROM `ipkg' (seriously!)

# Upgrade

When overwriting a prior install of the drone, run the following commands before commencing with the above Install instructions:
```
$ rm -rf /jffs/usr/*
$ reboot
```

# Todo

* Test router's ability to perform with a wired Internet connection for communicating with AWS

# Notes

Because the client's dependencies take up more space than is available in the WRT's nonvolatile memory, it is necessary to install everything but the client itself to RAM. `wtm-configure-env.sh' takes care of this, and will re-install all the dependencies and start the client at each reboot.

The packet sniffer is a custom C program based off of Wi-viz (http://devices.natetrue.com/wiviz/), which can be found in the `wiviz-src/` directory.
