###	基于telnet 的dubbo接口自动化测试 
####	什么是telnet
>Telnet协议是TCP/IP协议的其中一部分，是Internet远程登陆服务的标准协议；好比ssh 也是远程登录方式的一种，只是协议不同，所谓协议简单理解就是双方约定好了的契约，他的通信方式是这样的
![telnet通信](https://gss3.bdstatic.com/7Po3dSag_xI4khGkpoWK1HF6hhy/baike/c0%3Dbaike72%2C5%2C5%2C72%2C24/sign=ab66ce1e1bd8bc3ed2050e98e3e2cd7b/a08b87d6277f9e2fc0ef662c1d30e924b899f338.jpg)

####	telnet 怎么使用
```bash
telnet host port
```
譬如
```bash
telnet baidu.com 80
```
####	dubbo 是如何支持telnet的
>duubo 默认的transport协议叫做netty协议，当然还有其他很多的协议譬如netty4、mina、grizzly（这些通信协议就是平时开发项目时使用的方式）因为dubbo 实现了自己的SPI机制，可以去dubbo jar 包目录下去看，类似这样的；

![dubbo transport协议](https://haitao.nos.netease.com/d5a07510-2cf0-4ccb-9539-486c8f04092c_1908_824.png)
并且dubbo内部也对telnet 协议做了支持， dubbo 是怎么支持telnet的呢？
dubbo 在内部对客户端使用tenlet 传递到duubo 的telnet 每条命令都做了解析，具体到解析逻辑还是使用了SPI的扩展机制，在jar 包里面
![dubbo  telnet 实现](https://haitao.nos.netease.com/f332fbd7-080f-4d4d-8b52-a17f47664c26_2222_630.png)

####	使用telnet命令行调用dubbo
>这个没啥好说的，举个栗子，怎么建立连接
```bash
telnet 10.177.34.203 20881
```
这里的`10.177.34.203` 是我的dubbo provider 就是dubbo 服务提供者服务器，再说一次dubbo 服务提供者服务器，不是zk 服务器 ，不是consumer 服务器 ；这个地方再多说句，看下你本地是否能ping通这个服务器，ping不通，下面的说的都白搭，ping不通的话要么到跳板机上去运行，要么本地链接vpn，`20881`  是dubbo 服务暴露端口

```bash
ls
```
建立连接过后，使用ls查看这台服务器暴露的dubbo服务有哪些
![ls](https://haitao.nos.netease.com/bb6059cc-3260-44cc-9ef9-49ffccd93e37_2578_902.png)
```bash
ls com.netease.kaola.distmerchant.check.api.CheckApiFacade
```
ls  服务器完整名，可以查个这个服务下具体的dubbo接口有哪些
com.netease.kaola.distmerchant.check.api.CheckApiFacade 是指服务的具体完整名称，譬如：
![ls](https://haitao.nos.netease.com/b1a71300-f490-43ba-ad6a-c3af3b0c3a24_1998_346.png)
再说最重要的一个命令`invoke`调用

```bash
invoke com.netease.kaola.distmerchant.check.api.CheckApiFacade.queryOrderByOrderId("2018070419130000702273913")
```
![ls](https://haitao.nos.netease.com/107030aa-d110-4012-b2cb-df4840b0d062_2878_372.png)

更多其他的命令，放这了[dubbo telnet 命令](http://alibaba.github.io/dubbo-doc-static/Telnet+Command+Reference-zh-showComments=true&showCommentArea=true.htm)，不过估计也不会看～～

####	使用python脚本基于telnet 进行dubbo自动化测试
>python 有个telnetlib的包 （这个跟dubbo 调用没毛关系），里面把telnet 怎么建立连接，怎么发送命令用python API 的方式提供了，简单的说就是利用python 代码来调用telnet，不用在命令行里面去敲了，然后我封装的那个基于telnet的dubbo 自动化测试，原理也比较简单，因为本身dubbo对telnet 命令进行了解析支持，再使用这个telnetlib 包进行dubbo telnet 建立链接、发送命令（查看服务、调用）就可以了，然后拿到telnet 的返回值，实际上就是dubbo调用服务的结果了，工具代码我放在了[dubbo 自动化](https://github.com/leijiang/qa/tree/master/dubbo) 了，其中[telnetlib 安装](https://github.com/leijiang/qa/tree/master/dubbo/install.sh) 是telnetlib 安装 命令，如果本地有就算了，没有的话 ，运行的sh 进行安装，（ps ： 知道怎么看 安装么有么？哎 ....,打开命令工具

![dubbo telnet 命令](https://haitao.nos.netease.com/f3c995cf-69c1-4485-a723-5b0978a4d421_2874_396.png)
这两步都没出错，恭喜你 ，安装成功了～
自动化测试代码我放这里了[dubbo.py](https://github.com/leijiang/qa/tree/master/dubbo/dubbo.py) ，怎么运行，不用我说了吧.... 算了还是说下：
```bash
python dubbo.py
```
亲测，通过.

![dubbo](https://haitao.nos.netease.com/171ed9bd-aa8c-4147-80d7-f3510de8b849_2878_406.png)







