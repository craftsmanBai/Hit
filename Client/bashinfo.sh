#!/bin/bash
FILENAME=$1
taskid=$2
if [ `uname -p` = "x86_64" ];
then
        PROFILENAME=$(uname -s)$(uname -n)_$(uname -r | tr  "." "_")_$(uname -p)"x64"
else
    PROFILENAME=$(uname -s)$(uname -n)_$(uname -r | tr  "." "_")_$(uname -p)"x86"
    
fi


linux_bash=$( python $PWD/volatility-2.4/vol.py -f $PWD/image/$FILENAME --profile=$PROFILENAME linux_bash  2>/dev/null | awk  'NR>2 \
                        {print \
                        "{ \
                                \"Pid\": \""$1"\", \
                                \"Name\": \""$2"\", \
                                \"CommandTime\": \""$3"\", \
                                \"Command\": \""$4"\"},"}')


data="{\"task_id\":$taskid, \
\"info\":\"bashinfo\", \
\"linux_bash\":[${linux_bash%?}]}"



echo $data > tmp_b.data
iconv -f GBK -t UTF-8 -c tmp_b.data -o tmpfile_b.data
rm -rf tmps_b.data

curl -H "Content-type: application/json" -d @tmpfile_b.data http://192.168.58.1:5000/result
rm -rf tmpfile_b.data
