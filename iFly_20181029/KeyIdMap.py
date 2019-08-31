#-*- coding:utf-8 -*-

KEY_ID_MAP = {u'1101': [u'smile', u'切换表情'],
              u'1102': [u'abc', u'ABC键'],
              u'1103': [u'def', u'DEF键'],
              u'1104': [u'ghi', u'GHI键'],
              u'1105': [u'jkl', u'JKL键'],
              u'1106': [u'mno', u'MNO键'],
              u'1107': [u'pqrs', u'PRRS键'],
              u'1108': [u'tuv', u'TUV键'],
              u'1109': [u'wxyz', u'WXYZ键'],
              u'1110': [u'symbol', u'符号切换键'],
              u'1111': [u',', u'逗号键'],
              u'1112': [u'space', u'空格键'],
              u'1113': [u'convert', u'中英切换键'],
              u'1114': [u'.', u'句号键'],
              u'1115': [u'del', u'退格键'],
              u'1116': [u'ab', u'字母切换键'],
              u'1117': [u'split', u'分词键'],
              u'1118': [u'number', u'数字切换键'],
              u'1119': [u'enter', u'回车键（普通回车）'],
              u'1120': [u'enter', u'回车键（go）'],
              u'1121': [u'enter', u'回车键（完成）'],
              u'1122': [u'enter', u'回车键（next）'],
              u'1123': [u'enter', u'回车键（搜索）'],
              u'1124': [u'clear', u'清除键'],
              u'1125': [u'q', u'Q键'],
              u'1126': [u'w', u'W键'],
              u'1127': [u'e', u'E键'],
              u'1128': [u'r', u'R键'],
              u'1129': [u't', u'T键'],
              u'1130': [u'y', u'Y键'],
              u'1131': [u'u', u'U键'],
              u'1132': [u'i', u'I键'],
              u'1133': [u'o', u'O键'],
              u'1134': [u'p', u'P键'],
              u'1135': [u'a', u'A键'],
              u'1136': [u's', u'S键'],
              u'1137': [u'd', u'D键'],
              u'1138': [u'f', u'F键'],
              u'1139': [u'g', u'G键'],
              u'1140': [u'h', u'H键'],
              u'1141': [u'j', u'J键'],
              u'1142': [u'k', u'K键'],
              u'1143': [u'l', u'L键'],
              u'1144': [u'z', u'Z键'],
              u'1145': [u'c', u'C键'],
              u'1146': [u'v', u'V键'],
              u'1147': [u'b', u'B键'],
              u'1148': [u'n', u'N键'],
              u'1149': [u'm', u'M键'],
              u'1150': [u'short', u'短斜线键'],  # TODO
              u'1151': [u'heng', u'“一”键'],
              u'1152': [u'shu', u'“丨”键'],
              u'1153': [u'pie', u'“丿”键'],
              u'1154': [u'dian', u'“丶”键'],
              u'1155': [u'zhe', u'“ㄥ”键'],
              u'1156': [u'*', u'通配符键(笔画，功能键)'],
              u'1157': [u'convert', u'英中切换键'],
              u'1158': [u'shift', u'切换大小写键（小写状态）'],
              u'1159': [u'shift', u'切换大小写键（大写状态）'],
              u'1160': [u'shift', u'切换大小写键（锁定状态）'],
              u'1161': [u'1', u'数字键1'],
              u'1162': [u'2', u'数字键2'],
              u'1163': [u'3', u'数字键3'],
              u'1164': [u'4', u'数字键4'],
              u'1165': [u'5', u'数字键5'],
              u'1166': [u'6', u'数字键6'],
              u'1167': [u'7', u'数字键7'],
              u'1168': [u'8', u'数字键8'],
              u'1169': [u'9', u'数字键9'],
              u'1170': [u'0', u'数字键0'],
              u'1171': [u'@', u'“@”键'],
              u'1172': [u'switch', u'切换单字按键'],
              u'1173': [u'switch', u'切换词组按键'],
              u'1174': [u'pageup', u'上翻页键'],
              u'1175': [u'pagedown', u'下翻页键'],
              u'1176': [u'back', u'返回键'],
              u'1177': [u'复制', u'复制键'],
              u'1178': [u'全选', u'全选键'],
              u'1179': [u'选择', u'选择键'],
              u'1180': [u'粘贴', u'粘贴键'],
              u'1181': [u'剪切', u'剪切键'],
              u'1182': [u'left', u'左箭头键'],
              u'1183': [u'right', u'右箭头键'],
              u'1184': [u'up', u'上箭头键'],
              u'1185': [u'down', u'下箭头键'],
              u'1186': [u'tab', u'Tab键'],
              u'1187': [u'开头', u'Home键（开头）'],
              u'1188': [u'末尾', u'End键（末尾）'],
              u'1189': [u'del2', u'Del键'],
              u'1190': [u'', u'添加表情键'],
              u'1191': [u'?', u'问号键'],
              u'1192': [u'!', u'感叹号键'],
              u'1193': [u'handwrite', u'手写面板键'],
              u'1194': [u'topbar', u'语音界面顶部按键'],  # 语言界面
              u'1195': [u'language', u'语言选择按键'],
              u'1196': [u'help', u'求助按键'],
              u'1197': [u'mic', u'语音麦克风按键'],
              u'1198': [u'error', u'语音错误按键'],
              u'1199': [u'说完了动画', u'语音说完动画按键'],
              u'1200': [u'说完了', u'语音说完（自动按下）'],
              u'1201': [u'重新开始', u'重新开始按键'],
              u'1202': [u'重试', u'重试按键'],
              u'1203': [u'设置网络', u'设置网络按键'],
              u'1204': [u'报告错误', u'报告错误按键'],
              u'1205': [u'取消', u'取消按键'],
              u'1206': [u'说完了', u'语音说完按键'],
              u'1207': [u'unlock', u'解锁按键(符号界面)'],
              u'1208': [u'net_symbol', u'网络符号切换键(怀旧)'],
              u'1209': [u'quick_symbol', u'快速符号键(怀旧)'],
              u'1210': [u'dict', u'词典开启键'],
              u'1211': [u'dict', u'词典关闭键'],
              u'1212': [u'qw', u'QW键'],
              u'1213': [u'er', u'ER键'],
              u'1214': [u'ty', u'TY键'],
              u'1215': [u'ui', u'UI键'],
              u'1216': [u'op', u'OP键'],
              u'1217': [u'as', u'AS键'],
              u'1218': [u'df', u'DF键'],
              u'1219': [u'gh', u'GH键'],
              u'1220': [u'jk', u'JK键'],
              u'1221': [u'l', u'L键（双键）'],
              u'1222': [u'zx', u'ZX键'],
              u'1223': [u'cv', u'CV键'],
              u'1224': [u'bn', u'BN键'],
              u'1225': [u'm', u'M键（双键）'],
              u'1226': [u'：', u'“：”键（点划笔画）'],
              u'1227': [u'；', u'“；”键(点划笔画)'],
              u'1228': [u'通配', u'通配符键(点划笔画)'],
              u'1229': [u'settings', u'设置齿轮键'],
              u'1230': [u'hide', u'隐藏键'],
              u'1231': [u'more', u'更多按键'],
              u'1232': [u'aoc_clear', u'联想清除按键'],
              u'1233': [u'x', u'X键(26键)'],
              u'1234': [u'半屏', u'半/全键'],
              u'1235': [u'全屏', u'全/半键'],
              u'1236': [u'+', u'+号键'],
              u'1237': [u'-', u'-号键'],
              u'1238': [u'*', u'*号键'],
              u'1239': [u'#', u'#号键'],
              u'1240': [u'', u'（号键（拨号）'],  # TODO
              u'1241': [u'', u'）号键（拨号）'],  # TODO
              u'1242': [u'', u'暂停按键（拨号）'],  # TODO
              u'1243': [u'', u'等待按键（拨号）'],  # TODO
              u'1244': [u'', u'Not按键（拨号）'],  # TODO
              u'1246': [u'选择', u'选择键'],
              u'1250': [u'/', u'/号键'],
              u'1790': [u'选择', u'选择键'],
              u'2147483644': [u'keyboardright', u'单手模式右箭头'],
              u'2147483645': [u'switchright', u'单手模式右展开'],
              u'2147483646': [u'keyboardleft', u'单手模式左箭头'],
              u'2147483647': [u'switchleft', u'单手模式左展开'],
              # custom
              u'4000': [u'keyboard', u'输入方式'],
              u'4001': [u'voice', u'语音输入'],
              u'4002': [u'selector', u'编辑'],
              u'4003': [u'emoji', u'表情'],
              u'4004': [u'皮肤', u'皮肤'],  # Included in menu_cell_key
              u'4005': [u'词库', u'词库'],  # Included in menu_cell_key
              u'4006': [u'常用语', u'常用语'],  # Included in menu_cell_key
              u'4007': [u'繁体开关', u'繁体开关'],  # Included in menu_cell_key
              u'4008': [u'夜间模式', u'夜间模式'],  # Included in menu_cell_key
              u'4009': [u'切换单手', u'切换单手'],  # Included in menu_cell_key
              u'4010': [u'剪贴板', u'剪贴板'],  # Included in menu_cell_key
              }

INPUT_METHOD_MAP = {u'0': u'拼音',
                    u'1': u'英文',
                    u'2': u'笔画',
                    u'3': u'手写',
                    u'4': u'数字',
                    }

INPUT_PANNEL_MAP = {u'0': u'main',
                    u'1': u'more',
                    u'2': u'speech',
                    u'3': u'digit',
                    u'4': u'symbol',
                    u'5': u'edit',
                    u'6': u'emotion',
                    u'7': u'abc',
                    u'8': u'more_bh',
                    u'9': u'menu',
                    u'10': u'switch'
                    }

INPUT_LAYOUT_MAP = {u'0': u'9键',
                    u'1': u'26键',
                    u'2': u'双键',
                    u'3': u'笔画',
                    u'4': u'全屏手写',
                    u'5': u'半屏手写',
                    u'6': u'9键横屏',
                    u'7': u'笔画横屏',
                    }


def ReturnKeyID(keyid):
    keyname = KEY_ID_MAP.get(keyid, (None, None))[0]
    if not keyname:
        return False
    return True


def GetKeyNameById(keyid):
    keyname = KEY_ID_MAP.get(keyid, (None, None))[0]
    if not keyname:
        raise AssertionError(u"Key not initialized yet. %s" % keyid)
    return keyname

if __name__ == '__main__':
    pass
