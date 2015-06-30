#!/usr/bin/env python
# -*- coding: utf-8 -*-

from server import db,flask_bcrypt
from flask.ext.sqlalchemy import SQLAlchemy


class User(db.Model):
    __tablename__ = 'hit_user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password = db.Column(db.String(128))
    email = db.Column(db.String(128))
    def __init__(self, username=None, password=None, email=None):
        self.username = username
        self.password = flask_bcrypt.generate_password_hash(password)
        self.email = email
    def __repr__(self):
        return '<User %r>' % self.username
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return unicode(self.id)

class ramstat(db.Model):
    __tablename__ = 'current_ram'
    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Integer)
    used = db.Column(db.Integer)
    free = db.Column(db.Integer)
    def __init__(self,total=0,used=0,free=0):
        self.total = total
        self.used = used
        self.free = free
		
class ServerInfo(db.Model):
    __tablename__ = 'server_info'
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(128))
    system = db.Column(db.String(128))
    runtime = db.Column(db.String(128))
    def __init__(self, ip=None, system=None, runtime=None):
        self.ip = ip
        self.system = system
        self.runtime = runtime

#这个是我写的配置任务模块
class TaskConfig(db.Model):
    __tablename__ = 'task_config'
    taskid = db.Column(db.Integer, primary_key=True) #任务ID
    userid = db.Column(db.Integer) #创建者ID
    ip = db.Column(db.String(128))
    mode = db.Column(db.Integer) #任务部署状态 0:指定时间执行 1:每月 2:每周 3:每天
    state = db.Column(db.Integer) #任务执行状态 0:未执行 1:已执行
    text = db.Column(db.String(1024)) #任务注释
    startime = db.Column(db.String(256))
    finishtime = db.Column(db.String(256))
    linux_pslist = db.Column(db.BLOB)
    linux_psaux = db.Column(db.BLOB)
    linux_pstree = db.Column(db.BLOB)
    linux_psxview = db.Column(db.BLOB)
    linux_lsof = db.Column(db.BLOB)
    linux_iomem = db.Column(db.BLOB)
    linux_mount = db.Column(db.BLOB)
    linux_dentry_cache = db.Column(db.BLOB)
    linux_dmesg = db.Column(db.BLOB)
    linux_check_afinfo = db.Column(db.BLOB)
    linux_check_tty = db.Column(db.BLOB)
    linux_check_creds = db.Column(db.BLOB)
    linux_check_fop = db.Column(db.BLOB)
    linux_check_syscall = db.Column(db.BLOB)
    linux_lsmod = db.Column(db.BLOB)
    linux_tmpfs = db.Column(db.BLOB)
    linux_arp = db.Column(db.BLOB)
    linux_ifconfig = db.Column(db.BLOB)
    linux_route_cache = db.Column(db.BLOB)
    linux_netstat = db.Column(db.BLOB)
    linux_proc_maps = db.Column(db.BLOB)
    linux_bash = db.Column(db.BLOB)
    linux_check_modules = db.Column(db.BLOB)

    def __init__(self, userid=None, ip=None, mode=None, startime=None, state=0, text=None):
        self.userid = userid
        self.ip = ip
        self.mode = mode
        self.state = state
        self.text = text
        self.startime = startime
