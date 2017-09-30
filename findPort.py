#!/usr/bin/env python
# -*- coding: utf8 -*-
'''
Created on 2016-07-13
@author: Linwencai
查看占用端口的进程
'''
import os
import sys


def cinput(msg):
    return getattr(__builtins__, 'raw_input', input)(msg)


def shell(cmd):
    with os.popen(cmd) as fp:
        return fp.read()


def win(port):
    netstat = shell('netstat -aon|findstr ":%s"' % port)
    if not netstat:
        return
    
    netstatList = [i for i in netstat.split('\n') if 'LISTENING' in i]
    if not netstatList:
        return
    print "\n".join(netstatList)
    netstat = netstatList[0]
    pid = netstat[netstat.rfind(' ')+1:]
    #print(pid)

    tasklist = shell('tasklist|findstr " %s "' % pid)
    if not tasklist:
        return
    print(tasklist)

    if not cinput("kill?").lower().startswith('y'):
        return
    #print(shell('TASKKILL /PID %s /T /F' % pid))
    print(shell('TASKKILL /PID %s /T /F' % pid))

    
def linux(port):
    tasklist = shell('netstat -lnp|grep ":%s"' % port)
    if not tasklist:
        return
    print(tasklist)

    pid = tasklist[tasklist.rfind('LISTEN')+11: tasklist.rfind('/')]
    if not pid:
        return
    
    if not cinput("kill?").lower().startswith('y'):
        return
    #print(shell('kill -9 %s' % pid))
    print(shell('kill %s' % pid))
    

if __name__ == '__main__':
    port = cinput("port:")

    if sys.platform.startswith('win'):
        win(port)
    elif sys.platform.startswith('linux'):
        linux(port)
    else:
        print('Error platform:%s' % sys.platform)
