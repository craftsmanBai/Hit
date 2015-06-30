#Horuseye client.py implemented by python, v0.01
# -*- coding: utf-8 -*-
#by Zing 2015  http://www.z1ng.net


from flask import Flask,request,jsonify
from flask.ext.restful import Resource, Api
import ConfigParser
import subprocess
import threading
import requests
import json
import time
import platform

app = Flask(__name__)
api = Api(app)

'''heartbeat ++++++++++++++++++++++++++++++++++++++++++++++++'''


config = ConfigParser.ConfigParser()
config.read("client.cfg")
CLIENT_NAME = config.get("info","CLIENT_NAME")
CLIENT_IP = config.get("info","CLIENT_IP")
CLIENT_SYSTEM = platform.system()

'''task setting---------------------------------------------'''

class TASK_SET(Resource):
    def get(self):
    	return "123123123"
    def put(self):
        job = request.get_json(force=True)
        INTERPRETER = "/usr/bin/python"  
        processor = "schedul.py"  
        pargs = [INTERPRETER, processor]
        pargs.extend([job['task_id'],job['start_time']])  
        subprocess.Popen(pargs)      
api.add_resource(TASK_SET, '/task_set/')
'''task setting---------------------------------------------'''

def live():
    while True:
        CLIENT_TIME = time.time()
        heartbeat = {'CLIENT_NAME': CLIENT_NAME,'CLIENT_INFO':{'CLIENT_IP':CLIENT_IP,"CLIENT_SYSTEM":CLIENT_SYSTEM,"CLIENT_TIME":CLIENT_TIME}}
        url = config.get("info","URL").rstrip('/')+"/active_client/"
        r = requests.put(url, data=json.dumps(heartbeat))
        print r
        time.sleep(10)
monitor = threading.Thread(target=live)
monitor.start()


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)

