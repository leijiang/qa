# encoding=utf-8
import json
import telnetlib
"""
creator: leijiang

tested in python2.7
"""
 
class Dubbo(telnetlib.Telnet,object):
    """
    简单说明下：这里测试调用com.netease.kaola.distmerchant.check.api.CheckApiFacade这个服务的queryOrderByOrderId 接口
    参数只有orderId 为  2018070419130000702273913
    逻辑基本么有：1 建立链接 2 发送命令（参数序列化） 3 返回字符串反序列化作为结果
    因为我本地python 版本是2.7 ，在python 3.3 理论上不用任何修改就可以运行，不行再吱一声
    """
 
    prompt = 'dubbo>'
    coding = 'utf-8'
 
    def __init__(self, host=None, port=0):
        super(Dubbo,self).__init__(host, port)
        self.write(b'\n')
 
    def command(self, flag, str_=""):
        data = self.read_until(flag.encode())
        self.write(str_.encode() + b"\n")
        return data
 
    def invoke(self, service_name, method_name,args):
        command_str = "invoke {0}.{1}({2})".format(
            service_name, method_name,json.dumps(args))
        print (command_str)
        self.command(Dubbo.prompt, command_str)
        data = self.command(Dubbo.prompt, "")

        data = json.loads(data.decode(Dubbo.coding, errors='ignore').split('\n')[0].strip())
        return data
 
if __name__ == '__main__':
    conn = Dubbo('10.177.34.203', 20881)
    params = "2018070419130000702273913"
    """
    再多说一句，如果参数是复杂类型，这个地方就是这样了
    params = {
        "name":"leijiang"
        "age":18
    }
    """

    result = conn.invoke(
        "com.netease.kaola.distmerchant.check.api.CheckApiFacade",
        "queryOrderByOrderId",
        params
    )
    print ('------------------')
    print (result)
    print ('------------------')