#!/bin/bash
FILENAME=$1
taskid=$2
if [ `uname -p` = "x86_64" ];
then
        PROFILENAME=$(uname -s)$(uname -n)_$(uname -r | tr  "." "_")_$(uname -p)"x64"
else
    PROFILENAME=$(uname -s)$(uname -n)_$(uname -r | tr  "." "_")_$(uname -p)"x86"
    
fi

linux_lsmod=$(python $PWD/volatility-2.4/vol.py -f $PWD/image/$FILENAME --profile=$PROFILENAME linux_lsmod  2>/dev/null | awk  '\
                        {print \
                        "{ \
                                \"Name\":\""$1"\", \
                                \"Pid\":\""$2"\", \
                                \"Environment\":\""$3"\"},"}')
linux_tmpfs=''
:<<!
linux_tmpfs=$(python $PWD/volatility-2.4/vol.py -f $PWD/image/$FILENAME --profile=$PROFILENAME linux_tmpfs  2>/dev/null | awk  'NR>=2 \
                        {print \
                        "{ \
                                \"Name\":\""$1"\", \
                                \"Pid\":\""$2"\", \
                                \"Environment\":\""$3"\"},"}')
!
data="{\"task_id\":$taskid, \
\"info\":\"kernel_mem\", \
\"linux_lsmod\":[${linux_lsmod%?}], \
\"linux_tmpfs\":[${linux_tmpfs%?}]}"


echo $data > tmp_k.data
iconv -f GBK -t UTF-8 -c tmp_k.data -o tmpfile_k.data
rm -rf tmp_k.data

curl -H "Content-type: application/json" -d @tmpfile_k.data http://192.168.58.1:5000/result
rm -rf tmpfile_k.data
