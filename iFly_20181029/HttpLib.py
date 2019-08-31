#-*- coding: UTF-8 -*-
"""

(C) Copyright 2016 wei_cloud@126.com

"""
import urllib, urllib2
import cookielib
import rsa, base64
import os, random
import gzip
import StringIO
import json
from datetime import timedelta, datetime
from robot.api import logger

class CloudWebLib(object):
    public_key_conf = '''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDNzh69KDi0KQUh5g3G0oeTzSTg
X039du+Eq4d+w/F2WTPM5pprzIUR0fKzA2ETCT7VHhD6evA7TFjD3pp+PdLnzPrD
LHF+Iv3HhcDC+hiwRXR33Gm7gY2pbgpVy1Jj5aGBty1sH8tiZuvZKubPzBOOQWs9
un/QRzfdKWKSxAd7cwIDAQAB
-----END PUBLIC KEY-----'''
    
    def __init__(self):
        self.defaultCodec = 'UTF-8'
        self.defaultHeads = {'User-Agent': 'Chrome/46.0.2486.0',
                             'Content-Type': 'application/x-www-form-urlencoded; charset=%s' % self.defaultCodec,
                             'Pragma': 'no-cache',
                             'Accept': '*/*',
                             'Connection': 'Keep-Alive',}
        self.baseUrl = 'http://ossptest.voicecloud.cn:89'
        ck = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(ck))
        self.sessionId = ''
      
    def set_home_url(self, homeurl):
        old = self.baseUrl
        self.baseUrl = homeurl
        return old
      
    def _parse_url(self, url):
        if url.startswith('http://') or url.startswith('https://'):
            return url
        return self.baseUrl + url
      
    def _read_page(self, resp, unzip=True):
        page = resp.read()
        if unzip and resp.headers.get('Content-Encoding') == 'gzip':
            page = gzip.GzipFile(fileobj=StringIO.StringIO(page)).read()
        if not unzip and resp.headers.get('Content-Encoding') == 'gzip':
            return page
        if not isinstance(page, unicode):
            page = unicode(page, self.defaultCodec)
        logger.debug(page)
        return page
    
    def _get_page(self, url, args={}, heads={}, expectCode=200):
        url = self._parse_url(url)
        para = urllib.urlencode(args) if isinstance(args, dict) else args
        logger.info("Post Request %s with %s" % (url, para))
        rheads = {}
        rheads.update(self.defaultHeads)
        rheads.update(heads)
        
        url = url + '?' + para
        request = urllib2.Request(url, headers=rheads)
        resp = self.opener.open(request)
        if resp.getcode() != expectCode:
            raise AssertionError("Server Failure! Response code %s" % resp.getcode())
        page = self._read_page(resp)
        resp.close()
        return page
        
    def _post_page(self, url, data, heads={}, expectCode=200):
        url = self._parse_url(url)
        para = urllib.urlencode(data) if isinstance(data, dict) else data
        logger.info("Post Request %s with %s" % (url, para))
        rheads = {}
        rheads.update(self.defaultHeads)
        rheads.update(heads)
        
        request = urllib2.Request(url, para, rheads)
        resp = self.opener.open(request)
        if resp.getcode() != expectCode:
            raise AssertionError("Server Failure! Response code %s" % resp.getcode())
        page = self._read_page(resp)
        resp.close()
        return page
    
    def login_cloud_web(self, username, passwd, url='/auth/login', heads={}):
        values = {'loginName':username,
                  'password':self._enc_passwd(passwd),
                 }
        page = self._post_page(url, values, heads)
        if page.find(u'错误：') != -1:
            raise RuntimeError('Login Failed!')
        self.sessionId = self.get_session_id()
   
    def _enc_passwd(self, passwd):
        public_key = rsa.PublicKey.load_pkcs1_openssl_pem(self.public_key_conf)
        return base64.encodestring(rsa.encrypt(passwd, public_key))
   
    def _get_cookie_value(self, cookies, skey):
        val = ''
        if not isinstance(cookies, dict):
            return ''
        for key, value in cookies.items():
            if key == skey:
                val = value
                break
            val = self._get_cookie_value(value, skey)
            if val: break
        return val
   
    def get_cookie_item(self, skey):
        ck = None
        for handler in self.opener.handlers:
            if isinstance(handler, urllib2.HTTPCookieProcessor):
                ck = handler.cookiejar._cookies
                break
        if not ck:
            return ''
        logger.debug(ck)
        return self._get_cookie_value(ck, skey)
    
    def get_session_id(self):
        sessionId = self.get_cookie_item('SHAREJSESSIONID').value
        if not sessionId:
            raise RuntimeError("Can not find session id in cookies!")
        return sessionId


    def search_user_group(self, bizId='', query_province='', query_city='', 
                          query_type='', usergroup_name='', 
                          url='/auth/usergroupList.json', **kws):
        """
        """
        values = {'sEcho': '3',
                  'iColumns': '9',
                  'sColumns': '',
                  'iDisplayStart': '0',
                  'iDisplayLength': '10',
                  'bizId': bizId,
                  'query_province': query_province,
                  'query_city': query_city,
                  'query_type': query_type,
                  'usergroup_name': usergroup_name,}
        page = self._post_page(url, values)
        grouplist = json.loads(page, encoding=self.defaultCodec)["aaData"]
        return grouplist
    
    def add_user_group(self, bizId='100IME', name='', description='', type='1',
                       uidfilename='', uidlist='', category='1',
                       province='0', city='', url='/auth/usergroupSave.json'):
        """
        """
        if not name or not description or (not uidfilename and not uidlist):
            raise AssertionError("Missing Name or UID info, Please check your input!")
        province = '' if city else province
        uidlist = '\r\n'.join(uidlist) if isinstance(uidlist, list) else uidlist
        fileurl, origName = self.upload_file(uidfilename, uidlist)
        groupinfo = {'bizId': bizId,
                     'name': name,
                     'description': description,
                     'type': type,
                     'listUrl': fileurl,
                     'fileOriginalname': origName,
                     'category': category,
                     }
        logger.debug(groupinfo)
        values = {'usergroupInfo': urllib.quote(json.dumps(groupinfo)),
                  'hiddenProvince': province,
                  'hiddenCity': city,}
        
        page = self._post_page(url, values)
        if not page == '1':
            raise AssertionError("Add User Group Failed! Got page: %s" % page)
        return page
        
    def _generate_upload_data(self, filename=None, content=None):
        '''
        '''
        if not filename and not content:
            raise AssertionError("No value provided. please input filename or content!")
        boundary = '----------%s' % ''.join(random.sample('0123456789abcdef', 15))
        fields = []
        uploadname = filename if filename else 'TestAutoList.txt'
        uploadcontent = content if content else open(uploadname, 'rb').read()
        
        fields.append('--' + boundary)
        fields.append('Content-Disposition: form-data; name="Filename"')
        fields.append('')
        fields.append(os.path.basename(uploadname))
        
        fields.append('--' + boundary)
        fields.append('Content-Disposition: form-data; name="file"; filename="%s"' % os.path.basename(uploadname))
        fields.append('Content-Type: application/octet-stream')
        fields.append('')
        fields.append(uploadcontent) 
        
        fields.append('--' + boundary)
        fields.append('Content-Disposition: form-data; name="Upload"')
        fields.append('')
        fields.append('Submit Query')
        
        fields.append('--' + boundary + '--')
        fields.append('')
        body = '\r\n'.join(fields)
        content_type = 'multipart/form-data; boundary=%s' % boundary
        return content_type, body
        
        
    def upload_file(self, filename=None, content=None, url='/auth/usergroupUpload.json'):
        """
        """
        if not filename and not content:
            raise AssertionError("No value provided. please input filename or content!")
        url = url + ';jsessionid=%s' % self.get_session_id() * 2
        content_type, data = self._generate_upload_data(filename, content)
        heads = {'Content-Type': content_type,
                 'User-Agent': 'Shockwave Flash',}
        page = self._post_page(url, data, heads)
        fileurl, origName = page.split(',')
        return fileurl, origName
    
    def remove_user_group_byID(self, ugid, url='/auth/usergroupDelete.json'):
        """
        """
        values = {'ugid': ugid,}
        page = self._get_page(url, values)
        if not page == 'true':
            raise AssertionError("Remove User Group Failed! Got page: %s" % page)
        return page
    
    def remove_user_group(self, usergroup_name, bizId='', query_province='', query_city='', 
                          query_type=''):
        """
        """
        grouplist = self.search_user_group(bizId, query_province, query_city, query_type, usergroup_name)
        for group in grouplist:
            logger.info(u'Removing Group %s' % group)
            self.remove_user_group_byID(group[0])
        logger.info('%d groups removed!' % len(grouplist))
        
    def search_gray_config(self, product='', platform='', type='', status='', 
                           text='', url='/auth/paramCfg/pageQuery', **kws):
        """
        """
        values = {'sEcho': '3',
                  'iColumns': '8',
                  'sColumns': 'cp.code,,,,,,,',
                  'iDisplayStart': '0',
                  'iDisplayLength': '10',
                  'iSortingCols': '0',
                  'bSortable_0': 'true',
                  'bSortable_1': 'false',
                  'bSortable_2': 'false',
                  'bSortable_3': 'false',
                  'bSortable_4': 'false',
                  'bSortable_5': 'false',
                  'bSortable_6': 'false',
                  'bSortable_7': 'false',
                  'product': product,
                  'platform': platform,
                  'type': type,
                  'status': status,
                  'text': text,}
        page = self._post_page(url, values)
        configlist = json.loads(page, encoding=self.defaultCodec)["aaData"]
        return configlist
    
    def get_gray_exception_byID(self, garyid, url='/auth/paramMng/getById'):
        """
        """
        values = {'id': garyid,}
        page = self._post_page(url, values)
        exceptionlist = json.loads(page, encoding=self.defaultCodec)["paramValueCfgs"]
        logger.info(u'Got exception list %s' % exceptionlist)
        return exceptionlist
        
    def get_gray_exception(self, product='', platform='', type='', status='',
                           text='', **kws):
        """
        """
        grayid = self.search_gray_config(product, platform, type, status, text, **kws)[0][-1]
        return grayid, self.get_gray_exception_byID(grayid)
        
    def save_gray_exception(self, grayid, cfgs, url='/auth/paramCfg/save'):
        """
        """
        values = {'paramId': grayid,
                  'cfgs': json.dumps(cfgs, encoding=self.defaultCodec, separators=(',', ':')),}
        page = self._post_page(url, values)
        if page != 'null':
            logger.info(page)
            raise AssertionError(u"Save Failed! Got Page: %s" % page)
        return page
    
    def add_gray_exception(self, grayName, paramValue, groupName, 
                           startTime='', endTime='', configType='0', 
                           status=1, cacheStatus=0, **kws):
        """
        """
        ugId = self.search_user_group(usergroup_name=groupName, **kws)[0][0]
        startTime = startTime if startTime else (datetime.now() + timedelta(days=-1)).strftime('%Y-%m-%d')
        endTime = endTime if endTime else (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d')
        exception = {'id': '',
                     'ugId': ugId,
                     'paramValue': paramValue,
                     'configType': configType,
                     'status': status,
                     'cacheStatus': cacheStatus,
                     'startTime': startTime,
                     'endTime': endTime,
                     'paramValueCfgUGs': [{"ugId":ugId,"cacheStatus":cacheStatus}],
                     'paramExts': [],}
        logger.info(exception)
        grayid, exceptionlist = self.get_gray_exception(text=grayName, **kws)
        cache = {'cacheStatus': cacheStatus}
        for ex in exceptionlist:
            ex.update(cache)
            ex['startTime'] = self._update_time_format(ex['startTime'])
            ex['endTime'] = self._update_time_format(ex['endTime'])
            for ugcfg in ex['paramValueCfgUGs']:
                ugcfg.update(cache)
        exceptionlist.append(exception)
        self.save_gray_exception(grayid, exceptionlist)
    
    def _update_time_format(self, timestr):
        if isinstance(timestr, basestring) and timestr.count('-') > 0:
            return timestr
        return time.strftime('%Y-%m-%d', time.localtime(float(timestr)/1000.0))
    
    def remove_gray_exception(self, grayName, groupName, **kws):
        """
        """
        ugId = self.search_user_group(usergroup_name=groupName, **kws)[0][0]
        grayid, exceptionlist = self.get_gray_exception(text=grayName, **kws)
        cache = {'cacheStatus': 0}
        removed = False
        for i in range(len(exceptionlist)-1, -1, -1):
            ex = exceptionlist[i]
            for group in ex['paramValueCfgUGs']:
                if group['ugId'] == ugId:
                    exceptionlist.remove(ex)
                    removed = True
                    logger.info(ex)
                    ex = None
                    break
            if not ex:
                continue
            ex.update(cache)
            ex['startTime'] = self._update_time_format(ex['startTime'])
            ex['endTime'] = self._update_time_format(ex['endTime'])
            for ugcfg in ex['paramValueCfgUGs']:
                ugcfg.update(cache)
        if not removed:
            raise RuntimeError('No group %s found in exception list %s' % (groupName, grayName))
        self.save_gray_exception(grayid, exceptionlist)
        
    def search_new_message(self, bizId='100IME', province='', city='', type='',
                           messageStatus='', messageName='', startDate='', 
                           endDate='', pushSys='all',url='/auth/messageList.json'):
        """
        """
        values = {'sEcho': '3',
                  'iColumns': '16',
                  'sColumns': '',
                  'iDisplayStart': '0',
                  'iDisplayLength': '10',
                  'bizId': bizId,
                  'province': province,
                  'city': city,
                  'type': type,
                  'messageStatus': messageStatus,
                  'messageName': messageName,
                  'startDate': startDate,
                  'endDate': endDate,
                  'pushSys': pushSys,}
        page = self._post_page(url, values)
        messagelist = json.loads(page, encoding=self.defaultCodec)["aaData"]
        logger.debug(messagelist)
        return messagelist
        
    def remove_new_message_byID(self, msgId, url='/auth/messageDelete.json'):
        """
        msgId=10111929
        """
        values = {'msgId': msgId,}
        page = self._post_page(url, values)
        return page
     
    def remove_new_message(self, messageName, bizId='100IME', province='', 
                           city='', type='', messageStatus='', startDate='', 
                           endDate='', pushSys='all', **kws):
        """
        """
        messagelist = self.search_new_message(bizId, province, city, type, messageStatus, messageName, startDate, endDate, pushSys)
        logger.info(messagelist)
        for message in messagelist:
            self.remove_new_message_byID(message[0])
          
    def add_new_message(self, msgId='', activityId='', extras_operator='', extras_model='',
                        extras_channel='', versionList='', params_ShowId='2002', params_DCount='1',
                        usergroupname='', hiddenusergroupname='', params_DStartTime='', params_DEndTime='',
                        title='', imgUrl='', content='', params_ActionId='3009', linkUrl='',
                        skininfoname='', hidden_skininfoname='', skinctgname='', hidden_skinctgname='',
                        bizId='100IME', osId='Android', pushSys='ossp', issecret='', 
                        actionParam='', msgType='1017', localMsgType='1017',
                        url='/auth/messageSave.json', **kws):
        """
        """
        if not title or not content or (not usergroupname and not hiddenusergroupname):
            raise AssertionError("Missing Parameters!")
        if not usergroupname or not hiddenusergroupname:
            sk = usergroupname or hiddenusergroupname
            group = self.search_user_group(bizId=bizId, usergroup_name=sk, **kws)
            usergroupname, hiddenusergroupname = group[1], group[0]
        params_DStartTime = params_DStartTime if params_DStartTime else (datetime.now() + timedelta(days=-1)).strftime('%Y-%m-%d %H:%M:%S')
        params_DEndTime = params_DEndTime if params_DEndTime else (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S')
        values = {'msgId': msgId,
                  'activityId': activityId,
                  'extras_operator': extras_operator,
                  'extras_model': extras_model,
                  'extras_channel': extras_channel,
                  'versionList': versionList,
                  'params_ShowId': params_ShowId,
                  'params_DCount': params_DCount,
                  'usergroupname': usergroupname,
                  'hiddenusergroupname': hiddenusergroupname,
                  'params_DStartTime': params_DStartTime,
                  'params_DEndTime': params_DEndTime,
                  'title': title,
                  'imgUrl': imgUrl,
                  'content': content,
                  'params_ActionId': params_ActionId,
                  'linkUrl': linkUrl,
                  'skininfoname': skininfoname,
                  'hidden_skininfoname': hidden_skininfoname,
                  'skinctgname': skinctgname,
                  'hidden_skinctgname': hidden_skinctgname,
                  'bizId': bizId,
                  'osId': osId,
                  'pushSys': pushSys,
                  'issecret': issecret,
                  'actionParam': actionParam,
                  'msgType': msgType,
                  'localMsgType': localMsgType,}
        
        content_type, data = self._generate_multipart_formdata(values)
        heads = {'Content-Type': content_type,}
        page = self._post_page(url, data, heads)
        return page
        
    def _generate_multipart_formdata(self, values):
        '''
        '''
        boundary = '----------%s' % ''.join(random.sample('0123456789abcdef', 15))
        fields = []
        for k, v in values.items():
            fields.append('--' + boundary)
            fields.append('Content-Disposition: form-data; name="%s"' % k)
            fields.append('')
            fields.append(v)
        fields.append('--' + boundary + '--')
        fields.append('')
        body = '\r\n'.join(fields)
        content_type = 'multipart/form-data; boundary=%s' % boundary
        return content_type, body
        
if __name__ == '__main__':
    import time
    loginurl = 'http://ossptest.voicecloud.cn:89/auth/login'
    username = 'ydhl'
    passwd = 'ydhl'
    CL = CloudWebLib()
    CL.login_cloud_web(username, passwd)
#     print CL.get_session_id()
#     CL.add_user_group(name='TestAutoDebug', description='For Debugging', uidlist='1234567890')
#     time.sleep(2)
#     grouplist = CL.search_user_group(usergroup_name='TestAutoDebug')
#     for group in grouplist:
#         print group
#     print '===Removing===='
#     CL.remove_user_group(usergroup_name='TestAutoDebug')
#     time.sleep(2)
#     grouplist = CL.search_user_group(usergroup_name='TestAutoDebug')
#     for group in grouplist:
#         print group

#     configlist = CL.search_gray_config(text='110055')
#     for config in configlist:
#         print config
#     exceptionlist = CL.get_gray_exception_byID('126')
#     for exception in exceptionlist:
#         print exception
#     CL.add_gray_exception('110055', '1', 'TestAutoDebug')
#     CL.remove_gray_exception('110055', 'TestAutoDebug')
    msglist = CL.search_new_message()
    print msglist[0]
    CL.add_new_message(usergroupname='TestAutoDebug', title='TestAutoDebug', content='ForDebug')
    CL.remove_new_message(messageName='TestAutoDebug')