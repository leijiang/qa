#-*- coding:utf-8 -*-

from robot.api import logger
from LogParser import *
from iFly.Keyboard import Keyboard
import time
import os
import datetime
import traceback

from selenium.common.exceptions import WebDriverException

# from Report import Report
from iFly.AppiumLib import AppiumLib
"""

(C) Copyright 2016 wei_cloud@126.com

"""


class iFlyLoglib():

    def __init__(self):
        self.log = ''
        self.keylog = None
        self.appiumui = 'gui'
        self.logcat_buf = ''
        self.om = ['']
        self.orf = ['']
        self.ps = ['']
        self.try_times = 0
        self.search_logcat = ''

        self.om_all = ['']
        self.orf_all = ['']
        self.ps_all = ['']

    def set_appium_type(self, uitype):
        """
        设置Appium的模式，Appium在命令行模式和GUI模式下会输出不同的日志格式，因此需要在连接设备前指定模式

        支持模式： GUI   commandline

        example:
        |   Set Appium Type | commandline |
        """
        self.appiumui = uitype.lower()

    def get_device_log(self):
        """
        获取设备日志
        """
        driver = self._current_application()
        log = driver.get_log('logcat')
        self.log = log
#         logger.debug(log)
        return log

    def clear_device_log(self):
        """
        清空设备日志
        """
        driver = self._current_application()
        driver.get_log('logcat')
        self.keylog = None
        self.log = ''

    def get_key_log(self):
        """
        获取键盘相关日志，用于获取键盘元素的坐标
        """
        self.keylog = iFlyKeyLogList(self.get_device_log(), self.appiumui)
        return self.keylog

    def log_last_device_log(self, loglevel='INFO'):
        """
        记录最后的操作日志，一般用于测试失败时保留设置日志时使用
        """
        print("=====Last Key Log=====")
#         self._log("=====Last Key Log=====", loglevel.upper())
        try:
            for keylog in self.keylog.log:
                print keylog['message']
        except:
            pass
#         self._log(self.keylog.log, loglevel.upper())
#         self._log("=====Latest Device Log=====", loglevel.upper())
        print('\n')
        print("=====Latest Device Log=====")
        self.get_device_log()
        for log in self.log:
            print log['message']
#         self._log(self.log, loglevel.upper())
        return self.log

    def update_keyboard(self, log=None):
        """
        更新键盘布局信息。每次按键或键盘弹出时需要调用此逻辑更新键盘信息
        """
        for i in range(5):
            keylog = self.get_key_log()
            if(len(keylog) == 0):
                time.sleep(0.5)
            else:
                break
        log = log or keylog
        if not self.keyboard:
            self.keyboard = Keyboard(log)
        else:
            self.keyboard.update_ui('init', log)

    def search_device_log(self, keystr):
        """
        按关键字搜索设备日志，返回搜索到的日志列表
        | ARGS:  | keystr:  | search keyword |

        example:
        |   Search Device Log | KEY_LOCATION |
        """
        ret = []
        for log in self.log:
            if log['message'].find(keystr) != -1:
                ret.append(log)
        return ret

    def _append_device_log(self):
        """
        """
        driver = self._current_application()
        log = driver.get_log('logcat')
        self.log.extend(log)
        return log

    def get_device_log_to_buffer(self):
        self.logcat_buf = self.get_device_log()
        print 'log type:', type(self.logcat_buf), len(self.logcat_buf)
        print self.logcat_buf

    def log_marks(self):
        self.om_all = ['']
        self.ps_all = ['']
        self.orf_all = ['']

    def mark_log_print(self):
        print '-' * 20, 'KEY', '-' * 20
        for line in self.om + self.orf:
            try:
                if line.startswith('sRequst '):
                    print line.split('<request>')[1].split('<base>')[0]
                elif line.startswith('type '):
                    print line.split(', result = ')[0]
                else:
                    print line
            except:
                print 'error:', line

    def get_device_log_to_buffer_matches(self, matches=[' D OperationManager: ', ' D OperationResultFactory: ', ' D PermissionBizHelper: ']):
        """
        查找Logcat中匹配的日志，配置并解析的默认tag为：OperationManager,OperationResultFactory,PermissionBizHelper
        """

        self.try_times = 3  # 初始化重试次数
        self.logcat_buf = self.get_device_log()
        print 'log type:', type(self.logcat_buf), len(self.logcat_buf)
        self.orf, self.om, self.ps = [''], [''], ['']
        orf, om, ps = [''], [''], ['']
        for log in self.logcat_buf:
            for matche in matches:
                if matche in log['message']:
                    print log['message']
                    if(matche == ' D OperationManager: '):
                        om.append(
                            log['message'].split(' D OperationManager: ')[1])
                    elif(matche == ' D OperationResultFactory: '):
                        orf.append(
                            log['message'].split(' D OperationResultFactory: ')[1])
                    elif(matche == ' D PermissionBizHelper: '):
                        ps.append(
                            log['message'].split(' D PermissionBizHelper: ')[1])

        print '-' * 20, 'OperationManager', '-' * 20
        for line in om:
            if line.startswith('sRequst '):
                self.om.append(line)
                self.om_all.append(line)
            else:
                #                 print self.om
                self.om[-1] += line
                self.om_all[-1] += line
        for line in self.om:
            print line
            print '\n'
        print '-' * 20, 'OperationResultFactory', '-' * 20
        for line in orf:
            if line.startswith('type '):
                self.orf.append(line)
                self.orf_all.append(line)
            else:
                self.orf[-1] += line
                self.orf_all[-1] += line
        for line in self.orf:
            print line
            print '\n'
        print '-' * 20, 'PermissionBizHelper', '-' * 20
        for line in ps:
            if line.startswith('post data'):
                self.ps.append(line)
                self.om.append(line)
                self.ps_all.append(line)
                self.om_all.append(line)
        for line in self.ps:
            print line
            print '\n'
        print '-' * 20, 'KEY', '-' * 20
        for line in self.om + self.orf:
            try:
                if line.startswith('sRequst '):
                    print line.split('<request>')[1].split('<base>')[0]
                elif line.startswith('type '):
                    print line.split(', result = ')[0]
                else:
                    print line
            except:
                print 'error:', line
        '''
        print self.logcat_buf
        '''

    def _append_device_log_to_buffer_matches(self, matches=[' D OperationManager: ', ' D OperationResultFactory: ', ' D PermissionBizHelper: ']):
        """
        查找Logcat中匹配的日志，配置并解析的默认tag为：OperationManager,OperationResultFactory,PermissionBizHelper
        """
        self.logcat_buf = self.get_device_log()
        print 'log type:', type(self.logcat_buf), len(self.logcat_buf)
#         self.orf,self.om,self.ps = [''],[''],['']
        orf, om, ps = [''], [''], ['']
        for log in self.logcat_buf:
            for matche in matches:
                if matche in log['message']:
                    print log['message']
                    if(matche == ' D OperationManager: '):
                        om.append(
                            log['message'].split(' D OperationManager: ')[1])
                    elif(matche == ' D OperationResultFactory: '):
                        orf.append(
                            log['message'].split(' D OperationResultFactory: ')[1])
                    elif(matche == ' D PermissionBizHelper: '):
                        ps.append(
                            log['message'].split(' D PermissionBizHelper: ')[1])

#         print '-'*20,'OperationManager','-'*20
        for line in om:
            if line.startswith('sRequst '):
                self.om.append(line)
            else:
                #                 print self.om
                self.om[-1] += line
                self.om_all[-1] += line
#         for line in self.om:
#             print line
#             print '\n'
#         print '-'*20,'OperationResultFactory','-'*20
        for line in orf:
            if line.startswith('type '):
                self.orf.append(line)
            else:
                self.orf[-1] += line
                self.orf_all[-1] += line
#         for line in self.orf:
#             print line
#             print '\n'
#         print '-'*20,'PermissionBizHelper','-'*20
        for line in ps:
            if line.startswith('post data'):
                self.ps.append(line)
                self.om.append(line)
                self.ps_all.append(line)
                self.om_all.append(line)
#         for line in self.ps:
#             print line
#             print '\n'
        print '-' * 20, 'KEY', '-' * 20
        for line in self.om + self.orf:
            try:
                if line.startswith('sRequst '):
                    print line.split('<request>')[1].split('<base>')[0]
                elif line.startswith('type '):
                    print line.split(', result = ')[0]
                else:
                    print line
            except:
                print 'error:', line
        '''
        print self.logcat_buf
        '''

    def mark_request_log_should_contains(self, count, key):
        count = int(count)
        match_count = 0
        for om in self.om_all:
            if(key in om):
                match_count += 1
        print u'关键字', key, u'期望:', count, u'实际:', match_count
        if(match_count < count):
            raise AssertionError(u"Request Log happens times unmatch with key:%s,Except:>=%d,Actual:%d" % (
                key, count, match_count))

    def request_log_should_contains(self, key):
        is_contains = False
        for om in self.om:
            if(key in om):
                is_contains = True
                break
        if(not is_contains):
            if(self.try_times > 0):
                self.try_times = self.try_times - 1
                print 'Prepare to retry,left times are:', self.try_times
                time.sleep(12)
                self._append_device_log_to_buffer_matches()
                return self.request_log_should_contains(key)
            else:
                raise AssertionError(
                    u"Request Log not found with key:%s" % (key))

    def request_log_should_not_contains(self, key):
        print 'log type:', type(self.logcat_buf), len(self.logcat_buf)
        log = self._is_key_in_log(key, self.logcat_buf)
        if(log):
            raise AssertionError(
                u"Log Buffer can be found with keys %s" % (key))
        else:
            print log

    def mark_request_log_key_attribute_should_be(self, count, key, element, value):
        is_contains = False
        count = int(count)
        match_count = 0
        print 'Happen Count', count, u"属性:", element, u' 期望结果:', value
        for om in self.om_all:
            if(key in om):
                match_count += 1
                logitem = iFlyLogContentBase(
                    om, self.appiumui, parser=OperationRequest)
                if(element in logitem.keys()):
                    if(not logitem[element] == value):
                        raise AssertionError(
                            u"Attribute not euqals! except:%s, actual:%s" % (logitem[element], value))
                else:
                    raise AssertionError(u"Request Log happens times unmatch with key:%s,Except:>=%d,Actual:%d" % (
                        key, count, match_count))

        if(match_count < count):
            raise AssertionError(u"Request Log happens times unmatch with key:%s,Except:>=%d,Actual:%d" % (
                key, count, match_count))

    def request_log_key_attribute_should_be(self, key, element, value):
        is_contains = False
        print u"属性:", element, u' 期望结果:', value
        for om in self.om:
            if(key in om):
                logitem = iFlyLogContentBase(
                    om, self.appiumui, parser=OperationRequest)
                if(element in logitem.keys()):
                    if(not logitem[element] == value):
                        raise AssertionError(
                            u"Attribute not euqals! except:%s, actual:%s" % (logitem[element], value))
                else:
                    raise AssertionError(
                        u"Request Log not found with element:%s" % (element))
                is_contains = True
                break
        if(not is_contains):
            if(self.try_times > 0):
                self.try_times = self.try_times - 1
                print 'Prepare to retry,left times are:', self.try_times
                time.sleep(20)
                self._append_device_log_to_buffer_matches()
                return self.request_log_key_attribute_should_be(key, element, value)
            else:
                raise AssertionError(
                    u"Request Log not found with key:%s" % (key))

    def _is_keys_in_log_str(self, log, *keys):
        is_contais_keys = True
        for key in keys:
            if(key not in log):
                is_contais_keys = False
                break
        return is_contais_keys

    def mark_result_log_key_attribute_should_be(self, count, element, value, *keys):
        """
        请求日志校验：包含keys的请求日志，通过解析xml来校验字段的值
        """
        count = int(count)
        match_count = 0
        print element, value
        for orf in self.orf_all:
            if(not self._is_keys_in_log_str(orf, *keys)):
                continue
            print orf
            logitem = iFlyLogContentBase(
                orf, self.appiumui, parser=OperationResult2)
            print 'logitem', logitem
            if(element in logitem.keys()):
                match_count += 1
                print 'element:', logitem[element]
                if(not logitem[element] == value):
                    raise AssertionError(
                        u"Attribute not euqals! except:%s, actual:%s" % (logitem[element], value))
            else:
                raise AssertionError(
                    u"Result Log not found with element:%s" % (element))
        if(match_count < count):
            raise AssertionError(u"Request Log happens times unmatch with key:%s,Except:>=%d,Actual:%d" % (
                str(keys), count, match_count))

    def result_log_key_attribute_should_be(self, element, value, *keys):
        """
        请求日志校验：包含keys的请求日志，通过解析xml来校验字段的值
        """
        is_contains = False
        print element, value
        for orf in self.orf:
            if(not self._is_keys_in_log_str(orf, *keys)):
                continue
            print orf
            logitem = iFlyLogContentBase(
                orf, self.appiumui, parser=OperationResult2)
            print 'logitem', logitem
            if(element in logitem.keys()):
                print 'element:', logitem[element]
                if(not logitem[element] == value):
                    raise AssertionError(
                        u"Attribute not euqals! except:%s, actual:%s" % (logitem[element], value))
            else:
                raise AssertionError(
                    u"Result Log not found with element:%s" % (element))
            is_contains = True
            break
        if(not is_contains):
            if(self.try_times > 0):
                self.try_times = self.try_times - 1
                print 'Prepare to retry,left times are:', self.try_times
                time.sleep(20)
                self._append_device_log_to_buffer_matches()
                return self.result_log_key_attribute_should_be(element, value, *keys)
            else:
                raise AssertionError(
                    u"Result Log not found with keys:" + str(keys))

    def mark_result_log_key_attribute_should_in(self, count, element, value, *keys):
        count = int(count)
        match_count = 0
        print u"属性:", element, u' 期望结果:', value.replace('|', ' or ')
        for orf in self.orf_all:
            if(not self._is_keys_in_log_str(orf, *keys)):
                continue
            print orf
            logitem = iFlyLogContentBase(
                orf, self.appiumui, parser=OperationResult2)
            if(element in logitem.keys()):
                match_count += 1
                print 'element:', logitem[element]
                # 修改为包含关系
                if(logitem[element] not in value.split('|')):
                    raise AssertionError(u"Attribute not include! except:%s, actual:%s" % (
                        logitem[element], ' or '.join(value.spllit('|'))))
            else:
                raise AssertionError(
                    u"Result Log not found with element:%s" % (element))
        if(match_count < count):
            raise AssertionError(u"Request Log happens times unmatch with key:%s,Except:>=%d,Actual:%d" % (
                str(keys), count, match_count))

    def result_log_key_attribute_should_in(self, element, value, *keys):
        is_contains = False
        print u"属性:", element, u' 期望结果:', value.replace('|', ' or ')
        for orf in self.orf:
            if(not self._is_keys_in_log_str(orf, *keys)):
                continue
            print orf
            logitem = iFlyLogContentBase(
                orf, self.appiumui, parser=OperationResult2)
            if(element in logitem.keys()):
                print 'element:', logitem[element]
                # 修改为包含关系
                if(logitem[element] not in value.split('|')):
                    raise AssertionError(u"Attribute not include! except:%s, actual:%s" % (
                        logitem[element], ' or '.join(value.spllit('|'))))
            else:
                raise AssertionError(
                    u"Result Log not found with element:%s" % (element))
            is_contains = True
            break
        if(not is_contains):
            if(self.try_times > 0):
                self.try_times = self.try_times - 1
                print 'Prepare to retry,left times are:', self.try_times
                time.sleep(20)
                self._append_device_log_to_buffer_matches()
                return self.result_log_key_attribute_should_in(element, value, *keys)
            else:
                raise AssertionError(
                    u"Result Log not found with keys:" + str(keys))

    def mark_result_log_should_contains(self, count, *keys):
        count = int(count)
        match_count = 0
        for key in keys:
            for orf in self.orf_all:
                if(key in orf):
                    match_count += 1
        if(match_count < count):
            raise AssertionError(u"Request Log happens times unmatch with key:%s,Except:>=%d,Actual:%d" % (
                str(keys), count, match_count))

    def result_log_should_contains(self, *keys):
        is_contains = False
        for key in keys:
            for orf in self.orf:
                if(key in orf):
                    is_contains = True
                    break
            if(not is_contains):
                if(self.try_times > 0):
                    self.try_times = self.try_times - 1
                    print 'Prepare to retry,left times are:', self.try_times
                    time.sleep(20)
                    self._append_device_log_to_buffer_matches()
                    return self.result_log_should_contains(*keys)
                else:
                    raise AssertionError(
                        u"Result Log not found with key:%s" % (key))
        '''
        is_contains = False 
        for orf in self.orf:
            if(key in orf):
#                 logitem = iFlyLogContentBase(orf, self.appiumui, parser=OperationRequest)
                is_contains = True
                break
        if(not is_contains):
            raise AssertionError(u"Result Log not found with key:%s"%(key))
        '''

    def assert_content_equals(self, content_actual, content_expect):
        if(not content_actual.equals(content_expect)):
            raise AssertionError(
                u"Assert Equal Failed! expect:%s, actual:%s" % (content_expect, content_actual))

    def assert_content_not_empty(self, content):
        print 'content is:', content
        if(not content):
            raise AssertionError(u"Assert Not Empty Failed!")

    def wait_until_log_contains(self, *keys, **kws):
        """
        等待特定日志出现
        | ARGS:  | keys:  | 搜索关键字列表，可输入多个  |
        |        | kws:   | 可用于指定超时时间，单位ms，例如：timeout=1200 |

        example:
        |   Wait Until Log Contains | KEY_LOCATION | timeout=2000
        |   Wait Until Log Contains | OperationManager | sRequst | timeout=2000
        """
        start = time.time()
        timeout = int(kws.get('timeout', 2000))
        log = self.get_device_log()

        while not self._is_keys_in_log(keys, log):
            end = time.time()
            if (end - start) * 1000 > timeout:
                raise AssertionError(
                    u"Log can not be found with keys %s after %s ms" % (keys, timeout))
            time.sleep(0.2)
            log = self._append_device_log()
        print 'self.log:', log
        return self.log

    def _is_keys_in_log(self, keys, loglist):
        for log in loglist:
            for key in keys:
                key_in_log = True
                if key not in log['message']:
                    key_in_log = False
                    break
            if key_in_log:
                return log
        return False

    def _is_key_in_log(self, key, loglist):
        for log in loglist:
            key_in_log = False
            if key in log['message']:
                return log
        return False

    def wait_until_key_contains(self, key, attr=None, value=None, timeout=2000):
        """
        等待按键出现或按键状态变化

        example:
        |   Wait Until Key Contains | pinyin_cloud |
        """
        start = time.time()
        self.update_keyboard()
        while not self.keyboard.key_map.has_key(key) \
                and (attr != None and self.get_key_attribute(key, attr) != value):
            end = time.time()
            if (end - start) * 1000 > int(timeout):
                raise AssertionError(
                    u"Key log can not be found with key %s after %s ms" % (key, timeout))
            time.sleep(0.2)
            self._append_device_log()
            keylog = iFlyKeyLogList(self.log, self.appiumui)
            self.update_keyboard(keylog)

    def keyboard_layout_should_be(self, method=None, layout=None, panel=None):
        """
        检查键盘布局
        | ARGS:  | method:  | 拼音, 英文, 笔画, 手写, 数字 |
        |        | layout:  | 9键, 26键, 双键, 笔画, 全屏手写, 半屏手写, 9键横屏, 笔画横屏 |
        |        | panel:   | main, more, speech, digit, symbol, edit, emotion, abc, more_bh |
        |        | See all supported type in KeyIdMap.py |   |

        example:
        |   Keyboard Layout Should Be | method=拼音 | layout=9键 | panel=main |
        |   Keyboard Layout Should Be | layout=26键  |
        """
        self.update_keyboard()
        actual = self.keyboard.get_keyboard_layout()
        if (method and method != actual['method']) or \
           (layout and layout != actual['layout']) or \
           (panel and panel != actual['panel']):
            raise AssertionError(u'Keyboard Layout not match! Got %s, %s, %s. Expect %s, %s, %s'
                                 % (actual['method'], actual['layout'], actual['panel'], method, layout, panel))

    def get_keyboard_layout(self):
        self.update_keyboard()
        actual = self.keyboard.get_keyboard_layout()
        return ''.join([actual['method'], actual['layout'], actual['panel']])

    def get_candidates(self):
        """
        获取候选字列表，返回候选字list

        example:
        |   Get Candidates |
        """
        return [item.text for item in self.keylog.get_keys('candidate_key')]

    def candidates_should_be(self, *args):
        """
        检查候选字，按输入顺序检查， 可同时检查1个或多个
        | ARGS:  | list of candidates |

        example:
        |   Candidates Should Be | 我 | 玩 | 问 | 晚 | 
        """
        candidates = self.get_candidates()
        for i in range(len(args)):
            if args[i] != candidates[i]:
                raise AssertionError(
                    'Candidate at index %s should be %s but got %s!' % (i, args[i], candidates[i]))

    def candidates_in_index_should_contain(self, word, index):
        candidates = self.get_candidates()
        for i in range(int(index)):
            if word == candidates[i]:
                break
            elif i == (int(index) - 1):
                raise AssertionError(
                    'Candidate in index %s should contain %s but not got!' % (index, word))

    def candidates_at_index_should_be(self, word, index):
        """
        检查候选字，检查指定位置的候选字
        | ARGS: |  word:  | expected candidate word |
        |       | index:  | candidate index, start from 1 |

        example:
        |   Candidates at Index Should Be | 我 | 1 |
        """
        candidates = self.get_candidates()
        if candidates[int(index) - 1] != word:
            raise AssertionError('Candidate at index %s should be %s but got %s!' % (
                index, word, candidates[index]))

    def first_candidate_is_chinese(self):
        """
        检查候选字首位为中文候选项                      WYF
        example:
        |   First Candidate Is Chinese |
        """
        candidates = self.get_candidates()
        candidate = candidates[0]
        if candidate >= u'\u4e00' and candidate <= u'\u9fa5':
            return True
        else:
            raise AssertionError(
                'First candidate should be Chinese but it is not!')

    def get_candidate_index(self, word, num):
        """
        返回候选字在列表中的位置                                              WYF
        | ARGS: |  word:  | expected candidate word |
        |       | num:  | candidate range, start from 1 |

        example:
        |   Get Candidate Index | 我 | 20 |
        """
        candidates = self.get_candidates()
        for i in range(1, int(num)):
            if candidates[i - 1] == word:
                return i
        raise AssertionError(
            'In the first %s candidates does not include %s!' % (num, word))

    def candidates_should_contain(self, word):
        """
    检查候选字，检查候选字列表中是否有指定的字
        | ARGS: |  word: |  expected candidate word |

        example:
        |   Candidates Should Contain | 我  |
        """
        candidates = self.get_candidates()
        if word not in candidates:
            raise AssertionError(
                'Candidate %s not exist in %s!' % (word, str(candidates)))

    def candidates_should_not_contain(self, word):
        """
        检查候选字，检查候选字列表中没有指定的字
        | ARGS: |  word:  | expected candidate word |

        example:
        |   Candidates Should Not Contain | 我  |
        """
        candidates = self.get_candidates()
        if word in candidates:
            raise AssertionError(
                'Candidate %s should not exist in %s!' % (word, str(candidates)))

    def get_combinations(self):
        """
        获取拼音组合选项，返回可能的组合列表
        """
        return [item.text for item in self.keylog.get_keys('combination_key')]

    def combinations_should_be(self, *args):
        """
        检查拼音组合，按输入顺序检查
        | ARGS: |  list of combinations |

        example:
        |   Combinations Should Be | A | B | C |
        """
        combinations = self.get_combinations()
        for i in range(len(args)):
            if args[i] != combinations[i]:
                raise AssertionError(
                    'Candidate at index %s should be %s but got %s!' % (i, args[i], combinations[i]))

    def combinations_at_index_should_be(self, word, index):
        """
        检查拼音组合，检查指定位置的拼音组合
        | ARGS: |  word: |  expected combination word |
        |       | index: | combination index, start from 1 |

        example:
        |   Combinations at Index Should Be | A | 1 |
        """
        combinations = self.get_combinations()
        if combinations[int(index) - 1] != word:
            raise AssertionError('Candidate at index %s should be %s but got %s!' % (
                index, word, combinations[index]))

    def combinations_should_contain(self, word):
        """
        检查拼音组合，检查拼音组合列表中是否有指定的字母
        | ARGS: |  word: |  expected combination word |

        example:
        |   Combinations Should Contain | A |
        """
        combinations = self.get_combinations()
        if word not in combinations:
            raise AssertionError(
                'Candidate %s not exist in %s!' % (word, str(combinations)))

    def combinations_should_not_contain(self, word):
        """
        检查拼音组合，检查拼音组合列表中没有指定的字母
        | ARGS:  | word: |  expected combination word |

        example:
        |   Combinations Should Not Contain | A |
        """
        combinations = self.get_combinations()
        if word in combinations:
            raise AssertionError(
                'Candidate %s should not exist in %s!' % (word, str(combinations)))

    def get_key_attribute(self, keystr, attrname):
        """
        获取按键属性
        |       | attrname: |  属性名称：    model, type, left, top, right, bottom, text, id, shown, add |
        """
        return self.keyboard.get_key_attribute(keystr, attrname)

    def key_attribute_should_be(self, keystr, attrname, value):
        """
        检查按键的属性值
        | ARGS: |  keystr:  | 键值，请参考 Keyboard Press 关键字 |
        |       | attrname: |  属性名称：    model, type, left, top, right, bottom, text, id, shown, add, highlight, reddot |
        |       | value:    | 期望的属性值 |

        example:
        |   Key Attribute Should Be | A | shown | true |
        """
        v = self.keyboard.get_key_attribute(keystr, attrname)
        if not isinstance(v, basestring):
            v = str(v)
        if v != value:
            raise AssertionError(u"Key %s attribute %s not equal! Should be %s, but got %s" % (
                keystr, attrname, value, v))

    def key_attribute_should_not_be(self, keystr, attrname, value):
        """
        检查按键的属性值，请参考 Key Attribute Should Be 关键字

        example:
        |   Key Attribute Should Not Be | A | shown | true |
        """
        v = self.keyboard.get_key_attribute(keystr, attrname)
        if not isinstance(v, basestring):
            v = str(v)
        if v == value:
            raise AssertionError(
                u"Key %s attribute %s Should not equal! Got %s" % (keystr, attrname, v))

    def get_useful_expressions(self):
        """
        获取常用语列表
        """
        return [item.text for item in self.keylog.get_keys('userphrase_content_key')]

    def useful_expression_should_contain(self, exp):
        """
        检查常用语
        """
        expressions = self.get_useful_expressions()
        if exp not in expressions:
            raise AssertionError(
                'Useful expression %s not exist in %s!' % (exp, str(expressions)))

    def useful_expression_should_not_contain(self, exp):
        """
        检查常用语
        """
        expressions = self.get_useful_expressions()
        if exp in expressions:
            raise AssertionError(
                'Useful expression %s should not exist in %s!' % (exp, str(expressions)))

    def clear_userful_expression(self):
        """
        清空常用语
        """
        while self.get_useful_expressions():
            self.keyboard_press('expend_1', u'delete')

    def get_pinyin_cloud(self):
        """
        获取云拼音组合选项，返回可能的组合列表
        """
        return [item.text for item in self.keylog.get_keys('pinyin_cloud')]

    def pinyin_cloud_should_be(self, *args):
        """
        检查云拼音组合，按输入顺序检查
        | ARGS: |  list of candidates |

        example:
        |   Pinyin Cloud Should Be | A | B | C |
        """
        pinyin_cloud = self.get_pinyin_cloud()
        for i in range(len(args)):
            if args[i] != pinyin_cloud[i]:
                raise AssertionError(
                    'Candidate at index %s should be %s but got %s!' % (i, args[i], pinyin_cloud[i]))

    def pinyin_cloud_should_displayed(self):
        """
        检查云拼音是否显示
        """
        pinyin_cloud = self.get_pinyin_cloud()
        if len(pinyin_cloud) < 1:
            raise AssertionError('Cloud Pinyin Candidates not found!')

    def pinyin_cloud_should_not_displayed(self):
        """
        检查云拼音是否显示
        """
        pinyin_cloud = self.get_pinyin_cloud()
        if len(pinyin_cloud) > 0:
            raise AssertionError('Cloud Pinyin Should no displayed!')

    def get_uid_from_log(self, logs=None):
        """
        从日志中获取UID
        """
        logs = logs or self.log
        log = self._is_keys_in_log(['OperationManager', 'sRequst'], logs)
        if log:
            logitem = iFlyLogBase(log, self.appiumui, parser=OperationRequest)
            return logitem['uid']
        raise AssertionError("uid can not found in the log")

    def get_close_search_candidate_location(self, logs=None):
        """
        关闭搜索导流临时悬浮窗
        """
        matche = 'search_top_window_close'
        start = 'start'
        device_log = self.get_device_log()
        i = len(device_log) - 1
        keylog_found = False
        while i >= 0:
            log = device_log[i]
            message = log['message']
            if matche in message:
                print message
                l = message.index('{')
                r = message.index('}')
                location = message[l + 1:r]
                list = location.strip().split(',')
                for type in list:
                    eve = type.strip().split(':')
                    if eve[0] == 'left':
                        left = int(eve[1])
                    if eve[0] == 'right':
                        right = int(eve[1])
                    if eve[0] == 'top':
                        top = int(eve[1])
                    if eve[0] == 'bottom':
                        bottom = int(eve[1])
                keylog_found = True
                i -= 1
                continue
            if keylog_found and start in message:
                print message
                l = message.index('{')
                r = message.index('}')
                location = message[l + 1:r]
                list = location.strip().split(',')
                for type in list:
                    eve = type.strip().split(':')
                    if eve[0] == 'left':
                        kleft = int(eve[1])
                    if eve[0] == 'right':
                        kright = int(eve[1])
                    if eve[0] == 'top':
                        ktop = int(eve[1])
                    if eve[0] == 'bottom':
                        kbottom = int(eve[1])
                break
            i -= 1
        if keylog_found == False:
            raise AssertionError('Close Search Candidate not found!')
        else:
            x = left + (right - left) / 2 + kleft
            y = top + (bottom - top) / 2 + ktop
        return x, y

    def get_search_candidate_log(self):
        self.clear_search_candidate_log()
        self.search_logcat = self.get_device_log()
        print self.search_logcat

    def clear_search_candidate_log(self):
        self.search_logcat = ''
        print self.search_logcat

    def search_candidate_present(self, key):
        """
        判断搜索导流key是否出现
        """
        searchmap = {u'title': u'search_top_window_title',
                     u'detail': u'search_top_window_detail',
                     u'menu': u'search_top_window_menu',
                     u'topclose': u'search_top_window_close',
                     u'confirm': u'search_top_window_confirm_setting',
                     u'icon': u'search_temp_icon',
                     u'temptextl': u'search_temp_text_l',
                     u'temptextr': u'search_temp_text_r',
                     u'tempclose': u'search_temp_close'}
        matche = searchmap.get(key)
        device_log = self.search_logcat
        i = len(device_log) - 1
        keylog_found = False
        while i >= 0:
            log = device_log[i]
            message = log['message']
            if matche in message:
                l = message.index('{')
                r = message.index('}')
                location = message[l + 1:r]
                list = location.strip().split(',')
                shown = ''
                for type in list:
                    eve = type.strip().split(':')
                    if eve[0] == 'shown':
                        shown = eve[1]
                        break
                if shown == 'true':
                    keylog_found = True
                    break
                else:
                    i -= 1
            else:
                i -= 1
        return keylog_found

    def get_search_candidate_text(self, key):
        """
        获取搜索导流key的text属性
        """
        searchmap = {u'title': u'search_top_window_title',
                     u'detail': u'search_top_window_detail',
                     u'menu': u'search_top_window_menu',
                     u'topclose': u'search_top_window_close',
                     u'confirm': u'search_top_window_confirm_setting',
                     u'icon': u'search_temp_icon',
                     u'temptextl': u'search_temp_text_l',
                     u'temptextr': u'search_temp_text_r',
                     u'tempclose': u'search_temp_close'}
        matche = searchmap.get(key)
        device_log = self.search_logcat
        i = len(device_log) - 1
        stext = 'null'
        while i >= 0:
            log = device_log[i]
            message = log['message']
            print message
            if matche in message:
                l = message.index('{')
                r = message.index('}')
                location = message[l + 1:r]
                list = location.strip().split(',')
                for type in list:
                    eve = type.strip().split(':')
                    if eve[0] == 'text':
                        stext = eve[1]
                        break
                break
            else:
                i -= 1
        if stext == 'null':
            raise AssertionError(matche + ' not found!')
        else:
            return stext

    def get_search_candidate_key(self, key):
        """
        获取搜索导流各按键坐标
        """
        searchmap = {u'title': u'search_top_window_title',
                     u'detail': u'search_top_window_detail',
                     u'menu': u'search_top_window_menu',
                     u'topclose': u'search_top_window_close',
                     u'confirm': u'search_top_window_confirm_setting',
                     u'icon': u'search_temp_icon',
                     u'temptextl': u'search_temp_text_l',
                     u'temptextr': u'search_temp_text_r',
                     u'tempclose': u'search_temp_close'}
        matche = searchmap.get(key)
        start = 'start'
        device_log = self.search_logcat
        print device_log
        i = len(device_log) - 1
        keylog_found = False
        while i >= 0:
            log = device_log[i]
            message = log['message']
            if matche in message:
                print message
                l = message.index('{')
                r = message.index('}')
                location = message[l + 1:r]
                list = location.strip().split(',')
                for type in list:
                    eve = type.strip().split(':')
                    if eve[0] == 'left':
                        left = int(eve[1])
                    if eve[0] == 'right':
                        right = int(eve[1])
                    if eve[0] == 'top':
                        top = int(eve[1])
                    if eve[0] == 'bottom':
                        bottom = int(eve[1])
                keylog_found = True
                i -= 1
                continue
            if keylog_found and start in message:
                print message
                l = message.index('{')
                r = message.index('}')
                location = message[l + 1:r]
                list = location.strip().split(',')
                for type in list:
                    eve = type.strip().split(':')
                    if eve[0] == 'left':
                        kleft = int(eve[1])
                    if eve[0] == 'right':
                        kright = int(eve[1])
                    if eve[0] == 'top':
                        ktop = int(eve[1])
                    if eve[0] == 'bottom':
                        kbottom = int(eve[1])
                break
            i -= 1
        if keylog_found == False:
            raise AssertionError(matche + ' not found!')
        else:
            x = left + (right - left) / 2 + kleft
            y = top + (bottom - top) / 2 + ktop
        return x, y

    def swipe_temp_search_candidate(self, duration=200):
        """
        滑动临时悬浮窗
        """
        tx, ty = self.get_search_candidate_key('icon')
        try:
            self.swipe(tx, ty, tx, ty + 30, duration)
        except WebDriverException:
            logger.warn('The swipe did not complete successfully')

    def clear_errlog_file(self):
        """ 
       清空错误日志存储信息
        """
        logdir = self._get_log_dir()
        print logdir

        filepath = logdir + '/' + 'errlog.txt'
        if os.path.exists(filepath):
            os.remove(filepath)
            print(filepath + " deleted")
        file = open(filepath, 'w')
        file.close()
        print filepath + " created."

    def save_log_message(self, message):
        """ 
       写入日志信息
        """
        logdir = self._get_log_dir()
        print logdir
        filepath = logdir + '/' + 'errlog.txt'

        file = open(filepath, 'a')
        file.write(message)
        file.write("\n")
        file.close()

    def get_uid_from_device_storage(self, logs=None):
        """
        从日志中获取UID
        """
        logs = self.get_device_log()
        log = self._is_keys_in_log(
            ['ControlService', 'iflytek_ime_uid ='], logs)
        print log
        if(log):
            print log["message"]
            msg = log["message"]
            print msg.split(' =')
            print msg.split(' =')[1]
            return msg.split(' =')[1].strip()
        else:
            return ""

    def list_to_string(self, list):
        strs = ""
        for str in list:
            if len(str) != 0:
                strs += str
                strs += ','
        return strs[:-1]

    def two_list_string(self, list1, list2):
        strs = ""
        for i in range(len(list1)):
            if len(list1[i]) != 0:
                strs += list1[i] + ': ' + list2[i]
                strs += '<br>'
        print strs
        return strs[:-4]

    def analysis_log_message(self, curpath):
        """ 
       解析本地日志信息
        """
        logdir = self._get_log_dir()
        filepath = logdir + '/' + 'errlog.txt'
        file_object = open(filepath, 'r')
        try:
            all_the_text = file_object.readlines()
        finally:
            file_object.close()
        allPanel, truePanel, falsePanel = [''], [''], ['']
        alreadyPanel, abnormalPanel = [''], ['']
        errParsed, notFound, textEmpty, notInit = [''], [''], [''], ['']
        errMes, foundMes, emptyMes, initMes = [''], [''], [''], ['']
        i = len(all_the_text) - 1
        status = 'FAIL'
        flag = 0
        findstatus = 'false'
        abnstatus = 'false'
        findflag = 0
        while i >= 0:
            print all_the_text[i]
            if 'status' in all_the_text[i]:
                flag = 1
                index = i
                if all_the_text[i].find('PASS') != -1:
                    status = 'PASS'
                else:
                    status = 'FAIL'
            elif 'tag' in all_the_text[i] and flag == 1:
                flag = 0
                list = all_the_text[i].strip().split(':')
                pannel = list[-1]
                ##
                if pannel in allPanel:
                    findflag = 1
                    if findstatus == 'true':
                        i -= 1
                        continue
                    elif abnstatus == 'false':
                        i -= 1
                        continue
                    else:
                        abnormalPanel.remove(pannel)
                else:
                    findflag = 0
                    allPanel.append(pannel)

                if status == 'PASS':
                    findstatus = 'true'
                    truePanel.append(pannel)
                    alreadyPanel.append(pannel)
                else:
                    findstatus = 'false'
                    falsePanel.append(pannel)
                    if i == index - 1:
                        if pannel not in abnormalPanel:
                            abnormalPanel.append(pannel)
                    else:
                        j = i + 1
                        inflag = 0
                        while j < index:
                            if pannel in all_the_text[j]:
                                inflag = 1
                                j += 1
                                if j == index:
                                    abnstatus = 'true'
                                    if pannel not in abnormalPanel:
                                        abnormalPanel.append(pannel)
                                    break
                                continue
                            elif inflag == 1 and 'format error' in all_the_text[j]:
                                abnstatus = 'false'
                                inflag = 0
                                errParsed.append(pannel)
                                alreadyPanel.append(pannel)
                                list1 = all_the_text[j].strip().split('{')
                                errMes.append(list1[-1].strip().split('}')[0])
                                break
                            elif inflag == 1 and 'not found' in all_the_text[j]:
                                abnstatus = 'false'
                                inflag = 0
                                notFound.append(pannel)
                                alreadyPanel.append(pannel)
                                foundMes.append(all_the_text[j].strip())
                                break
                            elif inflag == 1 and 'not empty' in all_the_text[j]:
                                abnstatus = 'false'
                                inflag = 0
                                textEmpty.append(pannel)
                                alreadyPanel.append(pannel)
                                list1 = all_the_text[j].strip().split('{')
                                emptyMes.append(list1[-1].strip()[:-1])
                                break
                            elif inflag == 1 and 'not initialized' in all_the_text[j]:
                                abnstatus = 'false'
                                inflag = 0
                                notInit.append(pannel)
                                alreadyPanel.append(pannel)
                                initMes.append(all_the_text[j].strip())
                                break
                            elif j == index - 1:
                                abnstatus = 'true'
                                if pannel not in abnormalPanel:
                                    abnormalPanel.append(pannel)
                                break
                            else:
                                j += 1

            i -= 1
        print 'truePanel', truePanel
        print 'falsePanel', falsePanel
        print 'abnormalPanel', abnormalPanel
        print 'errParsed', errParsed
        print 'notFound', notFound
        print 'textEmpty', textEmpty
        print 'notInit', notInit
        if len(errParsed) > 1:
            errresult = u'失败'
        else:
            errresult = u'成功'
        if len(notFound) > 1:
            foundresult = u'失败'
        else:
            foundresult = u'成功'
        if len(notInit) > 1:
            initresult = u'失败'
        else:
            initresult = u'成功'
        if len(textEmpty) > 1:
            emptyresult = u'失败'
        else:
            emptyresult = u'成功'
        adr_send = ''
        if errresult == '成功' and foundresult == '成功' and initresult == '成功' and emptyresult == '成功':
            if len(abnormalPanel) == 1:
                result = u'通过'
            else:
                result = u'校验不完全'
                adr_send = 'yfwang13@iflytek.com'
        else:
            result = u'失败'
            adr_send = 'yfwang13@iflytek.com'
        version = AppiumLib().obtain_apk_version()
#         curtime = strftime("%Y-%m-%d %H:%M:%S", gmtime())

        now = datetime.datetime.now()
        curtime = now.strftime('%Y-%m-%d %H:%M:%S')
        message = curtime + '        ' + version + '        ' + result
        print message
        print curpath
        curdir = curpath + '/' + 'ExecuteNotes.txt'
        print curdir
        if os.path.exists(curdir):
            pass
        else:
            file = open(curdir, 'w')
            file.close()
            print curdir + " created."
        file = open(curdir, 'a')
        file.write(message)
        file.write("\n")
        file.close()
        if len(adr_send) != 0:
            Report().sendLogCheckResult(version, adr_send, result, self.list_to_string(alreadyPanel), self.list_to_string(abnormalPanel),
                                        errresult, self.two_list_string(errParsed, errMes), foundresult, self.two_list_string(notFound, foundMes), initresult, self.two_list_string(notInit, initMes), emptyresult, self.two_list_string(textEmpty, emptyMes))
