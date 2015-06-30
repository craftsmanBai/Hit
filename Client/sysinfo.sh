#!/bin/bash
FILENAME=$1
taskid=$2
if [ `uname -p` = "x86_64" ];
then
        PROFILENAME=$(uname -s)$(uname -n)_$(uname -r | tr  "." "_")_$(uname -p)"x64"
else
    PROFILENAME=$(uname -s)$(uname -n)_$(uname -r | tr  "." "_")_$(uname -p)"x86"
    
fi

linux_iomem=$( python $PWD/volatility-2.4/vol.py -f $PWD/image/$FILENAME --profile=$PROFILENAME linux_iomem  2>/dev/null | awk -F '0x' '\
                        {print \
                        "{ \
                                \"Name\":\""$1"\", \
                                \"Start\":\""0x""$2"\", \
                                \"End\":\""0x""$3"\"},"}')
linux_mount=$( python $PWD/volatility-2.4/vol.py -f $PWD/image/$FILENAME --profile=$PROFILENAME linux_mount  2>/dev/null | awk  'NR>1 \
                        {print \
                        "{ \
                                \"Device\":\""$1"\", \
                                \"MountPoint\":\""$2"\", \
                                \"FSType\":\""$3"\", \
                                \"MountOptions\":\""$4"\"},"}')
linux_dentry_cache=$( python $PWD/volatility-2.4/vol.py -f $PWD/image/$FILENAME --profile=$PROFILENAME linux_dentry_cache  2>/dev/null | awk  '\
                        {print \
                        "{ \
                                \"Info\":\""$1"\"},"}')

linux_dmesg=''

:<<!
linux_dmesg=$(python $PWD/volatility-2.4/vol.py -f $PWD/image/$FILENAME --profile=$PROFILENAME linux_psenv  2>/dev/null | awk  'NR>=2 \
                        {print \
                        "{ \
                                \"Name\":\""$1"\", \
                                \"Pid\":\""$2"\", \
                                \"Environment\":\""$3"\"},"}')
!


data="{\"task_id\":$taskid, \
\"info\":\"sysinfo\", \
\"linux_dmesg\":[${linux_dmesg%?}], \
\"linux_iomem\":[${linux_iomem%?}], \
\"linux_mount\":[${linux_mount%?}], \
\"linux_dentry_cache\":[${linux_dentry_cache%?}]}"





echo $data > tmp_s.data
iconv -f GBK -t UTF-8 -c tmp_s.data -o tmpfile_s.data
rm -rf tmp_s.data

curl -H "Content-type: application/json" -d @tmpfile_s.data http://192.168.58.1:5000/result
rm -rf tmpfile_s.data

rm -rf tmpfile_s.data
