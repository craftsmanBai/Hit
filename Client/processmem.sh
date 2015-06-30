#!/bin/bash
FILENAME=$1
taskid=$2
if [ `uname -p` = "x86_64" ];
then
        PROFILENAME=$(uname -s)$(uname -n)_$(uname -r | tr  "." "_")_$(uname -p)"x64"
else
    PROFILENAME=$(uname -s)$(uname -n)_$(uname -r | tr  "." "_")_$(uname -p)"x86"
    
fi

linux_proc_maps=$( python $PWD/volatility-2.4/vol.py -f $PWD/image/$FILENAME --profile=$PROFILENAME linux_proc_maps  2>/dev/null | awk  'NR>2 \
                        {print \
                        "{ \
                                \"Pid\": \""$1"\", \
                                \"Start\": \""$2"\", \
                                \"End\": \""$3"\", \
                                \"Flags\": \""$4"\", \
                                \"Pgoff\": \""5"\", \
                                \"Major\": \""$6"\", \
                                \"Minor\": \""$7"\", \
                                \"Inode\": \""$8"\", \
                                \"FilePath\": \""$9"\"},"}')


data="{\"task_id\":$taskid, \
\"info\":\"processmem\", \
\"linux_proc_maps\":[${linux_proc_maps%?}]}"

echo $data > tmp_pm.data
iconv -f GBK -t UTF-8 -c tmp_pm.data -o tmpfile_pm.data
rm -rf tmps_pm.data

curl -H "Content-type: application/json" -d @tmpfile_pm.data http://192.168.58.1:5000/result
rm -rf tmpfile_pm.data
