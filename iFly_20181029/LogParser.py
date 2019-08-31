#-*- coding:utf-8 -*-
"""

(C) Copyright 2016 wei_cloud@126.com

"""
import re
import json
from robot.api import logger
from copy import deepcopy
from xml.dom.minidom import parseString

from robot.libraries.BuiltIn import BuiltIn
import os


class iFlyKeyLog(object):
    """
    I/KEY_LOCATION: {type:normal_key,left:915,top:10,right:1065,bottom:138,id:1230}
    u'D/KEY_LOCATION( 7084): {type:input_mode,method:0,layout:1,panel:7}
    """

    def __init__(self, log, appiumui='gui'):
        self.log = log['message']
        self.appiumui = appiumui
        self._parse(self.log)
        self.timestamp = log['timestamp']

    def _parse(self, log):
        """
        D/KEY_LOCATION( 4759): {type:emoji_content_key,left:398,top:282,right:463,bottom:351,id:/storage/sdcard0/iFlyIME/expression/ae298850-5704-11e3-949a-0800200c9a66//res/1-20-1F637,shown:true}
        08-20 04:00:17.085 12585 12585 D KEY_LOCATION: {type:menu_cell_key,left:356,top:200,right:472,bottom:303,text:祝福语,id=1049,shown:true,highlight:false,reddot:false}
        """
        if self.appiumui == 'gui':
            re_baseline = re.compile(r'''(?P<level>\w)/
                                         (?P<model>\w+?)\(\s*(?P<thread>\d+)\)\:
                                         \s*\{type\:(?P<type>\w+?)\,
                                         left\:(?P<left>[\-\d]+?)\,
                                         top\:(?P<top>[\-\d]+?)\,
                                         right\:(?P<right>[\-\d]+?)\,
                                         bottom\:(?P<bottom>[\-\d]+?)
                                         (\,(text\:(?P<text>.*?)\,)*(id[\=\:](?P<id>[\d/\w\-\.]+?)\,)*
                                         shown\:(?P<shown>\w+?))*
                                         (\,add\:(?P<add>\w+?))*
                                         (\,backup\:(?P<backup>\w+?))*
                                         (\,highlight\:(?P<highlight>\w+?))*(\,reddot\:(?P<reddot>\w+?))*
                                         (\,selected\:(?P<selected>\w+?))*\}
                                        ''', re.X)
        else:
            re_baseline = re.compile(r'''[\d\-]+\s+[\d\:\.]+\s+\d+\s+\d+\s+
                                        (?P<level>\w)\s+
                                         ((?P<model>[\w/\.\-\+\:\$\[\]]+?))*\s*\:
                                         \s*\{type\:(?P<type>\w+?)\,
                                         left\:(?P<left>[\-\d]+?)\,
                                         top\:(?P<top>[\-\d]+?)\,
                                         right\:(?P<right>[\-\d]+?)\,
                                         bottom\:(?P<bottom>[\-\d]+?)
                                         (\,(text\:(?P<text>.*?)\,)*(id[\=\:](?P<id>[\d/\w\-\.]+?)\,)*
                                         shown\:(?P<shown>\w+?))*
                                         (\,add\:(?P<add>\w+?))*
                                         (\,backup\:(?P<backup>\w+?))*
                                         (\,highlight\:(?P<highlight>\w+?))*(\,reddot\:(?P<reddot>\w+?))*
                                         (\,selected\:(?P<selected>\w+?))*\}
                                        ''', re.X)
        m = re_baseline.match(log)
        if m:
            ret = m.groupdict()
            self.level, self.model, self.type, self.left, self.top, self.right, self.bottom, self.text, self.id, self.shown, self.add, self.backup, self.highlight, self.reddot, self.selected = \
                ret['level'], ret['model'], ret['type'], int(ret['left']), int(ret['top']), int(ret['right']), int(ret['bottom']), ret[
                    'text'], ret['id'], ret['shown'], ret['add'], ret['backup'], ret['highlight'], ret['reddot'], ret['selected']
            self.location = (
                self.left + (self.right - self.left) / 2, self.top + (self.bottom - self.top) / 2)
        else:
            try:
                variables = BuiltIn().get_variables()
                logfile = variables['${LOG FILE}']
                if logfile != 'NONE':
                    logdir = os.path.dirname(logfile)
                else:
                    logdir = variables['${OUTPUTDIR}']
            except RuntimeError:
                pass
            filepath = logdir + '/' + 'errlog.txt'
            if os.path.exists(filepath):
                file = open(filepath, 'a')
                file.write(u"Log can not be parsed, format error. %s" % log)
                file.write("\n")
                file.close()

            raise RuntimeError(
                u"Log can not be parsed, format error. %s" % log)

    def __str__(self):
        return self.log

    def __unicode__(self):
        return self.__str__()


class iFlyKeyLogList(list):
    """
    self.layout values {type:input_mode,method:0,layout:1,panel:7}
    """
    OUT_KEY = ['pinyin_cloud', 'composing']
    STATIC_KEY = ['composing']

    def __init__(self, log, appiumui='gui'):
        list.__init__(self)
        self.keys = {}
        self.log = log
        self.appiumui = appiumui
        self.index = -1
        self.layout = None
        self._parse(log)

    def _parse(self, log):
        """
        05-26 09:15:49.825 21967 21979 D OperationResultFactory: 
        05-26 09:51:29.688 10834 10834 D skia    :
        """
        keylog_found = False
        i = len(log) - 1
        if self.appiumui == 'gui':
            re_loghead = re.compile(r'''(?P<level>\w)/
                                         ((?P<model>[\w/\.\-\+\:\$\[\]]+?))*\s*\(\s*(?P<thread>\d+)\)\:
                                         ''', re.X)
        else:
            re_loghead = re.compile(r'''[\d\-]+\s+[\d\:\.]+\s+\d+\s+\d+\s+
                                        (?P<level>\w)\s+
                                         ((?P<model>[\w/\.\-\+\:\$\[\]]+?))*\s*\:
                                         ''', re.X)
        while i >= 0:
            parsinglog = log[i]
            if not re_loghead.match(parsinglog['message']):
                parsinglog = deepcopy(log[i])
                parsinglog['message'] = log[
                    i - 1]['message'] + log[i]['message']
                i -= 1
                if not re_loghead.match(parsinglog['message']):
                    logger.warn(u'Log can not be parsed: %s' %
                                parsinglog['message'])
                    i -= 1
                    continue
            if not self.layout and parsinglog['message'].find('KEY_LOCATION') != -1 and parsinglog['message'].find('type:input_mode') != -1:
                self._parse_input_layout(parsinglog['message'])
                i -= 1
                continue
            if parsinglog['message'].find('KEY_LOCATION') != -1 and parsinglog['message'].find('type:stop') != -1:
                keylog_found = True
                i -= 1
                continue
            if keylog_found and parsinglog['message'].find('KEY_LOCATION') != -1:
                key = iFlyKeyLog(parsinglog, self.appiumui)
                if parsinglog['message'].find('type:start') != -1:
                    if len(self) == 0:
                        keylog_found = False
                        i -= 1
                        continue
                    elif len(self) == 1 and self.keys.keys()[0] in self.OUT_KEY:
                        cloudLocation = self.keys[
                            self.keys.keys()[0]][-1].location
                        if self.keys.keys()[0] == 'composing':
                            self.keys[
                                self.keys.keys()[0]][-1].location = (key.left + 35, key.top + cloudLocation[1])
                        else:
                            self.keys[self.keys.keys()[
                                0]][-1].location = (key.left + cloudLocation[0], key.top + cloudLocation[1])
                        keylog_found = False
                        i -= 1
                        continue
                    elif len(self) != 1 and self.keys.keys()[0] == 'pinyin_cloud':
                        keylog_found = False
                        i -= 1
                        continue
                    elif self.keys.keys()[0] not in self.OUT_KEY:
                        self.keys[key.type] = [key]
                        self.insert(0, key)
                        break
                    else:
                        i -= 1
                        continue
                try:
                    self.keys[key.type].insert(0, key)
                except:
                    self.keys[key.type] = [key]
                self.insert(0, key)

            i -= 1
        self.index = i

    def get_keys(self, type):
        return self.keys.get(type, [])

    def get_out_keys(self, keystr):
        if self.keys.has_key(keystr):
            return self.keys[keystr]
        else:
            self._parse(self.log[:self.index])
            return self.keys.get(keystr, [])

    def get_input_layout(self):
        if self.layout:
            return self.layout
        for i in range(self.index, -1, -1):
            if self.log[i]['message'].find('KEY_LOCATION') != -1 and self.log[i]['message'].find('type:input_mode') != -1:
                self._parse_input_layout(self.log[i]['message'])
        return self.layout

    def _parse_input_layout(self, log):
        """
        u'D/KEY_LOCATION( 7084): {type:input_mode,method:0,layout:1,panel:7}
        """
        if self.appiumui == 'gui':
            re_baseline = re.compile(r'''(?P<level>\w)/
                                         (?P<model>\w+?)\(\s*(?P<thread>\d+)\)\:
                                         \s*\{type\:(?P<type>\w+?)\,
                                         method\:(?P<method>\d+?)\,
                                         layout\:(?P<layout>\d+?)\,
                                         panel\:(?P<panel>\d+?)\}
                                        ''', re.X)
        else:
            re_baseline = re.compile(r'''[\d\-]+\s+[\d\:\.]+\s+\d+\s+\d+\s+
                                        (?P<level>\w)\s+
                                         ((?P<model>[\w/\.\-\+\:\$\[\]]+?))*\s*\:
                                         \s*\{type\:(?P<type>\w+?)\,
                                         method\:(?P<method>\d+?)\,
                                         layout\:(?P<layout>\d+?)\,
                                         panel\:(?P<panel>\d+?)\}
                                        ''', re.X)
        m = re_baseline.match(log)
        if m:
            self.layout = m.groupdict()
        else:
            raise RuntimeError(
                u"Log can not be parsed, format error. %s" % log)

    def __str__(self):
        return u'\n'.join(map(str, self))

    def __unicode__(self):
        return self.__str__()


class iFlyRequestLog(object):
    """
D/OperationManager( 9407): sRequst = <?xml version='1.0' encoding='utf-8' standalone='yes' ?><request><cmd>uplog</cmd><base><aid>100IME</aid><imei>mac:00:08:22:70:ba:df</imei><imsi></imsi><caller /><osid>android</osid><ua>GiONEE|F303|F303|ANDROID5.0|720*1280</ua><version>6.0.2998.ossptest</version><df>01010000</df><uid>160530094744788575</uid><uuid>a537fa5f-870d-4ee3-b6c3-10f237cfa490</uuid><mac>00:08:22:70:ba:df</mac><cpu /><androidid>3f0e2b5c8c3d43d6</androidid><cellid /><sid></sid><userid></userid><ap>wifi</ap></base><param /></request>
u"08-25 03:07:33.258  7144  7156 D OperationManager: sRequst = <?xml version='1.0' encoding='utf-8' standalone='yes' ?><request><cmd>gettoast</cmd><base><aid>100IME</aid><imei>864732021616548</imei><imsi></imsi><caller /><osid>android</osid><ua>OPSSON|opsson Q3C|p7528|ANDROID4.4.4|480*854</ua><version>6.0.2998.ossptest</version><df>01010000</df><uid>160420201936119842</uid><uuid>869f9b10-f3a2-423c-b3d1-155445de252f</uuid><mac>ff:ff:ff:ff:ff:ff</mac><cpu>0000000000000000</cpu><androidid>a1ade0814a9affcf</androidid><cellid /><sid></sid><userid></userid><ap>wifi</ap></base><param><timestamp>2016-05-18 18:58:19</timestamp></param></request>"
    """

    def __init__(self, log, appiumui='gui'):
        self.log = log['message']
        self.appiumui = appiumui
        self._parse(self.log)
        self.timestamp = log['timestamp']

    def _parse(self, log):
        if self.appiumui == 'gui':
            re_baseline = re.compile(r'''(?P<level>\w)/
                                         (?P<model>\w+?)\(\s*(?P<thread>\d+)\)\:
                                         \s*\{type\:(?P<type>\w+?)\,
                                         left\:(?P<left>[\-\d]+?)\,
                                         top\:(?P<top>[\-\d]+?)\,
                                         right\:(?P<right>[\-\d]+?)\,
                                         bottom\:(?P<bottom>[\-\d]+?)
                                         (\,(text\:(?P<text>.*?)\,)*(id[\=\:](?P<id>[\d/\w\-\.]+?)\,)*
                                         shown\:(?P<shown>\w+?))*
                                         (\,add\:(?P<add>\w+?))*
                                         (\,backup\:(?P<backup>\w+?))*
                                         (\,highlight\:(?P<highlight>\w+?))*(\,reddot\:(?P<reddot>\w+?))*
                                         (\,selected\:(?P<selected>\w+?))*\}
                                        ''', re.X)
        else:
            re_baseline = re.compile(r'''[\d\-]+\s+[\d\:\.]+\s+\d+\s+\d+\s+
                                        (?P<level>\w)\s+
                                         ((?P<model>[\w/\.\-\+\:\$\[\]]+?))*\s*\:
                                         \s*\{type\:(?P<type>\w+?)\,
                                         left\:(?P<left>[\-\d]+?)\,
                                         top\:(?P<top>[\-\d]+?)\,
                                         right\:(?P<right>[\-\d]+?)\,
                                         bottom\:(?P<bottom>[\-\d]+?)
                                         (\,(text\:(?P<text>.*?)\,)*(id[\=\:](?P<id>[\d/\w\-\.]+?)\,)*
                                         shown\:(?P<shown>\w+?))*
                                         (\,add\:(?P<add>\w+?))*
                                         (\,backup\:(?P<backup>\w+?))*
                                         (\,highlight\:(?P<highlight>\w+?))*(\,reddot\:(?P<reddot>\w+?))*
                                         (\,selected\:(?P<selected>\w+?))*\}
                                        ''', re.X)


class iFlyLogBaseList(list):
    """
    """

    def __init__(self, log, appiumui='gui', parser=None):
        list.__init__(self)
        self.log = log
        self.appiumui = appiumui
        self.parser = parser
        self.index = -1
        self._parse(log)

    def _parse(self, log):
        i = len(log) - 1
        while i >= 0:
            parsinglog = log[i]
            parsedlog = None
            try:
                parsedlog = iFlyLogBase(parsinglog)
            except AttributeError:
                parsinglog = deepcopy(log[i])
                parsinglog['message'] = log[
                    i - 1]['message'] + log[i]['message']
                i -= 1
                try:
                    parsedlog = iFlyLogBase(parsinglog)
                except AttributeError:
                    logger.info(u'Log can not be parsed: %s' %
                                parsinglog['message'])
                    i -= 1
                    continue
            if parsedlog:
                self.insert(0, parsedlog)
            i -= 1


class iFlyLogBase(dict):
    """
    """

    def __init__(self, log, appiumui='gui', parser=None):
        dict.__init__(self)
        self.log = log['message']
        self.appiumui = appiumui
        self.parser = parser
        self._parse(self.log)
        self.timestamp = log['timestamp']

    def _parse(self, log):
        if self.appiumui == 'gui':
            re_loghead = re.compile(r'''(?P<level>\w)/
                                         ((?P<model>[\w/\.\-\+\:\$\[\]]+?))*\s*\(\s*(?P<thread>\d+)\)\:\s*
                                         (?P<content>.*$)
                                         ''', re.X)
        else:
            re_loghead = re.compile(r'''[\d\-]+\s+[\d\:\.]+\s+\d+\s+\d+\s+
                                        (?P<level>\w)\s+
                                         ((?P<model>[\w/\.\-\+\:\$\[\]]+?))*\s*\:\s*
                                         (?P<content>.*$)
                                         ''', re.X)
        ret = re_loghead.match(log).groupdict()
        self.level, self.model, self.content = ret[
            'level'], ret['model'], ret['content']
        if self.parser:
            self.update(self.parser(self.content))


class iFlyLogContentBase(dict):
    """diff between iFlyLogContentBase And iFlyLogBase is:
        iFlyLogContentBase Log is Log Content
    """

    def __init__(self, log, appiumui='gui', parser=None):
        dict.__init__(self)
        self.log = log
        self.appiumui = appiumui
        self.parser = parser
        self._parse(self.log)

    def _parse(self, log):
        if self.parser:
            self.update(self.parser(log))


class OperationRequest(dict):

    def __init__(self, log):
        """
        """
        dict.__init__(self)
        if log:
            if 'type =' in log and ', result' in log:
                self.type = log.split('type = ')[1].split(',')[0]
            re_xmlstr = re.compile(r'''\<\?xml.*?\<\/request\>''', re.X)
            xmlstr = re_xmlstr.findall(log)[0]
            self._parse(parseString(xmlstr))

    def _parse(self, xml):
        if xml.hasChildNodes():
            for child in xml.childNodes:
                if child.nodeType == child.TEXT_NODE:
                    self[xml.tagName] = child.data
                self._parse(child)


class OperationResult(dict):

    def __init__(self, log):
        dict.__init__(self)
        if log:
            re_xmlstr = re.compile(r'''\<\?xml.*?\<\/result\>''', re.X)
            xmlstr = re_xmlstr.findall(log)[0]
            self._parse(parseString(xmlstr))

    def _parse(self, xml):
        """
        """
        self['status'] = xml.getElementsByTagName(
            'status')[0].childNodes[0].data
        if self['status'] != 'success':
            return
        configlist = xml.getElementsByTagName('config')
        for config in configlist:
            keys = config.getElementsByTagName('key')
            values = config.getElementsByTagName('value')
            for k, v in zip(keys, values):
                self[k.childNodes[0].data] = v.childNodes[0].data


class OperationResult2(dict):

    def __init__(self, log):
        dict.__init__(self)
        log_type = 'xml'
        if log:
            if('<result>' in log):
                # logcat日志可能会被截断,待处理，根节点不是result的情况
                if('</result>' not in log):
                    log_will_cast = log.rsplit('</', 1)[1].split('>', 1)[1]
                    log = log.replace(log_will_cast, '')

                    re_xmlstr = re.compile(r'''<.*?>''', re.X)
                    re_list = re_xmlstr.findall(log)
                    for node in re_list[::-1]:
                        if(not node.startswith('<?') and not node.startswith('</')):
                            if(node.replace('<', '</') not in log):
                                log += node.replace('<', '</')

                    print 'log casted:', log
            else:
                log_type = 'json'
            if(log_type == 'xml'):
                re_xmlstr = re.compile(r'''\<\?xml.*?\<\/result\>''', re.X)
                xmlstr = re_xmlstr.findall(log)[0]
                node = parseString(u'{0}'.format(xmlstr).encode('utf-8'))

                self._parse(parseString(u'{0}'.format(xmlstr).encode('utf-8')))
            else:
                re_jsonstr = re.compile(r'''{.*}''', re.X)
                jsonstr = re_jsonstr.findall(log)[0]
                self._parse_json(jsonstr)

    def _parse_json(self, jsonstr):
        d = json.loads(jsonstr)
        for k, v in d.items():
            self[k] = v

    def _parse(self, xml):
        """
        """

        if xml.hasChildNodes():
            for child in xml.childNodes:
                if child.nodeType == child.TEXT_NODE:
                    self[xml.tagName] = child.data
                self._parse(child)
        '''
        configlist = xml.getElementsByTagName('config')
        for config in configlist:
            keys = config.getElementsByTagName('key')
            values = config.getElementsByTagName('value')
            for k, v in zip(keys, values):
                print [k.childNodes[0].data,v.childNodes[0].data]
                self[k.childNodes[0].data] = v.childNodes[0].data
        '''

if __name__ == '__main__':
    pass
