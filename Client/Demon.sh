#!/bin/bash
# Hit Demon.sh implemented by bash shell scripts, v0.01
# by Zing 2015  http://www.z1ng.net


HitLog="$PWD/log/Hit.log"
DaemonLog="$PWD/log/Daemon.log"
DaemonPID="$PWD/log/Daemon.pid"
HitPID="$PWD/log/Hit.pid"
COMMAND="python $PWD/client.py"
INTERVAL=${3:-1}
RETRY=3
STAT=1
PID=''

monitor() {
  while true 
  do
    PSLINE=$(ps $PID | wc -l)
    if [ -n "$PID" -a $PSLINE -eq 1 ]; then
      start_process
      echo restart
    fi
    echo $PSLINE
    sleep $INTERVAL 
  done;
}

stop() {
  if [ -e $HitPID ] ; then
    kill $(cat $HitPID)
    rm $HitPID 
    echo "master has stop"
  fi

  if [ -e $DaemonPID ] ; then
    kill $(cat $DaemonPID)
    rm $DaemonPID 
    echo "child has stop"
  fi
}

start_process() {
  $COMMAND > $HitLog &
  PID=$!
  sleep 1 
  PSLINE=$(ps $PID | wc -l)
  if [ $PSLINE -eq 1 ]; then
    RETRY=$(($RETRY - 1))
    STAT=0
  else
    RETRY=3
    STAT=1
    echo $PID > $DaemonPID
  fi

  if [ $RETRY -lt 1 ]; then
    echo some error occured
    exit 1
  fi
}

start_monitor() {
  (monitor &> $DaemonLog& [ $STAT -eq 1 ] && echo $! > $HitPID)
}

start_process
start_monitor
echo "Write to Deamon.log"
exit 0