#!/bin/bash

FILENAME=$1
taskid=$2
if [ `uname -p` = "x86_64" ];
then
        PROFILENAME=$(uname -s)$(uname -n)_$(uname -r | tr  "." "_")_$(uname -p)"x64"
else
    PROFILENAME=$(uname -s)$(uname -n)_$(uname -r | tr  "." "_")_$(uname -p)"x86"
    
fi




linux_pslist=$( python $PWD/volatility-2.4/vol.py -f $PWD/image/$FILENAME --profile=$PROFILENAME linux_pslist 2>/dev/null | awk  'NR>=3 \
                        {print \
                        "{ \
                                \"Offset\":\""$1"\", \
                                \"Name\":\""$2"\", \
                                \"Pid\":\""$3"\", \
                                \"Uid\":\""$4"\", \
                                \"DTB\":\""$5"\", \
                                \"StartTime\":\""$6"\"},"}')




linux_psxview=$( python $PWD/volatility-2.4/vol.py -f $PWD/image/$FILENAME --profile=$PROFILENAME linux_psxview  2>/dev/null | awk  'NR>2 \
                        {print \
                        "{ \
                                \"Offset(V)\":\""$1"\", \
                                \"Name\":\""$2"\", \
                                \"Pid\":\""$3"\", \
                                \"pslist\":\""$4"\", \
                                \"pid_hash\":\""$5"\", \
                                \"kmem_cache\":\""$6"\", \
                                \"parrent\":\""$7"\", \
                                \"leaders\":\""$8"\"},"}')
linux_lsof=$( python $PWD/volatility-2.4/vol.py -f $PWD/image/$FILENAME --profile=$PROFILENAME linux_lsof  2>/dev/null | awk  'NR>2 \
                        {print \
                        "{ \
                                \"Pid\":\""$1"\", \
                                \"Fd\":\""$2"\", \
                                \"Path\":\""$3"\"},"}')



linux_pstree=$( python $PWD/volatility-2.4/vol.py -f $PWD/image/$FILENAME --profile=$PROFILENAME linux_pstree  2>/dev/null | awk  'NR>=3 \
                        {print \
                        "{ \
                                \"Name\":\""$1"\", \
                                \"Pid\":\""$2"\", \
                                \"Uid\":\""$3"\"},"}')


data="{\"task_id\":$taskid, \
\"info\":\"process\", \
\"linux_pslist\":[${linux_pslist%?}], \
\"linux_pstree\":[${linux_pstree%?}], \
\"linux_psxview\":[${linux_psxview%?}], \
\"linux_lsof\":[${linux_lsof%?}]}"



echo $data > tmp_p.data
iconv -f GBK -t UTF-8 -c tmp_p.data -o tmpfile_p.data
rm -rf tmp_p.data
curl -H "Content-type: application/json" -d @tmpfile_p.data http://192.168.58.1:5000/result
rm -rf tmpfile_p.data
:<<!
linux_psaux=$( python $PWD/volatility-2.4/vol.py -f $PWD/image/$FILENAME --profile=$PROFILENAME linux_psaux  2>/dev/null | awk  'NR>=2 \
                        {print \
                        "{ \
                                \"Pid\":\""$1"\", \
                                \"Uid\":\""$2"\", \
                                \"Gid\":\""$3"\", \
                                \"Arguments\":\""$4"\"},"}')
!



