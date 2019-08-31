###	appium 分享
#####	appium是神马
*	定义
	*	appium 是一个支持 iOS 平台和 Android 平台上的原生应用，web应用和混合应用自动化测试开源工具。
	*	备注
		*	“移动原生应用”是指那些用iOS或者 Android SDK 写的应用（Application简称app）。
		* “移动web应用”是指使用移动浏览器访问的应用（appium支持iOS上的Safari和Android上的 Chrome）。
		* “混合应用”是指原生代码封装网页视图——原生代码和 web 内容交互。比如，像 Phonegap （Phonegap 发音[foʊnɡæp] 这里解析下Phonegap，采用HTML，CSS和js技术，创建移动跨平台移动应用程序的一种技术。使开发者能够在网页中调用IOS，Android等智能手机地理定位，联系人，声音和振动核心功能），可以帮助开发者使用网页技术开发应用，然后用原生代码封装，这些就是混合应用。
##### appium原理
*	appium原理![appium原理](http://otfah9orz.bkt.clouddn.com/appium_principle.png)
	*	clien-server 结构
		*	备注：就跟我们平时浏览器访问网页，浏览器是客户端，通过操作发送请求服务器来获取数据。
	*	appium-client：提供多语言的api编写脚本、发送脚本（自动化测试命令）
		*	备注：提供多语言的api来编写自动化测试脚本，自动化测试命令被appium-client 包装成JSON 格式通过http协议发送到clien-server
	*	appium-server：
		* 接受、解析自动化测试命令、执行自动化测试命令；驱动客户端执行解析过的命令
		* 备注：接受appium-client 发送的自动化测试命令，解析，驱动Android 、IOS客户端或者虚拟机来执行解析后的命令

*	备注
	*	在Windows平台上，通过Java（ java-client ）编写了一个appium自动化脚本并执行，请求会首先到Window下的appium-Server，appium-Server通过解析，驱动Android虚拟机或真机来执行appium脚本
	*	在MAC平台上，通过Python（python-client ）编写了一个appium自动化脚本并执行，请求会首先到MAC下的appium-Server，appium-Server通过解析，驱动iOS设备来执行appium自动化脚本。

#####	特点	
*	支持多平台、多语言
	*	appium是跨平台的，可以用在OSX，Windows以及Linux桌面系统上运行。
	*	appium允许测试人员在不同的平台（iOS，Android）使用同一套API来写自动化测试脚本，这样大大增加了iOS和Android测试套件间代码的复用性
	*	备注
		*	（这里可以抛出一个问题，活跃气氛，避免一个人尬聊）appium 为什么能支持多语言？appium选择了Client/Server的设计模式。只要client能够发送http请求给server，那么的话client用什么语言来实现都是可以的，这就是appium如何做到支持多语言的原因
*	不需要修改或者重新编译APP
	*	这里抛出个问题，为什么不需要不需要修改或者重新编译APP呢？代表你思考过这个问题（实际上是由它的原理决定的，通过appium-server  端解析自动化测试命令，驱动客户端真机设备或者模拟器来执行，我看官网上面说的是叫这个  vendor specific mechanism（通过调用特定供应商机制来执行 貌似是这么翻译的） ，要是你喜欢中文中夹杂的英文你可以说.. 故不需要修改或重新编辑APP） 
*	扩展Selenium 
	*	appium类库封装了标准Selenium客户端类库。
		*	备注：（Selenium 发音[sɪˈliniəm]  呃..这种英语专业的不用多说了吧）Selenium 是一种web自动化测试的工具 ，appium类库封装了标准Selenium客户端类库， 为用户提供所有常见的JSON格式selenium命令以及额外的移动设备控制相关的命令，如多点触控手势和屏幕朝向。
	*	什么不直接使用Selenium呢？
		*	备注： 为appium 用户提供了方便的接口来执行各种设备动作，例如在测试过程中安装/卸载App。这就是为什么我们需要appium特定的客户端，而不是通用的Selenium 客户端。
		

#####	appium如何使用
*	下载Android SDK
*	安装 appium Server 
	*	window环境，下载AppiumForWindows_1_4_16_1.zip ，
	*	安装完成后，命令控制台输入appium-doctor ![appium Server](https://s33.postimg.cc/94juvshj1/Wechat_IMG1.png?dl=1) 
		* 备注： appium-doctor 是环境诊断命令，如果运行如图就是按照ok的，如果提示：“appium-doctor”不是内部或外部命令，找到Appium的安装目录，添加到环境变量path下面（参考Java环境的设置）
* java-client安装 （java 客户端）
	*	安装Java 环境
		*	备注：这样提一句配置jAVA_HOME 环境变量，这样显得你真的配置过，专业
	*	安装开发IDE ，推荐使用 IntelliJ IDEA 
		*	备注（ IntelliJ IDEA  发音美[aɪˈdi:ə]，就是你用的那个， 有些同学使用Eclipse也是可以的，但个人觉得还是 IntelliJ IDEA   最牛逼，不接受反驳 ）
	*  安装Maven  ，java 包管理工具
		*  备注，发音[ˈmevən]，java 包管理工具，主要方便好管理， （当然手动导入java包也可以，low些，没什么好说的）
* appium 使用 	
	* 搭建maven项目以及添加依赖![搭建maven项目](http://otfah9orz.bkt.clouddn.com/appium_idea_maven.png) 
	*	启动Android模拟器![启动Android模拟器](http://otfah9orz.bkt.clouddn.com/appium_android_system.png) 
		*	备注：这个地方你自己看，貌似看你是用真机玩的，可以你截个图修改掉
	* 启动 appium server![Appium Server](http://otfah9orz.bkt.clouddn.com/appium_server_view.png) 
	*  编写appium  client脚本![Appium Server](https://s33.postimg.cc/tna5nfqql/Wechat_IMG7.png?dl=1) 
	*  运行结果
		* ![运行](http://otfah9orz.bkt.clouddn.com/appium_run_calculator.png) 		
#####	我们用appium做神马
* 蘑菇街的自动化测试
	*   备注：下面的这些你之前弄过 ，随便截图几个代码片段，运行效果贴上面就好了
	* Desired Capabilities
		* #appium related setting 
appium.target.app=mogujie
appium.target.os=android
appium.target.type=device
appium.target.device.name=OPPO
R7sm
appium.ios.version=
appium.android.version=5.1
		* #mogujie app related setting
mogujie.ios.simulator=
mogujie.android.simulator=
mogujie.ios.device=
mogujie.android.device=/Users/qianqian/package/
A1d957223582000802.5729f0367538e.apk
		* #appium related setting
appium.target.app=mogujie
appium.target.os=ios
appium.target.type=Simulator
appium.target.device.name=iPhone6s
appium.ios.version=9.2
appium.android.version=
		* #mogujie app related setting
mogujie.ios.simulator=/Users/qianqian/package/Mogujie4iphone.zip
mogujie.android.simulator=
mogujie.ios.device=
mogujie.android.device=
	* sessions
	```java
driver = AppDriver.getDriver();
        case "ios":
            webDriver = new IOSDriver<MobileElement>(new URL("h3p://127.0.0.1:4723/wd/hub"), capabili8es);
            break;
        case "android":
            webDriver = new AndroidDriver<MobileElement>(new URL("h3p://127.0.0.1:4723/wd/hub"), capabili8es);
            break;
	```
	* 登录自动化测试![登录自动化测试](https://s33.postimg.cc/s9iis7z7x/Wechat_IMG5.png?dl=1)![登录自动化测试](https://s33.postimg.cc/5rbm9k8nx/Wechat_IMG6.png?dl=1)
		* 备注：自己准备几个图
#####	更多资料
*	Appium中文站 http://appium.io/index.html?lang=zh
