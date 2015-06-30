#!/bin/bash
FILENAME=$1
taskid=$2
if [ `uname -p` = "x86_64" ];
then
        PROFILENAME=$(uname -s)$(uname -n)_$(uname -r | tr  "." "_")_$(uname -p)"x64"
else
    PROFILENAME=$(uname -s)$(uname -n)_$(uname -r | tr  "." "_")_$(uname -p)"x86"
    
fi

linux_check_afinfo=$( python $PWD/volatility-2.4/vol.py -f $PWD/image/$FILENAME --profile=$PROFILENAME linux_check_afinfo  2>/dev/null | awk  'NR>2 \
                        {print \
                        "{ \
                                \"SymbolName\":\""$1"\", \
                                \"Member\":\""$2"\", \
                                \"Address\":\""$3"\"},"}')
linux_check_tty=$( python $PWD/volatility-2.4/vol.py -f $PWD/image/$FILENAME --profile=$PROFILENAME linux_check_tty  2>/dev/null | awk  'NR>2 \
                        {print \
                        "{ \
                                \"Name\":\""$1"\", \
                                \"Address\":\""$2"\", \
                                \"Symbol\":\""$3"\"},"}')
linux_check_creds=$( python $PWD/volatility-2.4/vol.py -f $PWD/image/$FILENAME --profile=$PROFILENAME linux_check_creds  2>/dev/null | awk  'NR>2 \
                        {print \
                        "{ \
                                \"Pids\":\""$1"\"},"}')
linux_check_fop=$( python $PWD/volatility-2.4/vol.py -f $PWD/image/$FILENAME --profile=$PROFILENAME linux_check_fop  2>/dev/null | awk  'NR>2 \
                        {print \
                        "{ \
                                \"SymbolName\":\""$1"\", \
                                \"Member\":\""$2"\", \
                                \"Address\":\""$3"\"},"}')
linux_check_syscall=$( python $PWD/volatility-2.4/vol.py -f $PWD/image/$FILENAME --profile=$PROFILENAME linux_check_syscall  2>/dev/null | awk  'NR>2 \
                        {print \
                        "{ \
                                \"TableName\":\""$1"\", \
                                \"Index\":\""$2"\", \
                                \"SystemCall\":\""$3"\", \
                                \"Index\":\""$4"\", \
                                \"HandlerAddress\":\""$5"\", \
                                \"Symbol\":\""$6"\"},"}')
linux_check_modules=$( python $PWD/volatility-2.4/vol.py -f $PWD/image/$FILENAME --profile=$PROFILENAME linux_check_modules  2>/dev/null | awk  'NR>2 \
                        {print \
                        "{ \
                                \"ModuleAddress\":\""$1"\", \
                                \"ModuleName\":\""$2"\"},"}')


data="{\"task_id\":$taskid, \
\"info\":\"rootkit\", \
\"linux_check_afinfo\":[${linux_check_afinfo%?}], \
\"linux_check_tty\":[${linux_check_tty%?}], \
\"linux_check_creds\":[${linux_check_creds%?}], \
\"linux_check_fop\":[${linux_check_fop%?}], \
\"linux_check_syscall\":[${linux_check_syscall%?}]}"



echo $data > tmp_r.data
iconv -f GBK -t UTF-8 -c tmp_r.data -o tmpfile_r.data
rm -rf tmp_r.data

curl -H "Content-type: application/json" -d @tmpfile_r.data http://192.168.58.1:5000/result
rm -rf tmpfile_r.data
