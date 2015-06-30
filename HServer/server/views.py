#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template, redirect,request, url_for,jsonify,Flask,session,g,abort,flash
from server import app, db, login_manager, flask_bcrypt, live_dic
from flask.ext.login import current_user, login_required, login_user, logout_user
from models import User,ramstat, TaskConfig
from forms import LoginForm,RegistrationForm,TaskConfigForm
import chartkick
import time,math
import sys

app.config['SECRET_KEY'] = '7798fshk@#$@$sfasdu234'
@login_manager.user_loader
def load_user(id):
    user = User.query.filter_by(id=id).first()
    return user

@app.route('/')
def index():
    if current_user.is_authenticated():
        return redirect(url_for('homepage'), 302)
    else:
        return redirect(url_for('login'), 302)

@app.route('/login',methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(username=request.form['username']).first()
        if user and flask_bcrypt.check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('homepage'), 302)
    return render_template('login.html',form=form)

@app.route('/regok', methods=['GET'])
def regok():
    return render_template('regok.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'), 302)

@app.route("/deltask/<id>", methods=['GET', 'POST'])
@login_required
def deltask(id):
    taskid = int(id)
    task = TaskConfig.query.filter_by(userid=current_user.id,taskid=taskid).first()
    if task:
        db.session.delete(task)
        db.session.commit()
        return 'yes'
    else:
        return 'no'

@app.route('/clientstatus')
@login_required
def clientstatus():
    '''
    filedata = [ { "MD5": "0", "name": "/lost+found", "inode": "11", "mode_as_string": "d/drwx------", "UID": "0", "GID": "0", "size": "16384", "atime": "1427368046", "mtime": "1426785483", "ctime": "1426785484", "crtime": "0"}, { "MD5": "0", "name": "/boot", "inode": "261633", "mode_as_string": "d/drwxr-xr-x", "UID": "0", "GID": "0", "size": "4096", "atime": "1426785484", "mtime": "1426785484", "ctime": "1426785484", "crtime": "0"}, { "MD5": "0", "name": "/dev", "inode": "392449", "mode_as_string": "d/drwxr-xr-x", "UID": "0", "GID": "0", "size": "4096", "atime": "1426785484", "mtime": "1426785484", "ctime": "1426785484", "crtime": "0"}, { "MD5": "0", "name": "/proc", "inode": "654081", "mode_as_string": "d/drwxr-xr-x", "UID": "0", "GID": "0", "size": "4096", "atime": "1426785484", "mtime": "1426785484", "ctime": "1426785484", "crtime": "0"}, { "MD5": "0", "name": "/sys", "inode": "130817", "mode_as_string": "d/drwxr-xr-x", "UID": "0", "GID": "0", "size": "4096", "atime": "1426785484", "mtime": "1426785484", "ctime": "1426785484", "crtime": "0"}, { "MD5": "0", "name": "/var", "inode": "523265", "mode_as_string": "d/drwxr-xr-x", "UID": "0", "GID": "0", "size": "4096", "atime": "1427368046", "mtime": "1426785770", "ctime": "1426785770", "crtime": "0"}, { "MD5": "0", "name": "/tmp", "inode": "261634", "mode_as_string": "d/drwxrwxrwt", "UID": "0", "GID": "0", "size": "4096", "atime": "1427370132", "mtime": "1427370961", "ctime": "1427370961", "crtime": "0"}, { "MD5": "0", "name": "/etc", "inode": "654082", "mode_as_string": "d/drwxr-xr-x", "UID": "0", "GID": "0", "size": "12288", "atime": "1427367414", "mtime": "1427796039", "ctime": "1427796039", "crtime": "0"}, { "MD5": "0", "name": "/root", "inode": "130818", "mode_as_string": "d/dr-xr-x---", "UID": "0", "GID": "0", "size": "4096", "atime": "1427368045", "mtime": "1427297955", "ctime": "1427297955", "crtime": "0"}, { "MD5": "0", "name": "/selinux", "inode": "392450", "mode_as_string": "d/drwxr-xr-x", "UID": "0", "GID": "0", "size": "4096", "atime": "1426785493", "mtime": "1426785493", "ctime": "1426785493", "crtime": "0"}, { "MD5": "0", "name": "/lib64", "inode": "261636", "mode_as_string": "d/dr-xr-xr-x", "UID": "0", "GID": "0", "size": "12288", "atime": "1427367414", "mtime": "1426760685", "ctime": "1426760685", "crtime": "0"}, { "MD5": "0", "name": "/usr", "inode": "130821", "mode_as_string": "d/drwxr-xr-x", "UID": "0", "GID": "0", "size": "4096", "atime": "1427298590", "mtime": "1426785508", "ctime": "1426785508", "crtime": "0"}, { "MD5": "0", "name": "/bin", "inode": "392451", "mode_as_string": "d/dr-xr-xr-x", "UID": "0", "GID": "0", "size": "4096", "atime": "1427367414", "mtime": "1427299794", "ctime": "1427299794", "crtime": "0"}, { "MD5": "0", "name": "/home", "inode": "12", "mode_as_string": "d/drwxr-xr-x", "UID": "0", "GID": "0", "size": "4096", "atime": "1427297361", "mtime": "1427274494", "ctime": "1427274494", "crtime": "0"}, { "MD5": "0", "name": "/lib", "inode": "13", "mode_as_string": "d/dr-xr-xr-x", "UID": "0", "GID": "0", "size": "4096", "atime": "1427367414", "mtime": "1426785680", "ctime": "1426785680", "crtime": "0"}, { "MD5": "0", "name": "/media", "inode": "392452", "mode_as_string": "d/drwxr-xr-x", "UID": "0", "GID": "0", "size": "4096", "atime": "1427368046", "mtime": "1316778620", "ctime": "1426785508", "crtime": "0"}, { "MD5": "0", "name": "/mnt", "inode": "261640", "mode_as_string": "d/drwxr-xr-x", "UID": "0", "GID": "0", "size": "4096", "atime": "1427368045", "mtime": "1426785957", "ctime": "1426785957", "crtime": "0"}, { "MD5": "0", "name": "/opt", "inode": "392453", "mode_as_string": "d/drwxr-xr-x", "UID": "0", "GID": "0", "size": "4096", "atime": "1427298490", "mtime": "1426757216", "ctime": "1426757216", "crtime": "0"}, { "MD5": "0", "name": "/sbin", "inode": "261641", "mode_as_string": "d/dr-xr-xr-x", "UID": "0", "GID": "0", "size": "12288", "atime": "1427367414", "mtime": "1426760688", "ctime": "1426760688", "crtime": "0"}, { "MD5": "0", "name": "/srv", "inode": "392454", "mode_as_string": "d/drwxr-xr-x", "UID": "0", "GID": "0", "size": "4096", "atime": "1427368045", "mtime": "1316778620", "ctime": "1426785508", "crtime": "0"}, { "MD5": "0", "name": "/.autofsck", "inode": "3716", "mode_as_string": "r/rrw-r--r--", "UID": "0", "GID": "0", "size": "0", "atime": "1426785935", "mtime": "1426785935", "ctime": "1426785935", "crtime": "0"}, { "MD5": "0", "name": "/centos.dd", "inode": "4854", "mode_as_string": "r/rrw-r--r--", "UID": "0", "GID": "0", "size": "0", "atime": "1427796096", "mtime": "1427796096", "ctime": "1427796096", "crtime": "0"}, { "MD5": "0", "name": "/$OrphanFiles", "inode": "866657", "mode_as_string": "d/d---------", "UID": "0", "GID": "0", "size": "0", "atime": "0", "mtime": "0", "ctime": "0", "crtime": "0"} ]
    for d in range(0,len(filedata)):
        if int(filedata[d]['size']):
            filedata[d]['size'] = convertBytes(float(filedata[d]['size']))
        filedata[d]['atime'] = rtnTimeStr(float(filedata[d]['atime']))
        filedata[d]['mtime'] = rtnTimeStr(float(filedata[d]['mtime']))
        filedata[d]['ctime'] = rtnTimeStr(float(filedata[d]['ctime']))
        filedata[d]['crtime'] = rtnTimeStr(float(filedata[d]['crtime']))
    '''
    return render_template('clientstatus.html',live_dic=live_dic)

@app.route('/homepage')
@login_required
def homepage():  
    return render_template('homepage.html')

'''
任务配置页面
userid=current_user.id,
'''
@app.route('/taskconfig',methods=['GET', 'POST'])
@login_required
def taskconfig():
    form = TaskConfigForm()
    if request.method == 'POST':
        timeset = form.ddate.data + " " + form.dtime.data
        if time.mktime(time.strptime(timeset,'%Y-%m-%d %H:%M'))<time.time():
            startime = "immediate"
        else:
            startime =  timeset
        newtask = TaskConfig(userid=current_user.id, ip=form.targetip.data, mode=0, startime=startime, state=0, text=form.comment.data)
        db.session.add(newtask)
        db.session.commit()
        return redirect(url_for('clientstatus'))
    return render_template('taskconfig.html',form=form,live_dic=live_dic)

@app.route('/result',methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        if request.json['info'] == 'sysinfo':
            taskres = TaskConfig.query.filter_by(taskid=request.json['task_id']).first()
            taskres.linux_iomem = str(request.json['linux_iomem'])
            taskres.linux_mount = str(request.json['linux_mount'])
            taskres.linux_dentry_cache = str(request.json['linux_dentry_cache'])
            taskres.linux_dmesg = str(request.json['linux_dmesg'])
            db.session.commit()
        elif request.json['info'] == 'rootkit':
            taskres = TaskConfig.query.filter_by(taskid=request.json['task_id']).first()
            taskres.linux_check_afinfo = str(request.json['linux_check_afinfo'])
            taskres.linux_check_tty = str(request.json['linux_check_tty'])
            taskres.linux_check_creds = str(request.json['linux_check_creds'])
            taskres.linux_check_fop = str(request.json['linux_check_fop'])
            taskres.linux_check_syscall = str(request.json['linux_check_syscall'])
            taskres.linux_check_modules = str(request.json['linux_check_modules'])
            db.session.commit()
        elif request.json['info'] == "process":
            taskres = TaskConfig.query.filter_by(taskid=request.json['task_id']).first()
            taskres.linux_pslist = str(request.json['linux_pslist'])
            taskres.linux_pstree = str(request.json['linux_pstree'])
            taskres.linux_psxview = str(request.json['linux_psxview'])
            taskres.linux_lsof = str(request.json['linux_lsof'])
            db.session.commit()
        elif request.json['info'] == 'kernel_mem':
            taskres = TaskConfig.query.filter_by(taskid=request.json['task_id']).first()
            taskres.linux_lsmod = str(request.json['linux_lsmod'])
            taskres.linux_tmpfs = str(request.json['linux_tmpfs'])
            db.session.commit()
        elif request.json['info'] == 'netinfo':
            taskres = TaskConfig.query.filter_by(taskid=request.json['task_id']).first()
            taskres.linux_arp = str(request.json['linux_arp'])
            taskres.linux_ifconfig = str(request.json['linux_ifconfig'])
            taskres.linux_route_cache = str(request.json['linux_route_cache'])
            taskres.linux_netstat = str(request.json['linux_netstat'])
            db.session.commit()
        elif request.json['info'] == 'processmem':
            taskres = TaskConfig.query.filter_by(taskid=request.json['task_id']).first()
            taskres.linux_proc_maps = str(request.json['linux_proc_maps'])    
            db.session.commit()
        elif request.json['info'] == 'bashinfo':
            taskres = TaskConfig.query.filter_by(taskid=request.json['task_id']).first()
            taskres.linux_bash = str(request.json['linux_bash'])
            db.session.commit()
        else:
            pass
        return "Result Logged.\n"
    else:
        return redirect(url_for('index'), 302)

@app.route('/result/<id>',methods=['GET','POST'])
@login_required
def showreport(id):
    taskid = int(id)
    taskres = TaskConfig.query.filter_by(taskid=taskid).first()
    host = taskres.ip
    startime = taskres.startime
    finishtime = taskres.finishtime
    note = taskres.text
    return render_template('result.html',taskid=taskid,host=host,startime=startime,finishtime=finishtime,note=note)

@app.route('/showtask')
@login_required
def showtask():
    tasklist = []
    reslist = TaskConfig.query.filter_by(userid=current_user.id,state=2).all()
    for res in reslist:
        taskdic = {}
        taskdic["taskid"] = res.taskid
        taskdic["host"] = res.ip
        taskdic["state"] = res.state
        taskdic["startime"] = res.startime
        taskdic["finishtime"] = res.finishtime
        taskdic["note"] = res.text
        tasklist.append(taskdic)
    return render_template('showtask.html',resdata=tasklist)

@app.route('/serverconfig',methods=['GET','POST'])
@login_required
def servercfg():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        user = User(form.username.data, form.password.data ,form.email.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('homepage'))
    return render_template('serverconfig.html', form=form)

@app.route('/taskstate',methods=['GET'])
@login_required
def tstate():
    tasklist = []
    reslist = TaskConfig.query.filter_by(userid=current_user.id).all()
    for res in reslist:
        taskdic = {}
        taskdic["taskid"] = res.taskid
        taskdic["host"] = res.ip
        taskdic["state"] = res.state
        taskdic["startime"] = res.startime
        taskdic["finishtime"] = res.finishtime
        taskdic["note"] = res.text
        tasklist.append(taskdic)
    return render_template('taskstate.html',resdata=tasklist)

@app.route('/download')
@login_required
def down():    
    return render_template('download.html')

@app.route('/pslist/<id>',methods=['GET'])
@login_required
def t1(id):
    taskid = int(id)
    res = TaskConfig.query.filter_by(taskid=taskid,userid=current_user.id).first()
    if res.linux_pslist:
        data = eval(res.linux_pslist)
    else:
        data = []
    return render_template('pslist.html',resdata=data)

@app.route('/psxview/<id>',methods=['GET'])
@login_required
def t6(id):
    taskid = int(id)
    res = TaskConfig.query.filter_by(taskid=taskid,userid=current_user.id).first()
    if res.linux_psxview:
        data = eval(res.linux_psxview)
    else:
        data = []
    return render_template('psxview.html',resdata=data)


@app.route('/psaux/<id>',methods=['GET'])
@login_required
def t2(id):
    taskid = int(id)
    res = TaskConfig.query.filter_by(taskid=taskid,userid=current_user.id).first()
    if res.linux_psaux:
        data = eval(res.linux_psaux)
    else:
        data = []
    return render_template('psaux.html',resdata=data)

@app.route('/pstree/<id>',methods=['GET'])
@login_required
def t3(id):
    taskid = int(id)
    res = TaskConfig.query.filter_by(taskid=taskid,userid=current_user.id).first()
    if res.linux_pstree:
        data = eval(res.linux_pstree)
    else:
        data = []
    return render_template('pstree.html',resdata=data)

@app.route('/pslist_cache/<id>',methods=['GET'])
@login_required
def t4(id):
    return render_template('pslist_cache.html')

@app.route('/pidhashtable/<id>',methods=['GET'])
@login_required
def t5(id):
    return render_template('pidhashtable.html')

@app.route('/lsof/<id>',methods=['GET'])
@login_required
def t7(id):
    taskid = int(id)
    res = TaskConfig.query.filter_by(taskid=taskid,userid=current_user.id).first()
    if res.linux_lsof:
        data = eval(res.linux_lsof)
    else:
        data = []
    return render_template('lsof.html',resdata=data)

@app.route('/memmap/<id>',methods=['GET'])
@login_required
def t8(id):
    return render_template('memmap.html')

@app.route('/proc_maps/<id>',methods=['GET'])
@login_required
def t9(id):
    taskid = int(id)
    res = TaskConfig.query.filter_by(taskid=taskid,userid=current_user.id).first()
    if res.linux_proc_maps:
        data = eval(res.linux_proc_maps)
    else:
        data = []
    return render_template('proc_maps.html')

@app.route('/dump_map/<id>',methods=['GET'])
@login_required
def t10():
    return render_template('dump_map.html')

@app.route('/11')
@login_required
def t11(id):
    return render_template('11.html',resdata=data)

@app.route('/bash/<id>',methods=['GET'])
@login_required
def t12(id):
    taskid = int(id)
    res = TaskConfig.query.filter_by(taskid=taskid,userid=current_user.id).first()
    if res.linux_bash:
        data = eval(res.linux_bash)
    else:
        data = []
    return render_template('bash.html',resdata=data)

@app.route('/lsmod_moddump/<id>',methods=['GET'])
@login_required
def t13(id):
    taskid = int(id)
    res = TaskConfig.query.filter_by(taskid=taskid,userid=current_user.id).first()
    if res.linux_lsmod:
        data = eval(res.linux_lsmod)
    else:
        data = []
    return render_template('lsmod_moddump.html',resdata=data)

@app.route('/tmpfs/<id>',methods=['GET'])
@login_required
def t14(id):
    taskid = int(id)
    res = TaskConfig.query.filter_by(taskid=taskid,userid=current_user.id).first()
    if res.linux_tmpfs:
        data = eval(res.linux_tmpfs)
    else:
        data = []
    return render_template('tmpfs.html',resdata=data)

@app.route('/check_afinfo/<id>',methods=['GET'])
@login_required
def t15(id):
    taskid = int(id)
    res = TaskConfig.query.filter_by(taskid=taskid,userid=current_user.id).first()
    if res.linux_check_afinfo:
        data = eval(res.linux_check_afinfo)
    else:
        data = []
    return render_template('check_afinfo.html',resdata=data)

@app.route('/check_tty/<id>',methods=['GET'])
@login_required
def t16(id):
    taskid = int(id)
    res = TaskConfig.query.filter_by(taskid=taskid,userid=current_user.id).first()
    if res.linux_check_tty:
        data = eval(res.linux_check_tty)
    else:
        data = []
    return render_template('check_tty.html',resdata=data)

@app.route('/keyboard_notifier/<id>',methods=['GET'])
@login_required
def t17(id):
    taskid = int(id)
    res = TaskConfig.query.filter_by(taskid=taskid,userid=current_user.id).first()
    if res.linux_psaux:
        data = eval(res.linux_psaux)
    else:
        data = []
    return render_template('keyboard_notifier.html',resdata=data)

@app.route('/check_creds/<id>',methods=['GET'])
@login_required
def t18(id):
    taskid = int(id)
    res = TaskConfig.query.filter_by(taskid=taskid,userid=current_user.id).first()
    if res.linux_check_creds:
        data = eval(res.linux_check_creds)
    else:
        data = []
    return render_template('check_creds.html',resdata=data)

@app.route('/check_fop/<id>',methods=['GET'])
@login_required
def t19(id):
    taskid = int(id)
    res = TaskConfig.query.filter_by(taskid=taskid,userid=current_user.id).first()
    if res.linux_check_fop:
        data = eval(res.linux_check_fop)
    else:
        data = []
    return render_template('check_fop.html',resdata=data)

@app.route('/check_idt/<id>',methods=['GET'])
@login_required
def t20(id):
    taskid = int(id)
    return render_template('check_idt.html')

@app.route('/check_syscall/<id>',methods=['GET'])
@login_required
def t21(id):
    taskid = int(id)
    res = TaskConfig.query.filter_by(taskid=taskid,userid=current_user.id).first()
    if res.linux_check_syscall:
        data = eval(res.linux_check_syscall)
    else:
        data = []
    return render_template('check_syscall.html',resdata=data)

@app.route('/check_modules/<id>',methods=['GET'])
@login_required
def t22(id):
    taskid = int(id)
    res = TaskConfig.query.filter_by(taskid=taskid,userid=current_user.id).first()
    if res.linux_check_modules:
        data = eval(res.linux_check_modules)
    else:
        data = []
    return render_template('check_modules.html',resdata=data)

@app.route('/arp/<id>',methods=['GET'])
@login_required
def t23(id):
    taskid = int(id)
    res = TaskConfig.query.filter_by(taskid=taskid,userid=current_user.id).first()
    if res.linux_arp:
        data = eval(res.linux_arp)
    else:
        data = []
    return render_template('arp.html',resdata=data)

@app.route('/ifconfig/<id>',methods=['GET'])
@login_required
def t24(id):
    taskid = int(id)
    res = TaskConfig.query.filter_by(taskid=taskid,userid=current_user.id).first()
    if res.linux_ifconfig:
        data = eval(res.linux_ifconfig)
    else:
        data = []
    return render_template('ifconfig.html',resdata=data)

@app.route('/route_cache/<id>',methods=['GET'])
@login_required
def t25(id):
    taskid = int(id)
    res = TaskConfig.query.filter_by(taskid=taskid,userid=current_user.id).first()
    if res.linux_route_cache:
        data = eval(res.linux_route_cache)
    else:
        data = []
    return render_template('route_cache.html',resdata=data)
@app.route('/netstat/<id>',methods=['GET'])
@login_required
def t26(id):
    taskid = int(id)
    res = TaskConfig.query.filter_by(taskid=taskid,userid=current_user.id).first()
    if res.linux_netstat:
        data = eval(res.linux_netstat)
    else:
        data = []
    return render_template('netstat.html',resdata=data)

@app.route('/pkt_queues/<id>',methods=['GET'])
@login_required
def t27(id):
    return render_template('pkt_queues.html')

@app.route('/sk_buff_cache/<id>',methods=['GET'])
@login_required
def t28(id): 
    return render_template('sk_buff_cache.html')

@app.route('/sk_buff_cache/<id>',methods=['GET'])
@login_required
def t29(id):
    return render_template('sk_buff_cache.html')

@app.route('/cpuinfo/<id>',methods=['GET'])
@login_required
def t30(id):
    return render_template('cpuinfo.html')

@app.route('/dmesg/<id>',methods=['GET'])
@login_required
def t31(id):
    taskid = int(id)
    res = TaskConfig.query.filter_by(taskid=taskid,userid=current_user.id).first()
    if res.linux_dmesg:
        data = eval(res.linux_dmesg)
    else:
        data = []
    return render_template('dmesg.html',resdata=data)

@app.route('/iomem/<id>',methods=['GET'])
@login_required
def t32(id):
    taskid = int(id)
    res = TaskConfig.query.filter_by(taskid=taskid,userid=current_user.id).first()
    if res.linux_iomem:
        data = eval(res.linux_iomem)
    else:
        data = []
    return render_template('iomem.html',resdata=data)

@app.route('/slabinfo/<id>',methods=['GET'])
@login_required
def t33(id):
    return render_template('slabinfo.html')

@app.route('/mount/<id>',methods=['GET'])
@login_required
def t34(id):
    taskid = int(id)
    res = TaskConfig.query.filter_by(taskid=taskid,userid=current_user.id).first()
    if res.linux_mount:
        data = eval(res.linux_mount)
    else:
        data = []
    return render_template('mount.html',resdata=data)

@app.route('/mount_cache/<id>',methods=['GET'])
@login_required
def t35(id):

    return render_template('mount_cache.html')

@app.route('/dentry_cache/<id>',methods=['GET'])
@login_required
def t36(id):
    taskid = int(id)
    res = TaskConfig.query.filter_by(taskid=taskid,userid=current_user.id).first()
    if res.linux_dentry_cache:
        data = eval(res.linux_dentry_cache)
    else:
        data = []
    return render_template('dentry_cache.html',resdata=data)

@app.route('/find_file/<id>',methods=['GET'])
@login_required
def t37(id):
    return render_template('find_file.html')

@app.route('/vma_cache/<id>',methods=['GET'])
@login_required
def t38(id):
    return render_template('vma_cache.html')

@app.route('/volshell/<id>',methods=['GET'])
@login_required
def t39(id):
    
    return render_template('volshell.html')

@app.route('/yarascan/<id>',methods=['GET'])
@login_required
def t40(id):
    return render_template('yarascan.html')
