#-*- coding:utf-8 -*-
"""

(C) Copyright 2016 wei_cloud@126.com

"""
import os
from robot.api import logger
from KeyIdMap import GetKeyNameById
from KeyIdMap import ReturnKeyID
import KeyIdMap
from LogParser import iFlyKeyLogList
# from win32com.test.util import LogHandler
from robot.libraries.BuiltIn import BuiltIn


class Keyboard(object):
    Switch_Keys = [u'init', u'settings', u'keyboard', u'voice', u'selector', u'emoji',
                   u'smile', u'symbol', u'convert', u'number', u'more', u'ab', u'back',
                   u'9键拼音', u'26键拼音', u'9键英文', u'26键英文', u'笔画输入', u'半屏手写', u'全屏手写',
                   ]

    Floating_Keys = [u'皮肤', u'词库', u'精品', u'常用语', u'更新', u'游戏', u'反馈', u'祝福语', u'下载',
                     u'离线语音', u'手机清理', u'更多功能', u'输入法设置', u'键盘高度', u'键盘音效',
                     u'按键设置', u'候选字大小', u'繁体开关', u'日间模式', u'键盘手写', u'定制工具栏',
                     u'键盘透明度', u'手写云输入', u'拼音云输入']

    def __init__(self, *args):
        """

        """
        self.key_map = {}
        self.left = 0
        self.right = 0
        self.top = 0
        self.bottom = 0
        self.layout = None
        if len(args) == 1:
            self.update_ui('init', args[0])

    def get_key_location(self, keystr):
        keystr = keystr.lower()
        try:
            return self.key_map[keystr]['location']
        except KeyError:
            if keystr in iFlyKeyLogList.OUT_KEY:
                self.keylog.get_out_keys(keystr)
                self._update_out_keys(self.keylog)
                return self.key_map[keystr]['location']
            else:
                raise AssertionError('Key %s not found in current view! Keys in view: %s' % (
                    keystr, str(self.key_map.keys())))

    def set_keyboard_type(self, typestr):
        """
        Useless in this mode
        """
        pass

    def update_ui(self, keystr, keylog=None):
        self.keylog = keylog
        if len(keylog) < 2:
            logger.debug("No key log found! Keyboard not changed!")
            return
        for vs in keylog.keys.values():
            for v in vs:
                logger.debug(u'%s' % v)
        self.key_map = {}
        startx, starty = keylog.keys['start'][
            0].left, keylog.keys['start'][0].top
        self.left, self.right, self.top, self.bottom = keylog.keys['start'][0].left, keylog.keys[
            'start'][0].right, keylog.keys['start'][0].top, keylog.keys['start'][0].bottom
        for key in keylog.get_keys('normal_key'):
            if key.id == '0':
                logger.info(u'Key with 0 id skipped: %s' % key)
                continue
            if key.shown == 'true':

                # 日志校验工具向txt写入错误信息
                if not ReturnKeyID(key.id):
                    try:
                        variables = BuiltIn().get_variables()
                        logfile = variables['${LOG FILE}']
                        if logfile != 'NONE':
                            logdir = os.path.dirname(logfile)
                        else:
                            logdir = variables['${OUTPUTDIR}']
                    except RobotNotRunningError:
                        pass
                    print logdir
                    filepath = logdir + '/' + 'errlog.txt'
                    if os.path.exists(filepath):
                        file = open(filepath, 'a')
                        file.write(u"Key not initialized yet. %s" % key.id)
                        file.write("\n")
                        file.close()

                self.key_map[GetKeyNameById(key.id)] = self._get_key_info(
                    startx, starty, key)

        self._update_extra_keys(startx, starty, keylog)
        self._update_out_keys(keylog)

        if keystr in self.Switch_Keys:
            newlayout = self._parse_layout(keylog.get_input_layout())
            if newlayout:
                self.layout = newlayout

    def _get_key_info(self, startx, starty, key):
        return {'location': map(lambda (a, b): a + b, zip([startx, starty], key.location)), 'attributes': key}

    def _update_extra_keys(self, startx, starty, keylog):
        """
        """
        candidate_key = keylog.get_keys('candidate_key')
        for i in range(len(candidate_key)):
            if candidate_key[i].shown == 'true':
                self.key_map['candidate_%d' % (
                    i + 1)] = self._get_key_info(startx, starty, candidate_key[i])

        combination_key = keylog.get_keys('combination_key')
        for i in range(len(combination_key)):
            self.key_map['combination_%d' % (
                i + 1)] = self._get_key_info(startx, starty, combination_key[i])

        number_key = keylog.get_keys('ab_number_key')
        for i in range(len(number_key)):
            self.key_map[number_key[i].text] = self._get_key_info(
                startx, starty, number_key[i])

        menu_type_key = keylog.get_keys('menu_type_key')
        for i in range(len(menu_type_key)):
            if len(menu_type_key[i].text) == 0 or menu_type_key[i].text == 'null':
                try:
                    variables = BuiltIn().get_variables()
                    logfile = variables['${LOG FILE}']
                    if logfile != 'NONE':
                        logdir = os.path.dirname(logfile)
                    else:
                        logdir = variables['${OUTPUTDIR}']
                except RobotNotRunningError:
                    pass
                print logdir
                filepath = logdir + '/' + 'errlog.txt'
                if os.path.exists(filepath):
                    file = open(filepath, 'a')
                    file.write(u"Log text should not empty. %s" %
                               menu_type_key[i])
                    file.write("\n")
                    file.close()
                    raise RuntimeError(
                        u"Log text should not be empty. %s" % menu_type_key[i])
            self.key_map[menu_type_key[i].text] = self._get_key_info(
                startx, starty, menu_type_key[i])

        menu_cell_key = keylog.get_keys('menu_cell_key')
        for i in range(len(menu_cell_key)):
            if len(menu_cell_key[i].text) == 0 or menu_cell_key[i].text == 'null':
                try:
                    variables = BuiltIn().get_variables()
                    logfile = variables['${LOG FILE}']
                    if logfile != 'NONE':
                        logdir = os.path.dirname(logfile)
                    else:
                        logdir = variables['${OUTPUTDIR}']
                except RobotNotRunningError:
                    pass
                print logdir
                filepath = logdir + '/' + 'errlog.txt'
                if os.path.exists(filepath):
                    file = open(filepath, 'a')
                    file.write(u"Log text should not empty. %s" %
                               menu_cell_key[i])
                    file.write("\n")
                    file.close()
                    raise RuntimeError(
                        u"Log text should not be empty. %s" % menu_cell_key[i])
            self.key_map[menu_cell_key[i].text] = self._get_key_info(
                startx, starty, menu_cell_key[i])

        expression_normal_key = keylog.get_keys('expression_normal_key')
        # Supported keys: emoji, emoticon, expression, doutu, add, back, delete
        for i in range(len(expression_normal_key)):
            self.key_map[expression_normal_key[i].text] = self._get_key_info(
                startx, starty, expression_normal_key[i])

        emoji_type_key = keylog.get_keys('emoji_type_key')
        for i in range(len(emoji_type_key)):
            self.key_map[
                'preview_%d' % (i + 1)] = self._get_key_info(startx, starty, emoji_type_key[i])

        emoji_content_key = keylog.get_keys('emoji_content_key')
        for i in range(len(emoji_content_key)):
            if emoji_content_key[i].id != 'null':
                self.key_map[
                    'emoji_%d' % (i + 1)] = self._get_key_info(startx, starty, emoji_content_key[i])

        emoticon_content_key = keylog.get_keys('emoticon_content_key')
        for i in range(len(emoticon_content_key)):
            if emoticon_content_key[i].id != 'null':
                #                 self.key_map[emoticon_content_key[i].text] = self._get_key_info(startx, starty, emoticon_content_key[i])
                self.key_map['emoticon_%d' % (
                    i + 1)] = self._get_key_info(startx, starty, emoticon_content_key[i])

        emoticon_type_key = keylog.get_keys('emoticon_type_key')
        for i in range(len(emoticon_type_key)):
            self.key_map[emoticon_type_key[i].text] = self._get_key_info(
                startx, starty, emoticon_type_key[i])
#             self.key_map['emotilabel_%d' % (i+1)] = self._get_key_info(startx, starty, emoticon_type_key[i])

        expression_type_key = keylog.get_keys('expression_type_key')
        for i in range(len(expression_type_key)):
            self.key_map['explabel_%d' % (
                i + 1)] = self._get_key_info(startx, starty, expression_type_key[i])

        expression_content_key = keylog.get_keys('expression_content_key')
        for i in range(len(expression_content_key)):
            if expression_content_key[i].id != 'null':
                self.key_map['expression_%d' % (
                    i + 1)] = self._get_key_info(startx, starty, expression_content_key[i])

        doutu_type_key = keylog.get_keys('doutu_type_key')
        #collect, shop, tag, search
        for i in range(len(doutu_type_key)):
            self.key_map[doutu_type_key[i].text] = self._get_key_info(
                startx, starty, doutu_type_key[i])

        doutu_collection_key = keylog.get_keys('doutu_collection_key')
        for i in range(len(doutu_collection_key)):
            if doutu_collection_key[i].id != 'null':
                self.key_map['doutucoll_%d' % (
                    i + 1)] = self._get_key_info(startx, starty, doutu_collection_key[i])

        doutu_net_key = keylog.get_keys('doutu_net_key')
        for i in range(len(doutu_net_key)):
            if doutu_net_key[i].id != 'null':
                self.key_map[
                    'doutunet_%d' % (i + 1)] = self._get_key_info(startx, starty, doutu_net_key[i])

        doutu_tag_key = keylog.get_keys('doutu_tag_key')
        for i in range(len(doutu_tag_key)):
            self.key_map[doutu_tag_key[i].text] = self._get_key_info(
                startx, starty, doutu_tag_key[i])

        userphrase_type_key = keylog.get_keys('userphrase_type_key')
        for i in range(len(userphrase_type_key)):
            self.key_map['group_%d' % (
                i + 1)] = self._get_key_info(startx, starty, userphrase_type_key[i])
        if userphrase_type_key:
            self.key_map['add_group'] = self._get_key_info(
                startx, starty, userphrase_type_key[-1])

        userphrase_normal_key = keylog.get_keys('userphrase_normal_key')
        for i in range(len(userphrase_normal_key)):
            if userphrase_normal_key[i].shown == 'true':
                self.key_map[userphrase_normal_key[i].text] = self._get_key_info(
                    startx, starty, userphrase_normal_key[i])

        userphrase_content_key = keylog.get_keys('userphrase_content_key')
        for i in range(len(userphrase_content_key)):
            self.key_map['content_%d' % (
                i + 1)] = self._get_key_info(startx, starty, userphrase_content_key[i])

        userphrase_help_key = keylog.get_keys('userphrase_help_key')
        offset = 0
        for i in range(len(userphrase_help_key)):
            if userphrase_help_key[i].text == 'expend':
                self.key_map['expend_%d' % (
                    i + 1 - offset)] = self._get_key_info(startx, starty, userphrase_help_key[i])
            else:
                self.key_map[userphrase_help_key[i].text] = self._get_key_info(
                    startx, starty, userphrase_help_key[i])
                offset += 1

        symbol_title_key = keylog.get_keys('symbol_title_key')
        for i in range(len(symbol_title_key)):
            self.key_map[symbol_title_key[i].text] = self._get_key_info(
                startx, starty, symbol_title_key[i])

        symbol_content_key = keylog.get_keys('symbol_content_key')
        for i in range(len(symbol_content_key)):
            if symbol_content_key[i].id != 'null':
                self.key_map['symbol_%d' % (
                    i + 1)] = self._get_key_info(startx, starty, symbol_content_key[i])

    def _update_out_keys(self, keylog):
        pinyin_cloud_key = keylog.get_out_keys('pinyin_cloud')
        for i in range(len(pinyin_cloud_key)):
            self.key_map['pinyin_cloud'] = {
                'location': pinyin_cloud_key[i].location, 'attributes': pinyin_cloud_key[i]}

        composing_key = keylog.get_out_keys('composing')
        for i in range(len(composing_key)):
            self.key_map['composing'] = {
                'location': composing_key[i].location, 'attributes': composing_key[i]}

    def _parse_layout(self, layout):
        """
        {type:input_mode,method:0,layout:1,panel:7}
        """
        if not layout:
            return None
        mapped = {}
        mapped['method'] = KeyIdMap.INPUT_METHOD_MAP[layout['method']]
        mapped['layout'] = KeyIdMap.INPUT_LAYOUT_MAP[layout['layout']]
        mapped['panel'] = KeyIdMap.INPUT_PANNEL_MAP[layout['panel']]
        return mapped

    def get_keyboard_layout(self):
        """
        {'method': '拼音',
         'layout': '9键',
         'panel' : 'main',
         }
        """
        return self.layout

    def get_keyboard_location(self):
        """
        """
        return {'x': self.left,
                'y': self.top,
                'width': self.right - self.left,
                'height': self.bottom - self.top,
                }

    def get_key_attribute(self, keystr, attrname):
        keystr = keystr.lower()
        return getattr(self.key_map[keystr]['attributes'], attrname)


if __name__ == '__main__':
    pass
