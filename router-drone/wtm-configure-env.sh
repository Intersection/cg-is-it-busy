#!/bin/sh

# Run this to install the pollster client's dependencies.
# *** Make sure the router is connected to the Internet via Wireless Client Mode. This can be done through the dd-wrt web interface. ***

if [ -f /jffs/usr/etc/wtm-configure-env.sh ];
then
    sleep 20 # wait for Internet connection...
fi

original_path="$PWD"
mkdir -p /tmp/smbshare/tmp/ipkg
cd /tmp/smbshare/tmp/ipkg
wget http://downloads.openwrt.org/whiterussian/packages/libpcap_0.9.4-1_mipsel.ipk
wget http://downloads.openwrt.org/whiterussian/packages/liblua_5.0.2-1_mipsel.ipk
wget http://downloads.openwrt.org/whiterussian/packages/lua_5.0.2-1_mipsel.ipk
wget http://www.timpinkawa.net/ddwrt/ipkg/wget_1.11-4_mipsel.ipk
wget http://downloads.openwrt.org/kamikaze/8.09.2/brcm47xx/packages/libopenssl_0.9.8i-3.2_mipsel.ipk
wget http://downloads.openwrt.org/kamikaze/8.09.2/brcm47xx/packages/openssl-util_0.9.8i-3.2_mipsel.ipk
ipkg -d smbfs -force-depends install libpcap_0.9.4-1_mipsel.ipk liblua_5.0.2-1_mipsel.ipk lua_5.0.2-1_mipsel.ipk wget_1.11-4_mipsel.ipk libopenssl_0.9.8i-3.2_mipsel.ipk openssl-util_0.9.8i-3.2_mipsel.ipk

if [ -f /jffs/usr/etc/wtm-configure-env.sh ];
then
    echo "wtm-configure-env exists"
else
    mkdir -p /jffs/usr/etc/
    mkdir -p /jffs/usr/lib/
    mkdir -p /jffs/usr/bin/
    cp $original_path/wtm-configure-env.sh /jffs/usr/etc/
    nvram set rc_startup="
    source /jffs/usr/etc/wtm-configure-env.sh &
    "
    nvram commit
    cp $original_path/etc/* /jffs/usr/etc/
    cp -r $original_path/lib/* /jffs/usr/lib/
    cp $original_path/wtm-start.sh /jffs/usr/etc/
    cp $original_path/wtm-pollster.lua /jffs/usr/etc/
    cp $original_path/wiviz-src/wiviz /jffs/usr/bin
fi


export LUA_INIT="@/jffs/usr/lib/compat-5.1.lua"
export PATH="$PATH:/tmp/smbshare/usr/bin:/tmp/smbshare/usr/sbin"
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/tmp/smbshare/usr/lib"

#Run the script!
/jffs/usr/etc/wtm-start.sh
