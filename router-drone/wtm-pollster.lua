#!/usr/bin/env lua

package.path=package.path..";/jffs/usr/lib/?.lua"
package.cpath=package.cpath..";/jffs/usr/lib/?/core.so"
require("math")
require("date")
dofile("/jffs/usr/lib/stringsplit.lua")
dofile("/jffs/usr/etc/config.lua")

-- Set timestamp format
date.fmt("${iso}-0300")

function PadCount(count)
    --[[
    Prefix the MAC address "count" for each db entry so that each count attribute is of consistent length,
    in order to be compatible with SimpleDB's lexicographical comparisons
    --]]

    final_num_digits = 8 -- The number of digits the output string should contain
    digs=string.len(tostring(count)) -- Get number of digits
    prefix=''
    for i=1,final_num_digits - digs do
        prefix = prefix..'0'
    end
    return prefix..tostring(count)
end

function GetTimeInt(timestamp, ival)
    -- Get which interval this datapoint belongs to

    timeint = ival * 60 -- Number of seconds in minutes_per_int
    interval = timestamp - (math.mod(timestamp, timeint))
    return interval
end

function url_encode(str)
    if (str) then
        str = string.gsub (str, "\n", "\r\n")
        str = string.gsub (str, " ", "%%20")
        str = string.gsub (str, ":", "%%3A")
        str = string.gsub (str, "=", "%%3D")
        str = string.gsub (str, "+", "%%2B")
        str = string.gsub (str, "/", "%%2F")
    end
    return str
end

function MakeSignature(params)
    strtosign = "GET\nsdb.amazonaws.com\n\n"..params
    sigcmd = 'echo -ne '..strtosign..' | openssl dgst -sha256 -hmac '..secret_key..' -binary | openssl enc -base64 | tr +/ -_ | tr -d "\n"'
    f = assert(io.popen(sigcmd, 'r'))
    output = assert(f:read("*a"))
    f:close()
    return output
end

function GetWgetArgs(ts, count)
    itemName = nodename.."-"..tostring(ts)
    attribute1 = "count"
    attribute1val = PadCount(count)
    attribute2 = "time_int"
    attribute2val = tostring(ts)
    attribute3 = "base_station"
    attribute3val = nodename
    version = "2009-04-15"
    sigversion = "2"
    sigmethod = "HmacSHA1"
    timestamp = tostring(date(true))
    params =
            "AWSAccessKeyId="..access_key..
            "&Action=PutAttributes"..
            "&Attribute.1.Name="..url_encode(attribute1)..
            "&Attribute.1.Value="..url_encode(attribute1val)..
            "&Attribute.2.Name="..url_encode(attribute2)..
            "&Attribute.2.Value="..url_encode(attribute2val)..
            "&Attribute.3.Name="..url_encode(attribute3)..
            "&Attribute.3.Value="..url_encode(attribute3val)..
            "&DomainName="..domain..
            "&ItemName="..itemName..
            "&SignatureMethod="..sigmethod..
            "&SignatureVersion="..sigversion..
            "&Timestamp="..url_encode(timestamp)..
            "&Version="..version

    tmppath="/tmp/root/tmpfile.tmp"
    os.execute("touch "..tmppath)
    file = io.open(tmppath, "w")
    file:write("GET\nsdb.amazonaws.com\n/\n"..params)
    file:close()

    params = string.gsub(params, "&", "\\&")
    os.execute("/jffs/usr/etc/sendtosdb.sh "..params.." "..secret_key)
    os.execute("rm /tmp/root/tmppath.tmp")
end

old_ts=0
datatable={}
while true do
    line = io.read()
    if line and not string.find(line,"Viz") and not string.find(line,"config") and not string.find(line,"channel") then
        tcpdump = split(line, "|")

        if GetTimeInt(tonumber(tcpdump[2]),minutes_per_interval) == old_ts then
            if not datatable[tcpdump[0]] then
                datatable[tcpdump[0]] = true
            end
        elseif old_ts == 0 then
            datatable[tcpdump[0]] = true
            old_ts = GetTimeInt(tonumber(tcpdump[2]), minutes_per_interval)
        else -- a new timestamp interval means that it's time to send some data to SimpleDB!
            count = 0
            for i in pairs(datatable) do -- count how many uniques there are
                count = count + 1
            end
            datatable = {} -- garbage collect the old data
            GetWgetArgs(old_ts, count)
            old_ts = GetTimeInt(tonumber(tcpdump[2]), minutes_per_interval) -- set new time int
        end
    end
end
