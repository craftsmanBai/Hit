#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SelectField, IntegerField, validators, SelectMultipleField, widgets
from wtforms.validators import DataRequired,EqualTo,Length,InputRequired,URL,NumberRange,AnyOf,ValidationError
from models import User
import re


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

class RegistrationForm(Form):
    username = StringField('username',validators=[
        DataRequired('plz input your username.'),
        Length(min = 3, max = 25,message='length between 3 and 25')
    ])
    email = StringField('email',validators=[
        DataRequired('plz input your email.'),
        Length(min = 4, max = 25,message='length must between 6 and 25')
    ])
    password = PasswordField('password', validators=[
        InputRequired('plz input password.'),
        Length(min = 8, max = 36,message='length must between 8 and 36')
    ])
    rptpassword = PasswordField('repeat password', validators=[
        InputRequired('plz input password to confirm'),
        Length(min = 8, max = 36,message='length must between 8 and 36'),
        EqualTo('password','password must be match')

    ])
    

    def validate_username(form,field):
        if not re.match(r'^[a-zA-Z0-9_-]{3,24}$',field.data):
            raise ValidationError(u'Wrong Username Format.')
        if field.data == "None":
            raise ValidationError(u'Wrong Username Format.')
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(u'Username existed.')

    def validate_email(form,field):
        if not re.match(r'^[a-zA-Z0-9]+\@[a-zA-Z0-9]+\.[a-zA-Z0-9]+$',field.data):
            raise ValidationError(u'Wrong Email Format.')

class TaskConfigForm(Form):
    ddate = StringField('ddate', validators=[])
    dtime = StringField('dtime', validators=[])
    comment = StringField('comment', validators=[])
    targetip = StringField('targetip', validators=[])

class StatusForm(Form):
    taskid = StringField('taskid', validators=[DataRequired()])
    taskhost = StringField('taskhost', validators=[DataRequired()])
    startime = StringField('startime', validators=[DataRequired()])
    endtime = StringField('endtime', validators=[DataRequired()])
    status = StringField('status', validators=[DataRequired()])


class pslist(Form):
    offset = StringField('offset', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    pid = StringField('pid', validators=[DataRequired()])
    uid = StringField('uid', validators=[DataRequired()])
    dtb = StringField('dtb', validators=[DataRequired()])
    startime = StringField('startime', validators=[DataRequired()])

class pstree(Form):
    name = StringField('name', validators=[DataRequired()])
    pid = StringField('pid', validators=[DataRequired()])
    uid = StringField('uid', validators=[DataRequired()])

class arp(Form):
    ip = StringField('ip', validators=[DataRequired()])
    mac = StringField('mac', validators=[DataRequired()])
    devname = StringField('devname', validators=[DataRequired()])

class apihooks(Form):
    pid = StringField('p', validators=[DataRequired()])
    name = StringField('n ', validators=[DataRequired()])
    hookvma = StringField('hookvma', validators=[DataRequired()])
    hooksymbol = StringField('hooksymbol', validators=[DataRequired()])
    hookedaddress = StringField('hookedaddress', validators=[DataRequired()])
    Type = StringField('Type', validators=[DataRequired()])
    hookaddress = StringField('hookaddress', validators=[DataRequired()])
    hooklibrary = StringField('hooklibrary', validators=[DataRequired()])

class bash(Form):
    pid = StringField('pid', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    commandtime = StringField('commandtime', validators=[DataRequired()])
    command = StringField('command', validators=[DataRequired()])

class bash_hash(Form):
    pid = StringField('pid', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    hits = StringField('hits', validators=[DataRequired()])
    command = StringField('command', validators=[DataRequired()])
    fullpath = StringField('fullpath', validators=[DataRequired()])

class bash_env(Form):
    pid = StringField('pid', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    Vars = StringField('Vars', validators=[DataRequired()])

class check_modules(Form):
    moduleaddress = StringField('moduleaddress', validators=[DataRequired()])
    modulename = StringField('modulename', validators=[DataRequired()])

class check_creds(Form):
    pids = StringField('pids', validators=[DataRequired()])

class check_fop(Form):
    symbolname = StringField('symbolname', validators=[DataRequired()])
    member = StringField('m', validators=[DataRequired()])
    address = StringField('address', validators=[DataRequired()])

class check_tty(Form):
    name = StringField('name', validators=[DataRequired()])
    address = StringField('address', validators=[DataRequired()])
    symbol = StringField('symbol', validators=[DataRequired()])

class check_afinfo(Form):
    symbolname = StringField('symbolname', validators=[DataRequired()])
    member = StringField('member', validators=[DataRequired()])
    address = StringField('address', validators=[DataRequired()])

class check_syscall(Form):
    tablename = StringField('tablename', validators=[DataRequired()])
    index = StringField('index', validators=[DataRequired()])
    systemcall = StringField('systemcall', validators=[DataRequired()])
    index = StringField('index', validators=[DataRequired()])
    handleraddress = StringField('handleraddress', validators=[DataRequired()])
    symbol = StringField('symbol', validators=[DataRequired()])

class check_inline_kernel(Form):
    name = StringField('name', validators=[DataRequired()])
    member = StringField('member', validators=[DataRequired()])
    hooktype = StringField('hooktype', validators=[DataRequired()])
    hookaddress = StringField('hookaddress', validators=[DataRequired()])
'''
class dmesg(Form):
    name = StringField('name', validators=[DataRequired()])
    pid = StringField('pid', validators=[DataRequired()])
    environment = StringField('environment', validators=[DataRequired()])
'''
class dentry_cache(Form):
    info = StringField('info', validators=[DataRequired()])

class enumerate_files(Form):
    path = StringField('path', validators=[DataRequired()])

class hidden_modules(Form):
    offset = StringField('offset', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])

class ifconfig(Form):
    interface = StringField('interface', validators=[DataRequired()])
    ipaddress = StringField('ipaddress', validators=[DataRequired()])
    macaddress = StringField('macaddress', validators=[DataRequired()])
    promiscousmode = StringField('promiscousmode', validators=[DataRequired()])

class iomem(Form):
    name = StringField('name', validators=[DataRequired()])
    start = StringField('startime', validators=[DataRequired()])
    end = StringField('end', validators=[DataRequired()])

class keyboard_notifier(Form):
    address = StringField('address', validators=[DataRequired()])
    symbol = StringField('symbol', validators=[DataRequired()])

class kernel_opened_files(Form):
    offset = StringField('offset', validators=[DataRequired()])
    partialfilepath = StringField('partialfilepath', validators=[DataRequired()])

class lsof(Form):
    pid = StringField('pid', validators=[DataRequired()])
    fd = StringField('fd', validators=[DataRequired()])
    path = StringField('path', validators=[DataRequired()])

class list_raw(Form):
    process = StringField('process', validators=[DataRequired()])
    pid = StringField('pid', validators=[DataRequired()])
    filedescriptor = StringField('filedescriptor', validators=[DataRequired()])
    inode = StringField('inode', validators=[DataRequired()])

class library_list(Form):
    task = StringField('task', validators=[DataRequired()])
    pid = StringField('pid', validators=[DataRequired()])
    loadaddress = StringField('loadaddress', validators=[DataRequired()])
    path = StringField('path', validators=[DataRequired()])

class ldrmodules(Form):
    pid = StringField('pid', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    start = StringField('start', validators=[DataRequired()])
    filepath = StringField('filepath', validators=[DataRequired()])
    kernel = StringField('kernel', validators=[DataRequired()])
    libc = StringField('libc', validators=[DataRequired()])

class lsmod(Form):
    name = StringField('name', validators=[DataRequired()])
    pid = StringField('pid', validators=[DataRequired()])
    environment = StringField('environment', validators=[DataRequired()])

class mount(Form):
    device = StringField('device', validators=[DataRequired()])
    mountpoint = StringField('mountpoint', validators=[DataRequired()])
    fstype = StringField('fstype', validators=[DataRequired()])
    mountoptions = StringField('mountoptions', validators=[DataRequired()])


class netstat(Form):
    name = StringField('name', validators=[DataRequired()])
    pid = StringField('pid', validators=[DataRequired()])
    environment = StringField('environment', validators=[DataRequired()])

class netfilter(Form):
    proto = StringField('proto', validators=[DataRequired()])
    hook = StringField('hook', validators=[DataRequired()])
    handler = StringField('handler', validators=[DataRequired()])
    ishooked = StringField('ishooked', validators=[DataRequired()])

class psxview(Form):
    offset = StringField('offset', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    pid = StringField('pid', validators=[DataRequired()])
    pslist = StringField('pslist', validators=[DataRequired()])
    pid_hash = StringField('pid_hash', validators=[DataRequired()])
    kmem_cache = StringField('kmem_cache', validators=[DataRequired()])
    parrent = StringField('parrent', validators=[DataRequired()])
    leaders = StringField('leaders', validators=[DataRequired()])

class plthook(Form):
    task = StringField('task', validators=[DataRequired()])
    elfstart = StringField('elfstart', validators=[DataRequired()])
    elfname = StringField('elfname', validators=[DataRequired()])
    symbol = StringField('symbol', validators=[DataRequired()])
    resolveaddress = StringField('resolveaddress', validators=[DataRequired()])
    h = StringField('h', validators=[DataRequired()])
    targetinfoh = StringField('targetinfoh', validators=[DataRequired()])

class psaux(Form):
    pid = StringField('pid', validators=[DataRequired()])
    uid = StringField('uid', validators=[DataRequired()])
    gid = StringField('gid', validators=[DataRequired()])
    arguments = StringField('arguments', validators=[DataRequired()])

class pslist(Form):
    offset = StringField('offset', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    pid = StringField('pid', validators=[DataRequired()])
    uid = StringField('uid', validators=[DataRequired()])
    dtb = StringField('dtb', validators=[DataRequired()])
    startime = StringField('startime', validators=[DataRequired()])

class pstree(Form):
    name = StringField('name', validators=[DataRequired()])
    pid = StringField('pid', validators=[DataRequired()])
    uid = StringField('uid', validators=[DataRequired()])

class psenv(Form):
    name = StringField('name', validators=[DataRequired()])
    pid = StringField('pid', validators=[DataRequired()])
    environment = StringField('environment', validators=[DataRequired()])

class proc_maps(Form):
    pid = StringField('pid', validators=[DataRequired()])
    start = StringField('start', validators=[DataRequired()])
    end = StringField('end', validators=[DataRequired()])
    flags = StringField('flags', validators=[DataRequired()])
    pgoff = StringField('pgoff', validators=[DataRequired()])
    major = StringField('major', validators=[DataRequired()])
    minor = StringField('minor', validators=[DataRequired()])
    inode = StringField('inode', validators=[DataRequired()])
    filepath = StringField('filepath', validators=[DataRequired()])

class route_cache(Form):
    interface = StringField('interface', validators=[DataRequired()])
    destination = StringField('destination', validators=[DataRequired()])
    gateway = StringField('gateway', validators=[DataRequired()])

class tmpfs(Form):
    name = StringField('name', validators=[DataRequired()])
    pid = StringField('pid', validators=[DataRequired()])
    environment = StringField('environment', validators=[DataRequired()])

class limeinfo(Form):
    memorystart = StringField('memorystart', validators=[DataRequired()])
    memoryend = StringField('memoryend', validators=[DataRequired()])
    size = StringField('size', validators=[DataRequired()])






















