#!/bin/bash
FILENAME=$1
taskid=$2
if [ `uname -p` = "x86_64" ];
then
        PROFILENAME=$(uname -s)$(uname -n)_$(uname -r | tr  "." "_")_$(uname -p)"x64"
else
    PROFILENAME=$(uname -s)$(uname -n)_$(uname -r | tr  "." "_")_$(uname -p)"x86"
    
fi

linux_arp=$( python $PWD/volatility-2.4/vol.py -f $PWD/image/$FILENAME --profile=$PROFILENAME linux_arp  2>/dev/null | awk  '\
                        {print \
                        "{ \
                                \"IP\":\""$1"]""\", \
                                \"MAC\":\""$4"\", \
                                \"Interface\":\""$6"\"},"}')
linux_ifconfig=$( python $PWD/volatility-2.4/vol.py -f $PWD/image/$FILENAME --profile=$PROFILENAME linux_ifconfig  2>/dev/null | awk  'NR>2 \
                        {print \
                        "{ \
                                \"Interface\":\""$1"\", \
                                \"IPAddress\":\""$2"\", \
                                \"MacAddress\":\""$3"\", \
                                \"PromiscousMode\":\""$4"\"},"}')
linux_route_cache=$( python $PWD/volatility-2.4/vol.py -f $PWD/image/$FILENAME --profile=$PROFILENAME linux_route_cache  2>/dev/null | awk  'NR>2 \
                        {print \
                        "{ \
                                \"Interface\":\""$1"\", \
                                \"Destination\":\""$2"\", \
                                \"Gateway\":\""$3"\"},"}')
linux_netstat=''
:<<!
linux_netstat=$(python $PWD/volatility-2.4/vol.py -f $PWD/image/$FILENAME --profile=$PROFILENAME linux_netstat  2>/dev/null | awk  'NR>=2 \
                        {print \
                        "{ \
                                \"Name\":\""$1"\", \
                                \"Pid\":\""$2"\", \
                                \"Environment\":\""$3"\"},"}')
!
data="{\"task_id\":$taskid, \
\"info\":\"netinfo\", \
\"linux_arp\":[${linux_arp%?}], \
\"linux_ifconfig\":[${linux_ifconfig%?}], \
\"linux_route_cache\":[${linux_route_cache%?}], \
\"linux_netstat\":[${linux_netstat%?}]}"

echo $data > tmp_n.data
iconv -f GBK -t UTF-8 -c tmp_n.data -o tmpfile_n.data
rm -rf tmp_n.data

curl -H "Content-type: application/json" -d @tmpfile_n.data http://192.168.58.1:5000/result
rm -rf tmpfile_n.data
