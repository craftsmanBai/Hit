#Horuseye schedule implemented by python, v0.01
# -*- coding: utf-8 -*-
#by Zing 2015  http://www.z1ng.net


import sys
import requests
import subprocess
import json
from crontab import CronTab
import string
import ConfigParser

task_id = sys.argv[1]
task_time = sys.argv[2]




def carry(filename,task_id):
	INTERPRETER = "/bin/bash"  
	for sh in ['process.sh','netinfo.sh','processmem.sh','sysinfo.sh','rootkit.sh','kernel_mem.sh']:
	    processor = sh
	    pargs = [INTERPRETER, processor,filename,task_id] 
	    result = subprocess.Popen(pargs)
	    
	   
	    
		




if task_time == "immediate":
	print 'okokoko'
	p = subprocess.Popen('./job.sh', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	filename = p.stdout.read()
	print filename
	print p.wait()
	if p.wait() == 0:
		print 'job success'
		carry(filename,task_id)
	else:
		pass
	

else:
	system_cron = CronTab(tabfile='/etc/crontab', user=False)
	COMMA = 'python schedul.py task_id immediate'
	job = system_cron.new(command=COMMA, user='root')
	job.setall(task_time)
	system_cron.write( 'HorusEyeCron.tab' )

