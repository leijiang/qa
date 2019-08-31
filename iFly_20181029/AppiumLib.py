#-*- coding: UTF-8 -*-
"""

(C) Copyright 2016 wei_cloud@126.com

"""
from AppiumLibrary import AppiumLibrary
import os
import time
import subprocess
from appium.webdriver.common.touch_action import TouchAction
from robot.api import logger
from selenium.common.exceptions import TimeoutException, WebDriverException
from LogParser import iFlyKeyLogList
from datetime import datetime, timedelta
from wx import Height
from robot.libraries.BuiltIn import BuiltIn
from socket import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

import traceback


class AppiumLib(AppiumLibrary):

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = '0.1.0'

    def __init__(self, timeout=5, run_on_failure='Capture Page Screenshot'):
        AppiumLibrary.__init__(self, timeout, run_on_failure)
        self.keyboard = None
        self.keypress_interval = 0.5
        self.log = ''
        self.device_id = ''
        self.remoteurl = ''
#         self.device_id = BuiltIn().get_variable_value("${UDID}")
#         self.apppackage = BuiltIn().get_variable_value("${APPPACKAGE}")
#         self.remoteurl = BuiltIn().get_variable_value("${SERVERURL}", '')
#         self.capturepath = BuiltIn().get_variable_value("${CAPPATH}")
#         self.skinname = BuiltIn().get_variable_value("${SKINNAME}")
#         self.layout = BuiltIn().get_variable_value("${LAYOUT}")

    def open_application(self, remote_url, alias=None, **kwargs):
        """Opens a new application to given Appium server.
        Capabilities of appium server, Android and iOS,
        Please check http://appium.io/slate/en/master/?python#appium-server-capabilities
        | *Option*            | *Man.* | *Description*     |
        | remote_url          | Yes    | Appium server url |
        | alias               | no     | alias             |

        Examples:
        | Open Application | http://localhost:4723/wd/hub | alias=Myapp1         | platformName=iOS      | platformVersion=7.0            | deviceName='iPhone Simulator'           | app=your.app                         |
        | Open Application | http://localhost:4723/wd/hub | platformName=Android | platformVersion=4.2.2 | deviceName=192.168.56.101:5555 | app=${CURDIR}/demoapp/OrangeDemoApp.apk | appPackage=com.netease.qa.orangedemo | appActivity=MainActivity |
        """

        for k in kwargs.keys():
            if not kwargs[k]:
                kwargs.pop(k)
                logger.info(k)
        self.remoteurl = BuiltIn().get_variable_value("${SERVERURL}", '')
        self.device_id = BuiltIn().get_variable_value("${UDID}")
        self.apppackage = BuiltIn().get_variable_value("${APPPACKAGE}")
        self.remoteurl = BuiltIn().get_variable_value("${SERVERURL}", '')
        self.capturepath = BuiltIn().get_variable_value("${CAPPATH}")

        if len(self.remoteurl) == 0:
            self.remoteurl = "http://localhost:4723/wd/hub"

        logger.info("****************")
        logger.info(self.remoteurl)
        AppiumLibrary.open_application(self, self.remoteurl, alias, **kwargs)

    def reset_application(self, appPackage=None):
        """ Reset application """
        driver = self._current_application()
        driver.reset(appPackage)

    def install_app(self, app_path):
        """Install the application found at `app_path` on the device.

        :Args:
         - app_path - the local or remote path to the application to install
        """
        driver = self._current_application()
        driver.install_app(app_path)

    def delete_phone_file(self, device, path):
        """Delete The File of `path` on the `path`.

        :Args:
         - path - the path in the device
         example:
        |   Delete Phone File | /sdcard/iflyime/st_map.zip
        """
        cmd = "adb -s %s shell rm -rf %s" % (device, path)
        os.system(cmd)

    def set_wifi_data_connection_status(self, device, connectionStatus):
        """Sets the network connection Status Of device.

        Android only.

        Possible values:
            | =Value= | =Alias=          | =Data= | =Wifi= | =Airplane Mode=  |
            |  0      | (None)           | 0      |   0    | 0                |
            |  1      | (Airplane Mode)  | 0      |   0    | 1                |
            |  2      | (Wifi only)      | 0      |   1    | 0                |
            |  4      | (Data only)      | 1      |   0    | 0                |
            |  6      | (All network on) | 1      |   1    | 0                |
        """
        print "In the Method"
        network_code = {"0": [("wifi", "disable"), ("data", "disable")],
                        "2": [("wifi", "enable"), ("data", "disable")],
                        "4": [("wifi", "disable"), ("data", "enable")],
                        "6": [("wifi", "enable"), ("data", "enable")]}
        network_status = network_code.get(connectionStatus)
        print network_status
        if not network_status:
            return
        for item in network_status:
            os.system("adb -s %s shell \"su -c 'svc %s %s'\"" %
                      (device, item[0], item[1]))
            time.sleep(3)
            print "set succeed"

    def try_into_settings(self, device, subsetting):
        """Try To Into The System Setting Via [adb shell am] Command.

        Android only.

        Possible values:
            | =Subsetting=     | =Alias=        |
            |  Security       | 安全设置       |
            |  Setting        | 系统设置       |
            |  Sound          | 声音设置       |
            |  Battery        | 电池信息       |
            |  Date           | 时间和日期     |
            |  Display        | 显示设置       |
            |  Language      | 语言及输入法设置 |
            |  Running      | 正在运行的任务    |
            |  DM      | 设备管理器    |

        """

        subsettings = {"Security": "SecuritySettings",
                       "Setting": "Settings",
                       "Sound": "SoundSettings",
                       "Battery": "BatteryInfo",
                       "Date": "DateTimeSettingsSetupWizard",
                       "DM": "DeviceAdminSettings",
                       "Display": "DisplaySettings",
                       "Language": "LanguageSettings",
                       "Running": "RunningServices"}
        cmd_parent = "adb -s %s shell am start -n com.android.settings/com.android.settings.%s" % (
            device, subsettings.get(subsetting, "Settings"))
        print cmd_parent
        os.system(cmd_parent)

    def is_icon_not_exist(self, device, pkgname):
        """Try To Get The Desktop Icon of `pkgname` on the device via dumpsys package.

        :Args:
         - pkgname - the target test packagename
        """
        results = os.popen(
            "adb -s %s shell dumpsys package %s" % (device, pkgname)).readlines()
        import re
        cmpstr = ""
        for i in range(len(results)):
            if re.search("%s/.LauncherActivity" % pkgname, results[i]):
                cmpstr = ",".join(results[i + 1:i + 4])
                break
        if len(results) == 0:
            results = os.popen(
                "adb -s %s shell dumpsys package com.iflytek.inputmethod.gionee" % device).readlines()
            for i in range(len(results)):
                if re.search(r"com.iflytek.inputmethod.gionee/.LauncherActivity", results[i]):
                    cmpstr = ",".join(results[i + 1:i + 4])
                    break
        print cmpstr
        if re.search("android.intent.action.MAIN", cmpstr) \
                and re.search("android.intent.category.LAUNCHER", cmpstr) \
                and re.search("android.intent.category.DEFAULT", cmpstr):
            return False
        return True

    def clear_ime_data(self, device, pkgname="com.iflytek.inputmethod"):
        """Clear the pakage Data via adb command,Default Assignate to com.iflytek.inputmethod
        Example:
        | Clear Ime Data |  ${UDID} |
        | Clear Ime Data |  ${UDID} |  com.iflytek.inputmethod |
        """
        cmd = "adb -s %s shell pm clear %s" % (device, pkgname)
        print cmd
        os.system(cmd)

    def set_ime_engine(self, device, engine="com.iflytek.inputmethod/.FlyIME"):
        """
        将输入法设置成默认输入法
        | ARGS:  | engine:  | 输入法引擎 |
        example:
        |   Set Ime Engine | com.iflytek.inputmethod/.FlyIME |
        """
        cmd = "adb -s %s shell ime set %s" % (device, engine)
        print cmd
        os.system(cmd)

    def start_launch_activity(self, device, launchactivity="com.iflytek.inputmethod/.LauncherActivity"):
        """Start The Assignate Activity via adb shell am
        Example:
        | Start Launch Activity |  ${UDID} |
        | Start Launch Activity |  ${UDID} |  com.iflytek.inputmethod/.LauncherActivity |
        """
        cmd = "adb -s %s shell am start -n %s" % (device, launchactivity)
        print cmd
        os.system(cmd)

    def remove_application(self, application_id):
        """Remove the application that is identified with an application id

        Example:
        | Remove Application |  com.netease.qa.orangedemo |
        """

        AppiumLibrary.remove_application(self, application_id)

    def swipe_timePicker_up(self,locator,duration):
        location = self.get_element_location(locator)

        self.swipe(location['x'], location['y'], location['x'], location['y'] - 200, duration)
        

    def swipe_up(self, duration=1000):
        """
        向上滑屏
        | ARGS:  |  duration:  |  滑动持续时间，默认1s，单位ms |

        example:
        |   Swipe Up |
        |   Swipe Up | 1000 |
        """
        driver = self._current_application()
        sizedict = driver.get_window_size()
        self.swipe(sizedict['width'] / 2, sizedict['height'] * 3 /
                   4, sizedict['width'] / 2, sizedict['height'] / 4, duration)

    def swipe_down(self, duration=1000):
        """
        向下滑屏
        | ARGS:  | duration:  | 滑动持续时间，默认1s，单位ms |
        """
        driver = self._current_application()
        sizedict = driver.get_window_size()
        self.swipe(sizedict['width'] / 2, sizedict['height'] / 4,
                   sizedict['width'] / 2, sizedict['height'] * 3 / 4, duration)

    def swipe_left(self, duration=1000):
        """
        向左滑屏
        | ARGS:  | duration:  | 滑动持续时间，默认1s，单位ms |
        """
        driver = self._current_application()
        sizedict = driver.get_window_size()
        self.swipe(sizedict['width'] * 3 / 4, sizedict['height'] /
                   2, sizedict['width'] / 4, sizedict['height'] / 2, duration)

    def swipe_right(self, duration=1000):
        """
        向右滑屏
        | ARGS:  | duration: |  滑动持续时间，默认1s，单位ms |
        """
        driver = self._current_application()
        sizedict = driver.get_window_size()
        self.swipe(sizedict['width'] / 4, sizedict['height'] / 2,
                   sizedict['width'] * 3 / 4, sizedict['height'] / 2, duration)

    def swipe_down_to(self, locator, duration=1000, maxdepth=10):
        """
        向下滑屏到指定的元素
        | ARGS:  | locator:  | 请参考 Appium元素定位部分，推荐XPATH |
        |        | duration: |  滑动持续时间，默认1s，单位ms |
        |        | maxdepth: |  最多滑屏次数，默认10次 |

        example:
        |   Swipe Down To locator | xpath=//android.widget.EditText |
        |   Swipe Down To locator | xpath=//android.widget.EditText | 500 | 5 |
        """
        moved = False
        counter = 0
        maxdepth = int(maxdepth)
        while not self._is_element_present(locator) and counter < maxdepth:
            self.swipe_down(duration)
            counter += 1
            moved = True

        if not self._is_element_present(locator):
            raise AssertionError(
                "Could not find element on page '%s' " % locator)
        if moved:
            time.sleep(1)
            self._current_application().page_source

    def swipe_up_to(self, locator, duration=1000, maxdepth=10):
        """
        向上滑屏到指定的元素
        | ARGS:  | locator:  | 请参考 Appium元素定位部分，推荐XPATH |
        |        | duration: |  滑动持续时间，默认1s，单位ms |
        |        | maxdepth: |  最多滑屏次数，默认10次 |

        example:
        |   Swipe Up To locator | xpath=//android.widget.EditText |
        """
        moved = False
        counter = 0
        maxdepth = int(maxdepth)
        while not self._is_element_present(locator) and counter < maxdepth:
            self.swipe_up(duration)
            counter += 1
            moved = True

        if not self._is_element_present(locator):
            raise AssertionError(
                "Could not find element on page '%s' " % locator)
        if moved:
            time.sleep(1)
            self._current_application().page_source

    def wait_and_tap(self, locator, timeout=10):
        """
        等待元素在页面显示后再点击
        | ARGS:  | locator: |  请参考 Appium元素定位部分，推荐XPATH |
        |        | timeout: |  等待时间， 默认10s，单位s |

        example:
        |   Wait and Tap | xpath=//android.widget.EditText |
        |   Wait and Tap | xpath=//android.widget.EditText | 5 |
        """
        self.wait_until_page_contains_element(locator, timeout)
        self.tap(locator)

    def tap_and_wait_page_load(self, locator, retry=3, timeout=30):
        """
        点击后等待页面加载，加载失败后进行重试。
        | ARGS:  | locator: |  请参考 Appium元素定位部分，只支持XPATH，或者使用文本定位 |
        |        | retry:   |  重试次数， 默认3次 |
        |        | timeout: |  等待时间， 默认10s，单位s |

        example:
        |   Tap And Wait Page Load | xpath=//android.widget.EditText |
        |   Tap And Wait Page Load | 词库 | 5 | 10 |
        """
        if not locator.startswith('xpath='):
            locator = "xpath=//*[@text='%s']" % locator
        self.tap(locator)
        reloadlocator = "xpath=//android.widget.TextView[@text='点击重新加载']"
        for i in range(int(retry)):
            time.sleep(0.5)
            self.wait_until_page_does_not_contain(u'正在加载', timeout)
            if self._is_element_present(reloadlocator):
                self.tap(reloadlocator)
            else:
                break
        self.page_should_not_contain_text(u'正在加载')
        if self._is_element_present(reloadlocator):
            raise AssertionError(
                u"Loading page failed! please check your network connectivity! Locator: %s" % locator)

    def wait_until_element_contains(self, locator, attribute, value, timeout=30):
        """
        等待页面元素的状态变化，例如下载是否完成等。
        | ARGS:  | locator: |  请参考 Appium元素定位部分，推荐XPATH |
        |        | attribute: |  属性 |
        |        | value: |  期望值 |
        |        | timeout: |  等待时间， 默认30s，单位s，需大于２s |

        example:
        |   Wait Until Element Contains | xpath=//android.widget.EditText | text | 文本 |
        """
        starttime = time.time()
        endtime = starttime
        while (endtime - starttime) < int(timeout):
            v = self.get_element_attribute(locator, attribute)
            if v.find(value) != -1:
                break
            time.sleep(1)
            endtime = time.time()
        if v.find(value) == -1:
            raise TimeoutException(
                "Can not find %s at %s after %s Seconds!" % (value, locator, timeout))

    def tap_text(self, text):
        """
        点击页面文本
        | ARGS: |  text:  | 文本 |

        example:
        |   Tap Text | 皮肤  |
        """
        locator = "xpath=//*[@text='%s']" % text
        self.tap(locator)

    def tap_button(self, text):
        """
        点击按钮
        | ARGS: |  text: |  按钮文本 |

        example:
        |   Tap Button | 确定 |
        """
        locator = "xpath=//android.widget.Button[@text='%s']" % text
        self.tap(locator)

    def tap_element_contains_text(self, text):
        """
        点击页面中包含文本的元素
        | ARGS: |  text: |  文本 |

        example:
        |   Tap Element Contains Text | 讯飞 |
        """
        locator = "xpath=//*[contains(@text,'%s')]" % text
        self.tap(locator)

        "driver..exists()"

    def start_activity(self, app_package, app_activity, alternate_activity=None, **opts):
        """
        启动指定的Activity
        | ARGS:  | app_package:  | Package名称 |
        |        | app_activity: |  Activity名称 |
        |        | alternate_activity: |  备用activity，部分机型可能会出现无法启动非launchable的activity，可通过此参数设置备选方案 |

        example:
        |   Start Activity | com.forimetest | .MainActivity |

        WebDriverException: Message: An unknown server-side error occurred while processing the command. Original error: Error occured while starting App. Original error: Activity used to start app doesn't exist or cannot be launched! Make sure it exists and is a launchable activity
        """
        driver = self._current_application()
        print 'start_activity1'
        try:
            driver.start_activity(app_package, app_activity, **opts)
        except WebDriverException:
            try:
                if alternate_activity:
                    driver.start_activity(
                        app_package, alternate_activity, **opts)
            except WebDriverException:
                print 'start_activity2'
                if(app_package.startswith('com.iflytek.inputmethod') and
                   not app_package.endswith('com.iflytek.inputmethod')):
                    command = 'adb -s %s shell am start -n %s/com.iflytek.inputmethod%s' % (
                        self.device_id, app_package, app_activity)
                    print 'start_activity command:', command
                    os.system(command)
                else:
                    raise

    def activate_ime_engine(self, engine):
        """
        弹出输入法键盘，注意，这里弹出的输入法键盘最上面一栏导航可能无法显示，请慎用，建议慎用点击输入框弹出
        | ARGS:  | engine:  | 输入法引擎 |

        example:
        |   Activate Ime Engine | com.iflytek.inputmethod/.FlyIME |
        """
        driver = self._current_application()
        driver.activate_ime_engine(engine)

    def ime_engine_should_be_enabled(self, engine):
        """
        检查当前使用的输入法引擎
        | ARGS: |  engine:  | 输入法引擎 |

        example:
        |   Ime Engine Should Be Enabled | com.iflytek.inputmethod/.FlyIME |
        """
        driver = self._current_application()
        if not driver.is_ime_active() or driver.active_ime_engine != engine:
            raise AssertionError(
                "IME not activate as expected! Current IME: %s" % driver.active_ime_engine)

    def wait_and_screenshot(self, locator, timeout=10, filename=None):
        """
        等待页面元素显示后截屏
        | ARGS:  | locator:  | 请参考 Appium元素定位部分，推荐X |
        |        | timeout:  | 等待时间， 默认10s，单位s |
        |        | filename: |  保持的文件名称 |

        example:
        |   Wait and Screenshot | xpath=//android.widget.EditText |
        |   Wait and Screenshot | xpath=//android.widget.EditText | filename=${CURDIR}/ScreenShot/Homepage.png |
        """
        self.wait_until_page_contains_element(locator, timeout)
        self.capture_page_screenshot(filename)

    def init_testdata(self, casename):
        driver = self._current_application()
        sizedict = driver.get_window_size()
        filename = '_'.join(
            [casename, str(sizedict['width']), str(sizedict['height'])])
        with open(filename, 'wb') as fp:
            fp.write('')

    def check_locations(self, casename, *locators):
        """
        检查元素位置信息，与上次执行的结果进行对比。

        Check Locations
        """
        driver = self._current_application()
        sizedict = driver.get_window_size()
        filename = '_'.join(
            [casename, str(sizedict['width']), str(sizedict['height'])])
        buf = ''
        for locator in locators:
            location = self.get_element_location(locator)
            size = self.get_element_size(locator)
            buf += ' '.join([locator, str(location), str(size), '\n'])
        if not os.path.exists(filename):
            with open(filename, 'ab') as fp:
                fp.write(buf.encode('GBK'))
        else:
            with open(filename, 'rb') as fp:
                data = fp.read().decode('GBK')
            if not buf == data:
                raise AssertionError("UI Changed!")

    def tap_if_present(self, locator):
        """
        点击可能显示的页面元素，如果没有显示则无操作
        | ARGS:  | locator:  | 请参考 Appium元素定位部分，推荐XPATH |

        example:
        |   Tap If Present | xpath=//android.widget.EditText |
        """
        if self._is_element_present(locator):
            self.tap(locator)
            return True
        return False

    def decide_if_present(self, locator):
        """
        判断当前页面是否有该页面元素，返回true or false   WYF
        | ARGS:  | locator:  | 请参考 Appium元素定位部分，推荐XPATH |

        example:
        |   Decide If Present | xpath=//android.widget.EditText |
        """
        if self._is_element_present(locator):
            return True
        return False

    def tap_next_to_install(self, locator1, locator2):
        """
       安装界面点击下一步直到页面底端显示安装                         WYF
        | ARGS: |  locator1:  | 显示文字为‘下一步’的按钮 |
        |       | locator2:  | 显示文字为‘安装’的按钮|
        example:
        |   Tap Next To Install | 下一步  | 安装  |
        """
        while True:
            if self._is_element_present(locator2):
                self.tap(locator2)
                break
            else:
                self.tap(locator1)

    def swipe_element_to_top(self, locator, duration=1000):
        """
        将元素滑动到页面顶端
        | ARGS: |  locator:  | 请参考 Appium元素定位部分，推荐XPATH |
        |       | duration:  | 持续时间，默认1s，单位ms |
        example:
        |   Swipe Element to Top | xpath=//android.widget.EditText |
        """
        location = self.get_element_location(locator)
        if location['y'] > 100:
            self.swipe(200, location['y'], 200, 100, duration)

    def element_attribute_should_not_match(self, locator, attr_name, match_pattern, regexp=False):
        """
        检查页面元素
        | ARGS:  | locator:       |  请参考 Appium元素定位部分，推荐XPATH |
        |        | attr_name:     | 属性名称 |
        |        | match_pattern: |  期望结果，可以是正则表达式 |
        |        | regexp:        | 是否为正则表达式，默认为否 |

        example:
        |   Element Attribute Should Not Match | xpath=//android.widget.EditText | Text | 文本 |
        """
        try:
            self.element_attribute_should_match(
                locator, attr_name, match_pattern, regexp=regexp)
        except:
            pass
        else:
            raise AssertionError("Element '%s' attribute '%s' should not be '%s' " % (
                locator, attr_name, match_pattern))


#
#     def init_keyboard(self):
#         """
#         #Not Used
#         init keyboard
#         """
#         driver = self._current_application()
#         sizedict = driver.get_window_size()
#         self.keyboard = Keyboard(sizedict['width'], sizedict['height'])

    def keyboard_press(self, *keystrs, **kws):
        """
        可以通过time属性设置按键后的等待时间，如果time设置为0，则不会更新键盘信息，用于获取更快的按键速度
        按键列表：
        | 通用按键： |          |  settings, keyboard, voice, selector, emoji, hide |
        | 候选字：     |          |  candidate_1, candidate_2, ..., candidate_n |
        | 9键拼音：     | 拼音组合： | combination_1, combination_2, ..., combination_n |
        |          | ^_^:      | smile |
        |          | 123:      | number |
        |          | 符:       | symbol |
        |          | 中/英:    | convert |
        |          | 回车:     | enter |
        |          | 清除:     | clear |
        |          | 返回:     | back |
        |          | 删除:     | del |
        | 编辑面板: | Del:     | del2 |
        |          | 方向键:   | up, down, left, right |
        | 表情面板: | 顶部导航：  | emoji, emoticon, expression, add, back, delete |
        |          | 底部导航:  | preview_1, preview_2, ..., preview_n |
        |          | 表情:      | emoji_1, emoji_2, ..., emoji_n |
        | 常用语         | 分组:      | group_1, group_2, ..., group_n |
        |          | 列表:      | content_1, content_2, ..., content_n |
        |          | 操作按钮:  | expend_1, expend_2, ..., expend_n |
        |          | 新增常用语   | add_null |
        |          | 新增分组        | add_group |
        |          | 全屏                  | full |
        |          | 设置                  | setting |
        |          | 修改                  | edit |
        |          | 删除                  | delete |
        |          | 置顶                  | top |
        | 云拼音         |            | pinyin_cloud |
        | 笔画输入    |            | DIAN, HENG, ZHE, SHU, PIE |
        | 拼音组合栏    |            | composing |

        Example:
        | Keyboard Press | a | b | c | candidate_1 |
        | Keyboard Press | settings | 中文 | 26键拼音 | time=1 |
        | Keyboard Press | emoji | ^_^ | time=1 |
        | Keyboard Press | voice | time=0 |
        """
        for keystr in keystrs:
            keystr = keystr.lower()
            action = TouchAction(self._current_application())
            x, y = self._get_key_location_in_keyboard(keystr)
            action.tap(x=x, y=y).perform()
            logger.info(u"Pressed key %s at location (%s, %s)" %
                        (keystr, x, y))
            interval = float(kws.get('time', None) or self.keypress_interval)
            time.sleep(interval)
            if interval != 0 and keystr not in iFlyKeyLogList.STATIC_KEY:
                self.keyboard.update_ui(keystr, self.get_key_log())
            time.sleep(0.5)

    def keyboard_press_and_screenshot(self, *keystrs, **kws):
        """
        按键的同时截图                    WYF      
        Example:
        | Keyboard Press And Screenshot | a | b | c |
        """
        for keystr in keystrs:
            keystr = keystr.lower()
            action = TouchAction(self._current_application())
            x, y = self._get_key_location_in_keyboard(keystr)
            action.tap(x=x, y=y).perform()
            filename = None
            self.capture_page_screenshot(filename)
            logger.info(u"Pressed key %s at location (%s, %s)" %
                        (keystr, x, y))
            interval = float(kws.get('time', None) or self.keypress_interval)
            time.sleep(interval)
            if interval != 0 and keystr not in iFlyKeyLogList.STATIC_KEY:
                self.keyboard.update_ui(keystr, self.get_key_log())

    def keys_should_present(self, *keystrs):
        for keystr in keystrs:
            try:
                x, y = self.keyboard.get_key_location(keystr)
                continue
            except:
                raise AssertionError(
                    "key '%s' not found in current page " % (keystr))
        return True

    def keys_log_should_present(self, *keystrs):
        for keystr in keystrs:
            try:
                x, y = self.keyboard.get_key_location(keystr)
                continue
            except:
                logdir = self._get_log_dir()
                filepath = logdir + '/' + 'errlog.txt'
                file = open(filepath, 'a')
                file.write("key '%s' not found in current page " % (keystr))
                file.write("\n")
                file.close()
                raise AssertionError(
                    "key '%s' not found in current page " % (keystr))
        return True

    def decide_key_if_present(self, keystr):
        try:
            x, y = self.keyboard.get_key_location(keystr)
            return True
        except AssertionError:
            logger.debug(u'key %s not found in current page' % keystr)
            return False

    def _get_key_location_in_keyboard(self, keystr):
        try:
            x, y = self.keyboard.get_key_location(keystr)
        except AssertionError:
            # keys in next page on settings panel is not shown by default
            if keystr in self.keyboard.Floating_Keys:
                logger.debug(
                    u'key %s not found in current page, swipe to next page' % keystr)
                # self.keyboard_swipe_left()
                x, y = self.keyboard.get_key_location(keystr)
            else:
                raise
        if keystr in iFlyKeyLogList.OUT_KEY:
            return x, y
        # Keys showed but not in current page
        keyboard_loc = self.keyboard.get_keyboard_location()
        count = 0
        while x < 0 and count < 15:
            count += 1
            logger.debug(
                u'key %s found at %d,%d. swipe keyboard to right %d' % (keystr, x, y, count))
            self.keyboard_swipe_right(200)
            time.sleep(0.5)
            x, y = self.keyboard.get_key_location(keystr)

        count = 0
        while x > keyboard_loc['width'] and count < 15:
            count += 1
            logger.debug(
                u'key %s found at %d,%d. swipe keyboard to left %d' % (keystr, x, y, count))
            self.keyboard_swipe_left(200)
            time.sleep(0.5)
            x, y = self.keyboard.get_key_location(keystr)

        count = 0
        while y < keyboard_loc['y'] and count < 15:
            count += 1
            logger.debug(
                u'key %s found at %d,%d. swipe keyboard to down %d' % (keystr, x, y, count))
            self.keyboard_swipe_down(200)
            time.sleep(0.5)
            x, y = self.keyboard.get_key_location(keystr)

        count = 0
        while y > keyboard_loc['y'] + keyboard_loc['height'] and count < 15:
            count += 1
            logger.debug(
                u'key %s found at %d,%d. swipe keyboard to up %d' % (keystr, x, y, count))
            self.keyboard_swipe_up(200)
            time.sleep(0.5)
            x, y = self.keyboard.get_key_location(keystr)

        return x, y

    def keyboard_long_press(self, keystr, duration=1000, waittime=0.5):
        """
        长按键盘按键
        | ARGS: |  keystr:  | 请参考  `Keyboard Press` 关键字 |
        |       | duration: |  按键时长，默认1s，单位ms |
        |       | waittime: |  按键后等待时间，默认0.5s，单位s |

        example:
        |   Long Press Key | enter |
        """
        action = TouchAction(self._current_application())
        x, y = self._get_key_location_in_keyboard(keystr.lower())
        longpress = action.long_press(x=x, y=y, duration=duration)
        longpress.release().perform()
        logger.info(u"Long pressed key %s at location (%s, %s)" %
                    (keystr, x, y))
        time.sleep(waittime)
        self.keyboard.update_ui(keystr, self.get_key_log())

#     def set_keyboard_type(self, typestr):
#         """
#         type string
#         """
#         self.keyboard.set_keyboard_type(typestr)

    def set_keypress_interval(self, interval):
        """
        设置按键的时间间隔，默认0.5s，返回原值
        | ARGS:  | interval: |  时间间隔，单位s |
        """
        orignal = self.keypress_interval
        self.keypress_interval = interval
        return orignal

    def keyboard_swipe_left(self, duration=200):
        """
        键盘向左滑动
        | ARGS:  | duration:  | 持续时间，默认200ms，单位ms |
        """
        loc = self.keyboard.get_keyboard_location()
        self._hand_swipe(loc['width'] * 3 / 4, loc['y'] + loc['height'] /
                         2, loc['width'] / 4, loc['y'] + loc['height'] / 2, duration)
        time.sleep(1)
        self.keyboard.update_ui('init', self.get_key_log())

    def keyboard_swipe_right(self, duration=200):
        """
        键盘向右滑动
        | ARGS: |  duration:  | 持续时间，默认200ms，单位ms |
        """
        loc = self.keyboard.get_keyboard_location()
        self._hand_swipe(loc['width'] / 4, loc['y'] + loc['height'] / 2,
                         loc['width'] * 3 / 4, loc['y'] + loc['height'] / 2, duration)
        time.sleep(1)
        self.keyboard.update_ui('init', self.get_key_log())

    def keyboard_swipe_up(self, duration=200):
        """
        键盘向上滑动
        | ARGS:  | duration: |  持续时间，默认200ms，单位ms |
        """
        loc = self.keyboard.get_keyboard_location()
        self._hand_swipe(loc['width'] / 2, loc['y'] + loc['height'] * 9 /
                         10, loc['width'] / 2, loc['y'] + loc['height'] * 2 / 3, duration)
        time.sleep(1)
        self.keyboard.update_ui('init', self.get_key_log())

    def keyboard_swipe_down(self, duration=200):
        """
        键盘向下滑动
        | ARGS:  | duration:  | 持续时间，默认200ms，单位ms |
        """
        loc = self.keyboard.get_keyboard_location()
        self._hand_swipe(loc['width'] / 2, loc['y'] + loc['height'] / 4,
                         loc['width'] / 2, loc['y'] + loc['height'] * 3 / 4, duration)
        time.sleep(1)
        self.keyboard.update_ui('init', self.get_key_log())

    def keyboard_combination_swipe_up(self, duration=200):
        """
        拼音组合栏向上滑动
        """
        loc = self.keyboard.get_keyboard_location()
        x, _ = self.keyboard.get_key_location('combination_1')
        self._hand_swipe(
            x / 2, loc['y'] + loc['height'] * 3 / 4, x / 2, loc['y'] + loc['height'] / 4, duration)
        time.sleep(1)
        self.keyboard.update_ui('init', self.get_key_log())

    def keyboard_combination_swipe_down(self, duration=200):
        """
        拼音组合栏向下滑动
        """
        loc = self.keyboard.get_keyboard_location()
        x, _ = self.keyboard.get_key_location('combination_1')
        self._hand_swipe(
            x / 2, loc['y'] + loc['height'] / 4, x / 2, loc['y'] + loc['height'] * 3 / 4, duration)
        time.sleep(1)
        self.keyboard.update_ui('init', self.get_key_log())

    def keyboard_candidate_swipe_left(self, duration=200):
        """
        候选字向左滑动
        | ARGS: |  duration: |  持续时间，默认200ms，单位ms |
        """
        loc = self.keyboard.get_keyboard_location()
        _, y = self.keyboard.get_key_location('candidate_1')
        self._hand_swipe(
            loc['width'] * 3 / 4, y + 20, loc['width'] / 4, y + 20, duration)
        time.sleep(1)
        self.keyboard.update_ui('init', self.get_key_log())

    def keyboard_candidate_swipe_right(self, duration=200):
        """
        候选字向右滑动
        | ARGS:  | duration:  | 持续时间，默认200ms，单位ms |
        """
        loc = self.keyboard.get_keyboard_location()
        _, y = self.keyboard.get_key_location('candidate_1')
        self._hand_swipe(
            loc['width'] / 4, y + 20, loc['width'] * 3 / 4, y + 20, duration)
        time.sleep(1)
        self.keyboard.update_ui('init', self.get_key_log())

    def keyboard_title_swipe_left(self, duration=200):
        """
        标题栏向左滑动
        | ARGS:  | duration:  | 持续时间， 默认200ms, 单位ms |
        """
        loc = self.keyboard.get_keyboard_location()
        self._hand_swipe(loc['width'] * 3 / 4, loc['y'] + loc['height'] /
                         10, loc['width'] / 4, loc['y'] + loc['height'] / 10, duration)
        time.sleep(1)
        self.keyboard.update_ui('init', self.get_key_log())

    def keyboard_title_swipe_right(self, duration=200):
        """
        标题栏向右滑动
        | ARGS:  | duration:  | 持续时间， 默认200ms, 单位ms |
        """
        loc = self.keyboard.get_keyboard_location()
        self._hand_swipe(loc['width'] / 4, loc['y'] + loc['height'] / 10,
                         loc['width'] * 3 / 4, loc['y'] + loc['height'] / 10, duration)
        time.sleep(1)
        self.keyboard.update_ui('init', self.get_key_log())

    def keyboard_get_key_location(self, keystr):
        """
        获取键盘按键位置
        """
        return self.keyboard.get_key_location(keystr)

    def swipe_element(self, locator, x, y, duration=500):
        """
        滑动选定的元素
        """
        loc = self.get_element_location(locator)
        size = self.get_element_size(locator)
        startx = loc['x'] + size['width'] / 2
        starty = loc['y'] + size['height'] / 2
        self.swipe(startx, starty, startx + int(x), starty + int(y), duration)

    def tap_element(self, el):
        """
        点击元素
        """
        driver = self._current_application()
        action = TouchAction(driver)
        action.tap(el).perform()

    def delete_path(self, path):
        """
        删除设备上的文件

        example:
        |   Delete Path | /sdcard/test.txt
        """
        driver = self._current_application()
        driver.delete_path(path)

    def adb_set_inputmethod_iflytek(self):
        cmd = "adb -s %s shell ime set com.iflytek.inputmethod/.FlyIME" % (
            self.device_id)
        os.system(cmd)

    def adb_pm_clear_iflytek_inputmethod(self):
        cmd = "adb -s %s shell pm clear %s" % (
            self.device_id, BuiltIn().get_variable_value("${APPPACKAGE}"))
        print cmd
        os.system(cmd)

    def adb_press_home(self):
        cmd = "adb -s %s shell input keyevent 3" % (self.device_id)
        os.system(cmd)

    def adb_press_back(self):
        cmd = "adb -s %s shell input keyevent 4" % (self.device_id)
        os.system(cmd)

    def adb_open_imetest_activity(self):
        cmd = "adb -s %s shell am start -n com.forimetest/.MainActivity" % (
            self.device_id)
        os.system(cmd)

    def adb_enable_inputmethod_iflytek(self):
        cmd = "adb -s %s shell ime enable com.iflytek.inputmethod/.FlyIME" % (
            self.device_id)
        os.system(cmd)

    def adb_remove_application(self, application):
        cmd = "adb -s %s uninstall %s" % (self.device_id, application)
        os.system(cmd)

    def adb_clear_device_log(self):
        cmd = "adb -s %s logcat -c" % (self.device_id)
        print cmd
        os.system(cmd)

    def adb_get_device_time(self):
        cmd = 'adb -s %s shell date' % (self.device_id)
        try:
            date_str = os.popen(cmd.decode('utf-8').encode('gbk')).readlines()
        except:
            date_str = os.popen(cmd.decode('utf-8').encode('gbk')).readlines()
        d = date_str[0].strip().split()
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        h, m, s = d[3].split(':')
        date_time = '%s%s%s.%s%s%s' % (
            d[5], '%02d' % (months.index(d[1]) + 1), d[2], h, m, s)
        date = datetime.strptime(date_time, "%Y%m%d.%H%M%S")
        return date

    def adb_set_device_time(self, days=0, seconds=0, minutes=0, hours=0, weeks=0):
        now = self.adb_get_device_time()
        timecur = (now).strftime('%Y%m%d.%H%M%S')
        delta = timedelta(days=int(days), seconds=int(seconds), minutes=int(
            minutes), hours=int(hours), weeks=int(weeks))
        timestr = (now + delta).strftime('%Y%m%d.%H%M%S')
        cmd = "adb -s %s shell \"su -c 'date -s \"%s\"'\"" % (
            self.device_id, timestr)
        print 'set time from %s -> %s' % (timecur, timestr)
        print 'cmd:', cmd
        os.system(cmd)
        time.sleep(1)
        print 'curtime', self.adb_get_device_time()

    def adb_set_wifi_status(self, wifi):
        if(wifi == '0' or wifi == 0):
            cmd = "adb -s %s shell \"su -c 'svc wifi disable'\"" % (
                self.device_id)
        else:
            cmd = "adb -s %s shell \"su -c 'svc wifi enable'\"" % (
                self.device_id)
        os.system(cmd)

    def set_device_time(self, days=0, seconds=0, minutes=0, hours=0, weeks=0):
        """
        修改设备的时间，按照当前时间的偏移量计算。需要手机有root权限，否则无法执行
        | ARGS: |  days:   | 偏移天数  |
        |       | seconds: |  偏移秒数 |
        |       | minutes: |  偏移分钟数 |
        |       | hours:   |  偏移小时数 |
        |       | weeks:   |  偏移周数 |

        example:
        |   Set Device Time | 
        |   Set Device Time | days=1 | weeks=1 |
        |   Set Device Time | hours=2 |
        """
        now = datetime.now()
        print(now)
        delta = timedelta(days=int(days), seconds=int(seconds), minutes=int(
            minutes), hours=int(hours), weeks=int(weeks))
        driver = self._current_application()
        driver.set_device_time((now + delta).strftime('%Y%m%d.%H%M%S'))

    def send_log_by_socket(self, log, port, transtype, host="", bufsiz=""):
        """
        将文本内容或流内容通过socket发送到服务端;
        | ARGS: |  log:   |  传输内容  |
        |       |  port:   |  端口号  |
        |       |  transtype:   |  传输类型，1为文本内容，2为流 |
        |       |   host:  |  IP地址，默认为本机 |
        |       |  bufsiz: |  接收返回内容缓冲区大小，默认为1024*100 |
        example:
        |   Send Log By Socket | log="hello world" | port=1122 | type=1 |
        |   Send Log By Socket | log=open(file,"r") | port=1122 | type=2 |
        |   Send Log By Socket | log=open"hello world" | port=1122 | type=1 | host=192.168.39.97 | bufsiz=1024 |
        """
        class TcpClient:

            def __init__(self, PORT, HOST="", BUFSIZ=""):
                self.PORT = eval(PORT)
                self.HOST = HOST if HOST else "127.0.0.1"
                self.ADDR = (self.HOST, self.PORT)
                self.BUFSIZ = eval(BUFSIZ) if BUFSIZ else 1024 * 100
                print "PORT:%s" % str(self.PORT)
                print "HOST:%s" % self.HOST
                print "BUFSIZ:%s" % self.BUFSIZ
                self.client = socket(AF_INET, SOCK_STREAM)
                try:
                    self.client.connect(self.ADDR)
                except Exception as e:
                    traceback.print_exc()
                    print e

            def sendstr(self, text):
                data = text
                if not data:
                    return
                self.client.send(data)
                print(r'Send Message To %s：%s' % (self.HOST, data))
                if data.upper() == "QUIT":
                    return
                data = self.client.recv(self.BUFSIZ)
                if not data:
                    return
                print(r'Receive Message From %s：%s' % (self.HOST, data))

            def sendstream(self, stream):
                if not isinstance(stream, file):
                    print "Not Match Type Of Stream"
                    raise Exception
                    return
                while True:
                    t = stream.readline()
                    if not t:
                        break
                    self.client.send(t)
                print "Send Stream Done"
        print "TcpClient Start"
        print log, type(log)
        if isinstance(log, unicode):
            log = log.encode("utf-8")
        tcpclient = TcpClient(port, host, bufsiz)
        if transtype == "1":
            print "Send Str"
            tcpclient.sendstr(log)
        elif transtype == "2":
            tcpclient.sendstream(log)
        else:
            print "Unknown Type"

    def decide_file_exist(self, path):
        """
        判断设备上是否存在文件                           WYF

        example:
        |   Decide File Exist | /sdcard/test.txt
        """
        driver = self._current_application()
        print dir(driver)
        check = True
        try:
            driver.pull_file(path)
        except WebDriverException:
            check = False
        return check

    def switch_ime(self, ime):
        """
        切换输入法                           WYF

        example:
        |   Switch Ime | com.baidu.input/.ImeService
        |   Switch Ime | com.iflytek.inputmethod/.FlyIME
        """
        cmd = "adb shell ime set %s" % (ime)
        os.system(cmd)

    def install_apk(self, path):
        """
        安装apk，path是apk在PC上的路径                               
        """
        cmd = "adb install %s" % (path)
        os.system(cmd)

    def add(self, a, b):
        """
        整数相加                   WYF
        """
        c = a + b
        return c

    def click_a_point(self, x=0, y=0):
        """
        点击坐标（x,y）                            WYF
        """
        self._info("Clicking on a point (%s,%s)." % (x, y))
        driver = self._current_application()
        action = TouchAction(driver)
        try:
            action.press(x=float(x), y=float(y)).release().perform()
        except:
            assert False, "Can't click on a point at (%s,%s)" % (x, y)

    def long_press_a_point(self, x=0, y=0):
        """ 
       长按坐标点（x,y）                     WYF
        """
        driver = self._current_application()
        action = TouchAction(driver)
        try:
            action.long_press(x=float(x), y=float(y)).perform()
        except:
            assert False, "Can't click on a point at (%s,%s)" % (x, y)

    def play_audio_file(self):
        """ 
       播放语音音频文件                       
        """
        cmd = "adb shell am broadcast -a PlayMusic"
        os.system(cmd)

    def stop_audio_file(self):
        """ 
       停止播放语音音频文件                       
        """
        cmd = "adb shell am broadcast -a StopMusic"
        os.system(cmd)

    def obtain_apk_message(self, device):
        """ 
       获取输入法apk版本等信息                       
        """
        cmd = "adb -s %s shell dumpsys package com.iflytek.inputmethod" % device
        os.system(cmd)
        try:
            date_str = os.popen(cmd.decode('utf-8').encode('gbk')).readlines()
        except:
            date_str = os.popen(cmd.decode('utf-8').encode('gbk')).readlines()
        print date_str

    def obtain_apk_version(self):
        """ 
       获取输入法apk版本号            
        """
        cmd = "adb -s %s shell dumpsys package com.iflytek.inputmethod" % (
            self.device_id)
        os.system(cmd)
        print cmd
        try:
            date_str = os.popen(cmd.decode('utf-8').encode('gbk')).readlines()
        except:
            date_str = os.popen(cmd.decode('utf-8').encode('gbk')).readlines()
        version = ''
        for str in date_str:
            if 'versionName' in str:
                print str
                version = str.strip().split('=')[-1]
        return version

    def obtain_apk_cpu(self):
        """ 
       获取输入法的cpu占用信息               
        """
        cmd = "adb -s %s shell top -m 30 -s cpu -n 1" % (self.device_id)
        result = subprocess.Popen(
            cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        while True:
            buff = result.stdout.readline()
            print buff
            if buff == '' and result.poll() != None:
                break

    def obtain_apk_memory(self):
        """ 
       获取输入法的内存占用信息                    
        """
        cmd = "adb -s %s shell dumpsys meminfo com.iflytek.inputmethod" % (
            self.device_id)
        result = subprocess.Popen(
            cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        while True:
            buff = result.stdout.readline()
            print buff
            if buff == '' and result.poll() != None:
                break

    def open_authority(self):
        """ 
       允许输入法所有权限，避免后续弹框                  
        """
        cmd = "adb shell uiautomator runtest AutoPermission.jar -c com.itesttech.App"
        print cmd
        os.system(cmd)

    def open_notifications(self):
        """ 
       打开系统通知栏                  
        """
        driver = self._current_application()
        driver.open_notifications()

    def push_sogou_package(self, path):
        """ 
       将搜狗文件夹导入手机              
        """
        cmd = "adb -s %s push %s /mnt/sdcard/sogou" % (self.device_id, path)
        print cmd
        os.system(cmd)

    def delete_sogou_package(self):
        """ 
       将搜狗文件夹从手机中删除              
        """
        cmd = "adb -s %s shell rm -rf /mnt/sdcard/sogou" % (self.device_id)
        print cmd
        os.system(cmd)

    def delete_package(self, path):
        """ 
       删除手机中的文件           
        """
        cmd = "adb -s %s shell rm -rf %s" % (self.device_id, path)
        print cmd
        os.system(cmd)

    def adb_push(self, srcpath, dstpath):
        """ 
    导入文件到手机
        """
        cmd = "adb -s %s push %s %s" % (self.device_id, srcpath, dstpath)
        print cmd
        os.system(cmd)

    def take_photo(self):
        """ 
       按拍照键       
        """
        cmd = "adb -s %s shell input keyevent CAMERA" % (self.device_id)
        print cmd
        os.system(cmd)

    def kill_settings_process(self):
        """ 
       查杀输入法设置进程
        """
        cmd = "adb -s %s shell ps" % (self.device_id)
        print cmd
        try:
            date_str = os.popen(cmd.decode('utf-8').encode('gbk')).readlines()
        except:
            date_str = os.popen(cmd.decode('utf-8').encode('gbk')).readlines()
        pid = 0
        for i in range(len(date_str)):
            str = date_str[i]
            d = str.strip().split()
#             print len(d)
#             print d[len(d) - 1]
            if d[len(d) - 1] == 'com.iflytek.inputmethod.settings':
                pid = d[1]
                break
        print pid
        cmd = "adb -s %s shell \"su -c 'kill %s'\"" % (self.device_id, pid)
        print cmd
        os.system(cmd)

    def kill_process_of_package(self, package):
        """ 
       通过包名查杀进程
        """
        cmd = "adb -s %s shell ps" % (self.device_id)
        print cmd
        try:
            date_str = os.popen(cmd.decode('utf-8').encode('gbk')).readlines()
        except:
            date_str = os.popen(cmd.decode('utf-8').encode('gbk')).readlines()
        pid = 0
        for i in range(len(date_str)):
            str = date_str[i]
            d = str.strip().split()
#             print len(d)
#             print d[len(d) - 1]
            if d[len(d) - 1] == package:
                pid = d[1]
                break
        print pid
        cmd = "adb -s %s shell \"su -c 'kill -KILL %s'\"" % (
            self.device_id, pid)
        print cmd
        os.system(cmd)

    def get_crash_file(self):
        """ 
       将输入法崩溃信息链接到测试报告
        """
        filepath = "/sdcard/Android/data/com.iflytek.inputmethod/cache"
        cmd = "adb -s %s shell ls %s" % (self.device_id, filepath)
#         cmd = "adb shell ls %s" % (filepath)
        print cmd
        try:
            date_str = os.popen(cmd.decode('utf-8').encode('gbk')).readlines()
        except:
            date_str = os.popen(cmd.decode('utf-8').encode('gbk')).readlines()
        print date_str
        filelist = []
        for name in date_str:
            print 'name', name
            lis = name.strip().split('.')
            if lis[-1] == 'txt':
                filelist.append(name.strip())
        print 'filelist', filelist

        logdir = self._get_log_dir()
        print logdir

        if len(filelist) != 0:
            for name in filelist:
                path = filepath + '/' + name
                cmd = "adb -s %s pull %s %s" % (self.device_id, path, logdir)
                date_str = os.popen(
                    cmd.decode('utf-8').encode('gbk')).readlines()

        if len(filelist) == 0:
            html_rst = ur'''本地无崩溃信息'''
            print html_rst
        else:
            html_rst = ''
            for name in filelist:
                path = logdir + '/' + name
                html_templet = ur'''输入法崩溃日志 ：<a href="%s" target="_blank" title="CRASH">%s</a>'''
                html_rst = html_rst + \
                    html_templet % (os.path.abspath(path), name) + '\n'
                print html_rst
        logger.info(html_rst, True, False)
        pass

    def capture_streenshot_to_path(self, filename):
        """ 
       保存屏幕截图到指定路径
        """
        print self.capturepath
        print filename
        filename = self.capturepath + "/" + filename
        print filename
#         print 'filename:' + filename
        driver = self._current_application()
        driver.get_screenshot_as_file(filename)

    def adb_broadcast_getdeviceuid(self):
        cmd = "adb -s %s shell am broadcast -a GetDeviceUid" % (self.device_id)
        print cmd
        os.system(cmd)

    def adb_broadcast_cleardeviceuid(self):
        cmd = "adb -s %s shell am broadcast -a ClearDeviceUid" % (
            self.device_id)
        print cmd
        os.system(cmd)

    def adb_mkdir(self, path):
        cmd = "adb -s %s shell mkdir -p %s" % (
            self.device_id, self.device_id)
        print cmd
        os.system(cmd)

    def get_keyboard_loc(self):
        """ 
       获取键盘面板的位置及大小，存储为全局变量，UI校验工具
        """
        loc = self.keyboard.get_keyboard_location()
        print loc
        index = self.capturepath.find("capturePics")
        path = self.capturepath[:index - 1]
        filepath = path + '/' + 'keyboardRegion.txt'
        print filepath
        if os.path.exists(filepath):
            file = open(filepath, 'a')
            file.write(u"x:%s, y:%s, height:%s, width:%s" %
                       (loc['x'], loc['y'], loc['height'], loc['width']))
            file.write("\n")
            file.close

    def change_h5_location(self, bodysize, inx, iny, offx, offy):
        """
        将h5页面元素坐标转化为相对手机屏幕的坐标
        """
        driver = self._current_application()
        sizedict = driver.get_window_size()
        ratio = sizedict['width'] / bodysize['width']
        changeX = int(inx) * ratio + int(offx)
        changeY = int(iny) * ratio + int(offy)
        return changeX, changeY

    def swipe_switch_keyboard(self, duration=200):
        """
        左滑动,切换中英文
        """
        loc = self.keyboard.get_keyboard_location()
        _, y = self.keyboard.get_key_location('convert')
        self._hand_swipe(
            loc['width'] * 3 / 4, y + 20, loc['width'] / 4, y + 20, duration)
        time.sleep(1)
        self.keyboard.update_ui('init', self.get_key_log())

    def adb_set_updatetime(self, days):
        """
        设置自动升级时间
        """
        now = self.adb_get_device_time()
        timecur = (now).strftime('%Y%m%d.%H%M%S')
        delta = timedelta(days=int(days))
        timestr = (now + delta).strftime('%Y%m%d.%H%M%S')
        time1 = timestr.split('.')[0]
        timestr = time1 + "." + "230000"
        cmd = "adb -s %s shell \"su -c 'date -s \"%s\"'\"" % (
            self.device_id, timestr)
        print 'set time from %s -> %s' % (timecur, timestr)
        print 'cmd:', cmd
        os.system(cmd)
        time.sleep(1)
        print 'curtime', self.adb_get_device_time()

    def adb_restore_time(self, timestr):
        """
        重置手机时间
        """
        timestr = timestr.strftime('%Y%m%d.%H%M%S')
        cmd = "adb -s %s shell \"su -c 'date -s \"%s\"'\"" % (
            self.device_id, timestr)
        os.system(cmd)
        time.sleep(1)

    def util_toast_appearance(self, toast):
        """查找指定toast是否存在
        :Args:
        - toast - 需查找的toast.
        """
        application = self._current_application() ##获取当前的驱动
        try:
            toast_loc = ("xpath", ".//*[contains(@text,'%s')]" %toast)
            WebDriverWait(application, 6, 0.5).until(expected_conditions.presence_of_element_located(toast_loc))
            self._info("Toast has been found: %s ." %toast)
            return True
        except:
            raise AssertionError("Not found toast")
            return False

