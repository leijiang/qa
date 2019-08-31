#-*- coding: UTF-8 -*-
"""

(C) Copyright 2016 wei_cloud@126.com

"""
import subprocess
import signal
import platform
import random
import tempfile
import time
import re
import os
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class AppiumServer(object):

    def __init__(self, udid=None):
        self.udid = udid
        self.process = None
        self.maxruntime = 6  # 单位h，小时
        self.maxwaittime = 3600  # 单位s

    def StartServer(self, udid=None, wait=False):
        """
        -a serverip -p port -bp bpport -U uid
        """
        udid = udid or self.udid
        port = self.GetUnUsedPort()
        if not self.isDeivceIdle(udid) and not wait:
            raise AssertionError('Device %s is occupied by another session')
        starttime = time.time()
        while not self.isDeivceIdle(udid):
            curtime = time.time()
            if curtime - starttime > self.maxwaittime:
                raise AssertionError('Device %s is still occupied!' % udid)
            print "Device occupied, waiting for device..."
            time.sleep(300)

        cmd = "appium -U " + udid + " -p " + \
            str(port) + " --session-override --log-level error"
        self.process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, shell=True)
        time.sleep(15)  # wait to startup
        return port

    def StopServer(self, udid=None):
        udid = udid or self.udid
        pidlist = self.GetRunningTasks(udid)
        for process in pidlist:
            cmd = 'kill -9 %s' % process['pid']
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            p.communicate()

    def GetRunningTasks(self, udid=None):
        """
          739 Thu May 26 20:01:55 2016     adb -P 5037 fork-server server
        """
        udid = udid or self.udid
        cmd = 'ps -eo pid,lstart,command | grep "appium -U %s" | grep -v grep' % udid
        self.process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, shell=True)
        out, err = self.process.communicate()
        re_process = re.compile(
            r'''\s*(?P<pid>\d+)\s+(?P<lstart>\w+\s+\w+\s+\d+\s+\d+\:\d+\:\d+\s+\d+)\s+(?P<cmd>.*)''', re.X)
        ret = []
        if not out:
            return []
        for line in out.splitlines():
            m = re_process.match(line)
            ret.append(m.groupdict())
        return ret

    def IsPortInUse(self, port):
        """
        netstat -anp | grep 7960
        """
        cmd = "netstat -anp | grep %s" % port
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        out, err = p.communicate()
        return bool(out)

    def GetUnUsedPort(self):
        port = random.randint(4500, 50000)
        while self.IsPortInUse(port):
            port = random.randint(4500, 50000)
        return port

    def GetConnectedDevices(self):
        """
        """
        devices = []
        cmd = "adb devices"
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        out, err = p.communicate()
        out = out[out.index("List of devices attached"):]
        lines = out.splitlines()
        for line in lines[1:]:
            if line.strip() and not line.startswith('*'):
                deviceId, status = line.split()
                if status.lower() == 'device':
                    devices.append(deviceId)
        return devices

    def isDeivceIdle(self, udid=None):
        udid = udid or self.udid
        devicelist = self.GetConnectedDevices()
        if not udid in devicelist:
            raise AssertionError(
                'Device %s not connected! Please plugin the decvice!' % udid)
        tasks = self.GetRunningTasks(udid)
        curtime = time.strptime(time.ctime())
        for task in tasks:
            starttime = time.strptime(task['lstart'])
            if curtime.tm_year > starttime.tm_year or ((curtime.tm_yday - starttime.tm_yday) * 24 + curtime.tm_hour - starttime.tm_hour) > self.maxruntime:
                print 'Device %s occupied too long, force to stop!' % udid
                self.StopServer(udid)
            else:
                return False
        return True


class WindowsAppiumServer(object):
    """
    Appium server managed by device id
    """
#     AppiumPath = 'C:/SVN/appium'

    def __init__(self, udid=None):
        self.platform = platform.system()
        self.udid = udid
        self.pidfile = 'Appium.pid'
        self.process = None
        self.maxruntime = 6  # 单位h，小时
        self.maxwaittime = 3600  # 单位s

    def StartServer(self, path, udid=None, wait=False):
        """
        String Command = "appium.cmd -p " + port + " -bp " + bpport + " --session-override --chromedriver-port "+ chromeport +" -U " 
                         + udid +  " >c://" + port + ".txt";
        """
        udid = udid or self.udid
        port = self.GetUnUsedPort()
        bpport = self.GetUnUsedPort()
        print port
        print bpport
#         if not self.isDeivceIdle(udid) and not wait:
#             raise AssertionError('Device %s is occupied by another session')
#         starttime = time.time()
#         while not self.isDeivceIdle(udid):
#             curtime = time.time()
#             if curtime - starttime > self.maxwaittime:
#                 raise AssertionError('Device %s is still occupied!' % udid)
#             print "Device occupied, waiting for device..."
#             time.sleep(300)
#         cmd = path + " -U " + udid + " -p " + \
#             str(port) + " -bp " + str(bpport) + \
#             " --session-override --log-level error --no-reset"
        cmd = path + " -U " + udid + " -p " + \
            str(port) + " -bp " + str(bpport) + \
            " --session-override --log-level error"
        print cmd
#         cmd = 'node %s -p %s --session-override --log-level error -U %s' % (
#             self.AppiumPath, port, udid)
        self.process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, shell=True)
        self.UpdatePidFile(self.process.pid, port, udid)
        time.sleep(15)
        return port

    def StopServer(self, udid=None):
        """
        TASKKILL /PID 1230 /PID 1241 /PID 1253 /T
        """
        udid = udid or self.udid
        runningtask = self.GetRunningTask(udid)

        if not runningtask:
            print "No Appium session found on server. %s" % self.udid
            return
        cmd = 'TASKKILL /T /F /PID %s' % runningtask
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        out, err = p.communicate()
        self.UpdatePidFile(None, None, udid)
        return out

    def GetRunningTask(self, udid=None):
        """
        映像名称    PID 会话名    会话#  内存使用  状态      用户名     CPU 时间 窗口标题
        """
        udid = udid or self.udid
        alltask = self.GetAllTasks()
        pidinfo = self.GetPidInfoByUdid(udid)
        if not pidinfo:
            return None
        pid = pidinfo[0]
        if pid in alltask:
            return pid
        else:
            self.UpdatePidFile(None, None, udid)
        return None

    def GetAllTasks(self):
        tasks = []
        cmd = 'tasklist /V /FI "IMAGENAME eq cmd.exe"'
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        out, err = p.communicate()
        lines = out.splitlines()
        if len(lines) < 2:
            return []
        spliters = map(len, lines[2].split())
        for line in lines[3:]:
            attrs = self.GetTaskInfo(line, spliters)
            tasks.append(attrs[1])
        return tasks

    def GetTaskInfo(self, line, spliters):
        """
        """
        attrs = []
        offset = 0
        for i in range(len(spliters)):
            attrs.append(line[offset:offset + spliters[i]].strip())
            offset += spliters[i] + 1
        return attrs

    def IsPortInUse(self, port):
        """
        netstat -ano | findstr :1900
        """
        cmd = "netstat -ano | findstr :%s" % port
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        out, err = p.communicate()
        return bool(out)

    def GetUnUsedPort(self):
        port = random.randint(4500, 50000)
        while self.IsPortInUse(port):
            port = random.randint(4500, 50000)
        return port

    def GetConnectedDevices(self):
        """
        """
        devices = []
        cmd = "adb devices"
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        out, err = p.communicate()
        out = out[out.index("List of devices attached"):]
        lines = out.splitlines()
        for line in lines[1:]:
            if line.strip() and not line.startswith('*'):
                deviceId, status = line.split()
                if status.lower() == 'device':
                    devices.append(deviceId)
        return devices

    def GetIdleDevices(self):
        devices = self.GetConnectedDevices()
        deviceusage = self.ReadPidFile()
        devicelist = []
        for i in range(len(deviceusage) - 1, -1, -1):
            if deviceusage[i][2] not in devices:
                self.StopServer()
            elif (time.time() - float(deviceusage[i][3])) > 5 * 3600:
                self.StopServer()
                devicelist.append(deviceusage[i][2])

    def isDeivceIdle(self, udid=None):
        udid = udid or self.udid
        devicelist = self.GetConnectedDevices()
        if not udid in devicelist:
            raise AssertionError(
                'Device %s not connected! Please plugin the decvice!' % udid)
        pidinfo = self.GetPidInfoByUdid(udid)
        if pidinfo:
            curtime = time.strptime(time.ctime())
            starttime = time.strptime(pidinfo[3])
            if curtime.tm_year > starttime.tm_year or ((curtime.tm_yday - starttime.tm_yday) * 24 + curtime.tm_hour - starttime.tm_hour) > self.maxruntime:
                print 'Device %s occupied too long, force to stop!' % udid
                self.StopServer(udid)
            else:
                return False
        return True

    def WritePidFile(self, pids):
        with open(os.path.join(tempfile.gettempdir(), self.pidfile), 'wb') as fp:
            for pidinfo in pids:
                fp.write(' '.join(pidinfo) + os.linesep)

    def ReadPidFile(self):
        """
        pid, port, udid, time
        """
        filepath = os.path.join(tempfile.gettempdir(), self.pidfile)
        if not os.path.exists(filepath):
            return []
        with open(filepath, 'rb') as fp:
            lines = fp.readlines()
        ret = []
        for line in lines:
            tmp = line.split()
            ret.append((tmp[0], tmp[1], tmp[2], ' '.join(tmp[3:])))
        return ret

    def UpdatePidFile(self, pid, port, udid):
        starttime = str(time.ctime())
        changeflag = False
        pidlist = self.ReadPidFile()
        for i in range(len(pidlist) - 1, -1, -1):
            if pidlist[i][2] == udid:
                pidlist.pop(i)
                changeflag = True
        if pid:
            pidlist.append([str(pid), str(port), udid, starttime])
            changeflag = True
        if changeflag:
            self.WritePidFile(pidlist)

    def GetPidInfoByUdid(self, udid):
        pidlist = self.ReadPidFile()
        for pidinfo in pidlist:
            if pidinfo[2] == udid:
                return pidinfo
        return None

if __name__ == '__main__':
    print 'start'
    AppiumServer().StartServer('7N2SSE1534020959')
    time.sleep(5)
    print 'after 5'
#     AppiumServer().StopServer('7N2SSE1534020959')
    time.sleep(5)
    print 'end'
