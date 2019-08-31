#-*- coding: UTF-8 -*-

from AppiumLib import AppiumLib
from HandWrite import HandWriteHelper
from LogHander import iFlyLoglib
from SeleniumLib import SeleniumLib
from HttpLib import CloudWebLib

# from BGLogLibrary import BGLogLibrary
# from robot.libraries.OperatingSystem import OperatingSystem


class IflyAppiumLib(AppiumLib, iFlyLoglib, HandWriteHelper):

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = '0.1.0'

    def __init__(self, timeout=5, run_on_failure='Capture Page Screenshot'):
        AppiumLib.__init__(self, timeout, run_on_failure)
        iFlyLoglib.__init__(self)


# class BGLog(BGLogLibrary):
#
#     ROBOT_LIBRARY_SCOPE = 'GLOBAL'
#     ROBOT_LIBRARY_VERSION = '0.1.0'
#
#     def __init__(self, run_on_failure='Capture Page Screenshot'):
#         #         AppiumAndroidLibrary.__init__(self, run_on_failure)
#         #         _ClientLog.__init__(self)
#         print 'run_on_failure'
#         BGLogLibrary.__init__(self, run_on_failure)


class IflySeleniumLib(SeleniumLib):

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = '0.1.0'

    def __init__(self,
                 timeout=5.0,
                 implicit_wait=0.0,
                 run_on_failure='Capture Page Screenshot',
                 screenshot_root_directory=None):
        SeleniumLib.__init__(
            self, timeout, implicit_wait, run_on_failure, screenshot_root_directory)


class iflyCloudLib(CloudWebLib):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = '0.1.0'

    def __init__(self):
        CloudWebLib.__init__(self)
