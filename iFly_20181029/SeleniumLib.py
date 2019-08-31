#-*- coding: UTF-8 -*- 
"""

(C) Copyright 2016 wei_cloud@126.com

"""
from Selenium2Library import Selenium2Library
import os, tempfile, time
from robot.api import logger
from selenium.common.exceptions import StaleElementReferenceException
from datetime import date, timedelta

class SeleniumLib(Selenium2Library):
    
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = '0.1.0'
    
    def __init__(self,
                 timeout=5.0,
                 implicit_wait=0.0,
                 run_on_failure='Capture Page Screenshot',
                 screenshot_root_directory=None
    ):
        Selenium2Library.__init__(self, timeout, implicit_wait, run_on_failure, screenshot_root_directory)
        self.tmpfiles = []
        
    def generate_temp_list_file(self, content):
        """
        生成临时的uid列表文件或用户列表文件。返回生成的文件路径。
        """
        tp = tempfile.mktemp('.txt')
        with open(tp, 'wb') as fp:
            fp.write(content)
        self.tmpfiles.append(tp)
        logger.debug(u'Temp file generated! %s' %tp)
        return tp
    
    def remove_temp_files(self):
        """
        删除生成的临时文件，一般用于teardown步骤中
        """
        for fp in self.tmpfiles:
            try:
                os.remove(fp)
                logger.debug(u'Temp file removed! %s' %fp)
            except:
                logger.info(u"Remove file failed! %s" % fp)
        self.tmpfiles = []
    
    def scroll_to_element(self, locator):
        """
        将元素滑动到显示界面
        """
        element = self._element_find(locator, True, False)
        self._current_browser().execute_script("arguments[0].scrollIntoView(true);", element)
        
    def wait_until_table_loaded(self, locator, row, column, value, timeout=10):
        """
        等待列表元素的加载。
        | ARGS: | locator:  | 列表元素路径 |
        |       | row:      | 等待的列表行数 |
        |       | column:   | 等待的列表列数 |
        |       | value:    | 列表期望值 |
        |       | timeout:  | 最大等待时间，单位s，默认10s |
        
        example:
        |   Wait Until Table Loaded | xpath=//table | 2 | 2 | TestGroup | 15 |
        """
        cell = None
        start = time.time()
        while time.time() - start < float(timeout):
            try:
                cell = self.get_table_cell(locator, row, column)
            except StaleElementReferenceException:
                time.sleep(0.5)
                continue
            except AssertionError:
                if self._is_element_present("xpath=//td[@class='dataTables_empty']"):
                    cell = []
                    logger.info('Table is Empty!')
                    break
                else:
                    time.sleep(0.5)
                    continue
            else:
                if cell != value:
                    time.sleep(0.5)
                    continue
                else:
                    break
        if cell != [] and cell != value:
            raise AssertionError(u'Table not loaded in %s seconds. Last Value: %s' % (timeout, cell))
        
        return cell
    
    def clear_table_with_id(self, locator, column, value):
        """
        清空含有某个元素的列表。每次删除第一行，直到被全部删除。
        | ARGS: | locator:  | 列表元素路径 |
        |       | column:   | 元素所在的列数 |
        |       | value:    | 列表期望值 |
        
        example:
        |   Clear Table With Id | xpath=//table | 2 | TestGroup |
        """
        count = 0
        cell = self.wait_until_table_loaded(locator, 2, column, value)
        while cell!=[]:
            self._remove_first_item()
            count += 1
            cell = self.wait_until_table_loaded(locator, 2, column, value)
        logger.info('%s rows removed from table!' % count)
    
    def _remove_first_item(self):
        self.click_element(u'link=删除')
        confirmButton = u"xpath=//button/span[.='确定']"
        self.wait_until_page_contains_element(confirmButton)
        self.click_element(confirmButton)
        time.sleep(1)
        
    def clear_group_in_exception_list(self, groupname):
        """
        清空含有某个组名的特殊列表。
        | ARGS: | groupname:  | 需要清除的组名称 |
        | 起始页面 |   | 配置修改页面 |
        
        example:
        |   Clear Group In Exception List | TestGroup |
        """
        try:
            elements = self.get_webelements(u"xpath=//tr//td/input[@placeholder='选择用户群']")
        except ValueError:
            elements = []
        for i in range(len(elements)-1, -1, -1):
            element = elements[i]
            value = element.get_attribute('value')
            if groupname in value:
                delbtn = element.find_element_by_xpath(u"../button[.='删除']")
                delbtn.click()
                time.sleep(0.5)
        self.click_element(u"xpath=//div[@id='edit_dialog']/..//div/button/span[.='确定']")

    def get_date_string(self, days=0, include_hours=False):
        """
        获得时间字符串，用于日期控件的输入。
        日期格式为标准格式： 2016-06-20
        | ARGS: | days:  | 与当前时间的偏移天数，默认为当天，可为负数  |
        |       | include_hours:   | 是否显示具体时间，默认只显示日期  |
        | 返回值 | 日期字符串   | 2016-06-20 |
        |       |           | 2016-06-20 09:19:22 |
        
        example:
        |   Get Date String | -2 |
        |   Get Date String | 5 | True |
        """
        today = date.today()
        delta = timedelta(days=int(days))
        if include_hours:
            return (today + delta).isoformat() + ' ' + time.strftime('%H:%M:%S')
        else:
            return (today + delta).isoformat()
        
    def input_time(self, locator, timestr):
        """
        用于输入日期控件中的日期
        
        example:
        |   Input Time | xpath=//input[@name='params_DStartTime'] | 2016-06-20 09:19:22 |
        """
        element = self._element_find(locator, True, False)
        self._current_browser().execute_script("arguments[0].value=arguments[1]", element, timestr)
        