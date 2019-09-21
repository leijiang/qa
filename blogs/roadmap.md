### 杂七杂八一些整理
######   Robot Framework是什么? 什么是关键字驱动测试？⭐⭐⭐⭐⭐
>网上都是千遍一律的上来就说rf怎么搭建怎么使用，竟然没有人能把rf 说清楚，除了下面这篇文章，让人有点惊讶。
*   https://blog.csdn.net/ojiawang/article/details/51476280
*   https://www.open-open.com/ppt/a51d1092d1f84e85b7003ae4edd43e65.html

######   Robot Framework  和 Appium 是什么关系，是怎么联系起来的？
> 把一个自动化框架比喻为一台运作的车子，编写测试用例（Robot Framework 里面编写测试用例估计比较容易或者轻松）的工程师是驾驶员，真正执行测试用例的 test libraries 是发动机，那么把驾驶员的意图传动到发动机的就是 Robot Framework，无论是认为他是解释层，胶水层，还是xxx都好，他的作用很明显，你要把握下方向盘，踩踩油门或者刹车，就能运作的很好了，当然记得遵守交规。
>  robotframework+appium 中的 Appium 就是一个发动机。其实你了解 robotframework 的话，你应该知道他有不同的发动机，比如 Webdriver，比如数据库连接，反正很多就是了。
> 接着轮到 Appium，Appium 本身可以成为一个自动化框架，也就是说他本身也是一台可以运作的车子（需要 xunit 的支持），你可以使用各种 bindings 来写测试脚本，然后通过 Webdriver protocol 和 Appium Server 交互， Appium Server 则驱动各种driver 去干活。

>上面一堆blabla的说的是什么意思呢，按照我的理解，就是说rf一个基于关键字的自动化测试框架，提供了关键字的方式录入测试用例、rf 框架会去回去解析、管理、并且运行这些case，
>这个地方要特别注意的一点是RF 跟客户端测试没毛关系，不管是android 、ios 还是pc、h5 ，还是接口测试、web页面测试等等（他提供了关键字的方式录入测试用例、rf 框架会去回去解析、管理、并且运行这些case，没有与任何平台做绑定）
>但是具体去做事呢，可能需要别的组件来做，比方说我要做客户端测试这时我需要appium ，就需要针对appium 这个库或者组件模块封装rf关键字 提供给脚本编写者使用（如果用appium的话，如果用monkey什么的另说），那我就需要调用appium ，我需要针对appium开发关键字，这个关键字叫技术关键字
>（关键字是分层的知道吧，不知道的话自己去看哈，我还是说下吧，分高级关键字、低级关键字、和技术关键字,高级关键字是油低级关键字构成，更多描述一个场景，比方说登陆，登陆由打开浏览器、输入用户名密码、提交三个步骤或者关键字组成，技术关键字就是具体实现了）
>类似这样的一些库![设计分层](/images/WechatIMG2.png)，要是我没猜错的话，这些库都是给rf 封装关键字的；Appium Library 是封装Appium 库的 rf关键字的，
 > robotframework-excellib 是 封装excel操作库 rf关键字的、robotframework-seleniumlibrary  是 封装selenium操作库 rf关键字的 （浏览器操作），运行的时候 rf回去解析这些关键字，调用具体的库去做具体的事情，调用appium 去做客户端测试、调用excel去做excel读写，调用selenium 去做浏览器打开、关闭、访问网页或者网页元素；
*   https://testerhome.com/topics/5131#reply-44405

######   github上面的一些资料 ⭐⭐⭐⭐⭐
>这个是我看到的整理最全的自动化测试技术图谱,目前在github 上已经有3000多个star了
*   https://github.com/atinfo/awesome-test-automation/blob/master/python-test-automation.md

######   两个阿里开源的自动化测试框架
*   https://macacajs.github.io/zh/guide/  和https://github.com/alibaba/f2etest 


######   接口自动化测试平台
*   https://github.com/githublitao/api_automation_test

######  讯飞脚本
>讯飞那个脚本我简单看下了，如果你要是理解了[ppt](https://www.open-open.com/ppt/a51d1092d1f84e85b7003ae4edd43e65.html) 这篇ppt说的内容你就理解了，
![设计分层](/images/WechatIMG1.jpeg)
>rf 测试设计是分层的：1） 描述层（写用例，不需要了解关键字以及关键字的实现） 2）实现层（需要熟悉关键字和rf 语法） 3）驱动层 （关键字的实现）
>讯飞这个包里面我看了 什么Lib结尾的就是<strong style='color:read'>关键字的实现</strong>，所以一定是开发的人写的，相当于开发测试库
>多说一句，我觉得要是做自动化测试，至少2、3 层都要会写，1）2）层都是在使用 ，算不上自动化测试，就是用table 、xml、html的方式写用例
*  https://www.open-open.com/ppt/a51d1092d1f84e85b7003ae4edd43e65.html


###### 提问区
*   rf的测试库可以通过其他语言来编辑，这个编辑是在哪里编辑
>在哪编辑？IDE呀，java语言就是java ide呀， python就是python ide呀，这个说的是支持语言之间相互调用

*   rf里所说的标准库就是测试库吧，那外部库主要又包含了哪些内容
>标准库就是官方的内置库，buildin 、xml  操作这些，外部库很多呀，比方selenium library appium等 都算

*   在哪里可以看到rf自带的测试库中的关键字
>buildin 、xml、string、remote等等，链接点进去看下[链接](https://www.cnblogs.com/loleina/p/5528287.html)


*   数据驱动就是我们写的关键字中的数据，例如登录输入用户名、密码中的数据？
>数据驱动是说rf 的开发模式或者推崇的思想，数据驱动开发模式就是关注点可以放在数据上，就好比针对一个场景沟通不同的数据进行测试，关注点落在数据上


*   驱动层中的关键字是在测试库中实现吧
>嗯

*   rf测试库包含技术层面和业务层面，这两个层面中的内容我需要都了解？
> ![分层](/images/WechatIMG1.png)，看你是什么角色了，如果是不懂技术的功能测试人员只需要了解业务层面 就是编写case就好了，如果稍微懂点技术 熟悉rf脚本的开发人员可以编写
>高级关键字，如果是开发人员就需要了解实现了就是测试库了，rf 就是兼顾了多个开发角色，让每个人做自己擅长的事情，你最好都要了解，
>最好的转变就是从 写业务case => 编写高级关键字 => 编写测试库

*   怎么查看rf中是否引用了selenium library库
>倒入了selenium package了呀 ![分层](/images/WechatIMG3.png)


*   能不能学下markdown ，归档的好乱呀。。



9月21日：
#####  **我理解的库文件扩展是这样的：**

1、首先我们会在python里的site-packages中创建ifly这个我们需要的自定义扩展库，然后在库文件中定义测试库的版本信息。
*   理解不是很对，放不放在site-packages下无所谓，site-packages 只是你在python脚本里面去写import 包的时候的一个搜索路径，跟java classpath类似，如果是使用ride导入文件的话放哪一样


2、然后我们会在ifly这个库中创建keywords.py关键字，但是创建好的关键字如果需要在rf中使用，我们必须得创建一个__init__.py文件（这个文件我看了下里面引入了很多其它文件夹，这么做的原因是需要使用这些类是么）
，而这个文件主要是用于定义自定义库的信息和需要用到的keywords调用继承和声明。
*   keywords.py这个文件没用
*   __init__.py 是申明当前文件夹是作为一个模块的，跟RF本身没关系，python 的语法，申明过后相当于整个文件夹就是个模块（别人可以导入你这个模块了），这里的模块类似java里面jar包
*   "这个文件我看了下里面引入了很多其它文件夹" 说法不对，import的是要么是模块要么是具体的类，肯定不会是文件夹， `__init__.py 文件在别人import 你的这个模块的时候， __init__.py里面的代码就会执行`,RF会去导入这个模块
*   "这么做的原因是需要使用这些类是么" 嗯是的，前面说了，"文件主要是用于定义自定义库的信息和需要用到的keywords调用继承和声明" 是的，这个地方会去声明一些类，RF 会去拿到这个申明类下面的所有的方法，类似这样的方法delete_phone_file，然后RF 自动就这个方法生成为一个关键字DELETE PHONE FILE，至于为啥是这个，应该是`约定` 
*   这是关键字实现代码：[1WechatIMG2](../images/1WechatIMG2.png)，这是RF根据方法描述自动生成的关键字描述文档[1WechatIMG2](../images/1WechatIMG4.png) 
 

3、最后我们需要使用这些关键字时会在rf中导入__init__.py文件下IflyAppiumLib类，例如我们会在Keywords这个文件夹setting导入Library iFly.IflyAppiumLibrun_on_failure=Capture Page Screenshot。


#####  **提问：**

1>在site-packages中的ifly中创建的版本号就是ROBOT_LIBRARY_VERSION = '0.1.0'信息吧？？
*   不知道你表达的是什么意思，一般在 `__init__.py` 申明扩展关键字的时候加上    `ROBOT_LIBRARY_SCOPE = 'GLOBAL'`  `ROBOT_LIBRARY_VERSION = '0.1.0'` 这两个东西一个是说扩展库的版本和使用范围，`RF框架读取这两个字段` 
                        

2>在ifly中keywords.py中是空的，这个是空的原因是不是因为在rf中导入Library  iFly.IflyAppiumLib库文件后，keywords是我自己写的那些关键字。
*   前面说了，关键字是 是根据`__init__.py` 你申明的类的方法自动生成的，并且是按照约定生成， keywords没用


话说大爷我这样排版，可以吗？

