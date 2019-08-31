#-*- coding: UTF-8 -*-

import time, os, re
from selenium.common.exceptions import WebDriverException
from robot.api import logger
from appium.webdriver.common.touch_action import TouchAction

class HandWriteHelper():
    
    def half_screen_hand_write_mu(self, duration=500):
        """
        半屏手写“木”字
        """
        location = self.keyboard.get_keyboard_location()
        start_x, start_y = location['x'] + 10, location['y'] + 80
        width, height = location['width'] - 50, location['height'] - 150
        #hen
        self.swipe(start_x+width/5, start_y+height/5, start_x+width*4/5, start_y+height/5, duration)
        #shu
        self.swipe(start_x+width/2, start_y+height/20, start_x+width/2, start_y+height, duration)
        #pie
        self.swipe(start_x+width/2, start_y+height/5, start_x+width*3/10, start_y+height*19/20, duration)
        #la
        self.swipe(start_x+width/2, start_y+height/5, start_x+width*7/10, start_y+height*19/20, duration)
        
        time.sleep(1.5)
        self.update_keyboard()
        
    def full_screen_hand_write_mu(self, start_x=50, start_y=200, width=350, height=200, duration=500):
        """
        全屏手写“木”字
        """
        start_x, start_y, width, height = map(int, [start_x, start_y, width, height])
        #hen
        self.swipe(start_x+width/5, start_y+height/5, start_x+width*4/5, start_y+height/5, duration)
        #shu
        self.swipe(start_x+width/2, start_y+height/20, start_x+width/2, start_y+height, duration)
        #pie
        self.swipe(start_x+width/2, start_y+height/5, start_x+width*3/10, start_y+height*19/20, duration)
        #la
        self.swipe(start_x+width/2, start_y+height/5, start_x+width*7/10, start_y+height*19/20, duration)
        
        time.sleep(1.5)
        self.update_keyboard()
        
    def hand_write(self, word, offsetx=1, offsety=1, style='ctt1', duration=25, interval=70, logtime=1.5):
        """
        全屏手写需要指定偏移坐标，目前推荐使用全屏手写，半屏手写目前存在bug，较短的笔画易被字母按键捕获，导致手写失败
        | ARGS: |  word:   | 中文单字 |
        |       | offsetx: |  坐标偏移量 |
        |       | offsety: |  坐标偏移量  |
        |       | style:   |  手写体，请参考HandTrack目录uni文件，默认为ctt1 |
        |       | duration: |  手写速度，默认25ms，单位ms |
        |       | interval: |  笔画间隔，默认70ms，单位ms |
        
        example:
        |   Hand Write | 来 |
        |   Hand Write | 没 | 100  |  200 | ctt1 |
        """
        if not offsetx:
            location = self.keyboard.get_keyboard_location()
            offsetx, offsety = location['x'], location['y']+45
        else:
            offsetx, offsety = int(offsetx), int(offsety)
        movements = self._get_movements(word, style)
        for mov in movements:
            action = TouchAction(self._current_application())
            lastloc = (mov[0][0], mov[0][1])
            action.press(x=lastloc[0]+offsetx, y=lastloc[1]+offsety).wait(ms=duration)
            if len(mov) == 2:
                action.move_to(x=mov[1][0]+offsetx, y=mov[1][1]+offsety).wait(ms=duration)
            else:
                for loc in mov[1:]:
                    action.move_to(x=loc[0]-lastloc[0], y=loc[1]-lastloc[1]).wait(ms=duration)
                    lastloc = loc
                action.move_to(x=1, y=1)
            action.release().perform()
            time.sleep(float(interval)/1000.0)
        logtime = float(logtime)
        if logtime != 0.0:
            time.sleep(logtime)
            self.update_keyboard()
        
    def _get_movements(self, word, style):
        """
        """
        try:
            data = self._read_style(style)[''.join([w[4:-1] for w in map(repr, list(word))])]
        except KeyError:
            raise AssertionError(u'Word %s:%s not found in the hand write resource file %s.uni!' % (word, repr(word)[4:-1], style))
        movements = []
        movement = []
        for line in data.splitlines():
            if line == '.PEN_DOWN':
                movement = []
                pass
            elif line == '.PEN_UP':
                if movement:
                    movements.append(movement)
                movement = []
            else:
                x, y = map(int, map(str.strip, line.split('-')))
                movement.append((x, y))
        return movements
    
    def _read_style(self, style):
        """
        .SEGMENT LINE ? ? "0x7b49"
        .END_SEG LINE ? ? "0x7b49"
        .SEGMENT LINE ? ? "0x6765 0x4e00 0x6876"
        """
        styles = {}
        fpath = os.path.join(os.path.dirname(__file__), 'HandTrack/%s.uni' % style)
        if not os.path.exists(fpath):
            raise AssertionError('Style file not exist, please check your input. %s' % style)
        re_word = re.compile(r'''\.SEGMENT\sLINE\s\?\s\?\s\"(.+?)\"\s+(.+?)\s+\.END_SEG\sLINE''', re.DOTALL)
        with open(fpath, 'rb') as fp:
            data = fp.read()
        ret = re_word.findall(data)
        for words in ret:
            styles[''.join([word[2:] for word in words[0].split()])] = words[1]
        return styles
    
    def _hand_swipe(self, start_x, start_y, end_x, end_y, duration=1000):
        """
        On some android 4.1.1 version devices， swipe command will not work as expected
        WebDriverException
        """
        try:
            self.swipe(start_x, start_y, end_x, end_y, duration)
        except WebDriverException:
            logger.warn('The swipe did not complete successfully')
        
if __name__ == '__main__':
    a = HandWriteHelper()._read_style('ctt1')
    print a['7b49']