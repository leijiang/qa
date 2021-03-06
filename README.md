
<h1>《客户端测试工程师技术成长路线》</h1>

**更新于20180802 by leijiang**
* [一堆废话](https://github.com/leijiang/qa/blob/master/README.md#一堆废话)

* [java基础](https://github.com/leijiang/qa/blob/master/README.md#java基础)
	* [对象导论](https://github.com/leijiang/qa/blob/master/README.md#对象导论)
	* [一切都是对象](https://github.com/leijiang/qa/blob/master/README.md#一切都是对象)
	* [操作符](https://github.com/leijiang/qa/blob/master/README.md#操作符)
	* [初始化与清理](https://github.com/leijiang/qa/blob/master/README.md#初始化与清理)
	* [访问权限控制](https://github.com/leijiang/qa/blob/master/README.md#访问权限控制)
	* [复用类](https://github.com/leijiang/qa/blob/master/README.md#复用类)
	* [多态](https://github.com/leijiang/qa/blob/master/README.md#多态)
	* [接口](https://github.com/leijiang/qa/blob/master/README.md#接口)
	* [内部类](https://github.com/leijiang/qa/blob/master/README.md#内部类)
	* [持有对象](https://github.com/leijiang/qa/blob/master/README.md#持有对象)
	* [通过异常处理错误](https://github.com/leijiang/qa/blob/master/README.md#通过异常处理错误)
	* [字符串](https://github.com/leijiang/qa/blob/master/README.md#字符串)
	* [类型信息](https://github.com/leijiang/qa/blob/master/README.md#类型信息)
	* [泛型](https://github.com/leijiang/qa/blob/master/README.md#泛型)
	* [数组](https://github.com/leijiang/qa/blob/master/README.md#数组)
	* [io系统](https://github.com/leijiang/qa/blob/master/README.md#io系统)
	* [注解](https://github.com/leijiang/qa/blob/master/README.md#注解)
	* [并发](https://github.com/leijiang/qa/blob/master/README.md#并发)

* [git基础](https://github.com/leijiang/qa/blob/master/README.md#git基础)
	* [git分支管理策略](https://github.com/leijiang/qa/blob/master/README.md#git分支管理策略)
	* [git工作流程](https://github.com/leijiang/qa/blob/master/README.md#git工作流程)
	* [git远程操作详解](https://github.com/leijiang/qa/blob/master/README.md#git远程操作详解)

* [maven基础](https://github.com/leijiang/qa/blob/master/README.md#maven基础)
	* [maven入门介绍](https://github.com/leijiang/qa/blob/master/README.md#maven入门介绍)
	* [maven实战之初识Maven](https://github.com/leijiang/qa/blob/master/README.md#maven实战之初识maven)
	* [maven的基本使用](https://github.com/leijiang/qa/blob/master/README.md#maven的基本使用)
    * [两小时从零到了解](https://github.com/leijiang/qa/blob/master/README.md#两小时从零到了解)

* [android开发](https://github.com/leijiang/qa/blob/master/README.md#android开发)
    * [android开发](https://github.com/leijiang/qa/blob/master/README.md#android开发)

* [android自动化测试](https://github.com/leijiang/qa/blob/master/README.md#android开发)
    * [android自动化测试](https://github.com/leijiang/qa/blob/master/README.md#android自动化测试)

* [appium教程](https://github.com/leijiang/qa/blob/master/README.md#appium教程)
    * [appium教程](https://github.com/leijiang/qa/blob/master/README.md#appium教程)
    
* [appium基础](https://github.com/leijiang/qa/blob/master/README.md#appium基础)
    * [appium文档](https://github.com/leijiang/qa/blob/master/README.md#appium文档)

* [测试汇总](https://github.com/leijiang/qa/blob/master/README.md#测试汇总)
    * [文档教程](https://github.com/leijiang/qa/blob/master/README.md#文档教程)      

# 一堆废话
 * 开始之前先说点废话,先申明下下面这个只是我学习一门技术的方法,并不是对每个人都适用,
   学习一门新东西的过程是理解三个W的过程,what、how、why
   * what:首先不用要求了解其原理,`快速`需要知道ta是什么,解决什么一类问题,基本怎么使用的,这个阶段一般找些quick start文档或者tutorial 教程
   * how:这个阶段对新技术有一定了解了,需要结合详细的教程,阅读完整的教材书籍,详细掌握其用法及掌握api,能熟练掌握
   * why:这个阶段是深入理解了,知其然,知其所以然,了解其原理,能对比跟类似的其他解决方案的优缺点,什么场景下适用合适,技术选型

# java基础

## 对象导论
* [《对象导论》](https://blog.csdn.net/wang_chaunwang/article/details/79893480)
    * 这个地方简单理解对象,就是一个实体,有行为(方法)跟状态(属性),拿人这个对象来举例子,人跑步是方法,人的年龄是状态

## 一切都是对象
* [《一切都是对象》](https://blog.csdn.net/wang_chaunwang/article/details/79915755)
    * 主要是一种思想,面对对象的思想,区别与面向过程而言,面向对象三个特征:封装(逻辑对外不可见,) 继承(儿子继承老子) 多态 (这个有点复杂,就理解为程序运行时候的动态绑定吧)

## 操作符
* [《操作符》](https://blog.csdn.net/wang_chaunwang/article/details/79923394)

## 初始化与清理
* [《初始化与清理》](https://blog.csdn.net/wang_chaunwang/article/details/79937743)

## 访问权限控制
* [《访问权限控制》](https://blog.csdn.net/wang_chaunwang/article/details/79947951)
    * 主要是权限的访问,private 只有自己类的成员可以访问 protected 类自己跟子类可以访问  public 谁都可以访问

## 复用类
* [《复用类》](https://blog.csdn.net/wang_chaunwang/article/details/79958084)

## 多态
* [《多态》](https://blog.csdn.net/wang_chaunwang/article/details/79986671)

## 接口
* [《接口》](https://blog.csdn.net/wang_chaunwang/article/details/80015761)
    * 简单理解为能力好了,鸟可以飞翔,飞翔就是一种能力;

## 内部类
* [《内部类》](https://blog.csdn.net/wang_chaunwang/article/details/80027505)

## 持有对象
* [《持有对象》](https://blog.csdn.net/wang_chaunwang/article/details/80037280)

## 通过异常处理错误
* [《通过异常处理错误》](https://blog.csdn.net/wang_chaunwang/article/details/80048501)

## 字符串
* [《字符串》](https://blog.csdn.net/wang_chaunwang/article/details/80076554)

## 类型信息
* [《类型信息》](https://blog.csdn.net/wang_chaunwang/article/details/80104776)

## 泛型
* [《泛型》](https://blog.csdn.net/wang_chaunwang/article/details/80141419)
    * 举个例子,用个列表存储整数 ,用个列表存储字符串 可以分别声明 ,List<Integer> List<String> 实际上都是List  列表
    * java泛型 在运行时是擦除的,这个注意下

## 数组
* [《数组》](https://blog.csdn.net/wang_chaunwang/article/details/80141577)

## io系统
* [《io系统》](https://blog.csdn.net/wang_chaunwang/article/details/80141939)
    * 主要是读取文件

## 注解
* [《注解》](https://blog.csdn.net/wang_chaunwang/article/details/80148352)
    * 简单理解就是做标记,做一些元数据的信息补充

## 并发
* [《并发》](https://blog.csdn.net/wang_chaunwang/article/details/80165133)
    * 这个比较复杂,主要是多线程的场景,多个线程对共享资源操作,容易出现问题,需要进行同步解决


# git基础

## Git分支管理策略
* [《Git分支管理策略》](http://www.ruanyifeng.com/blog/2012/07/git.html)

## Git工作流程
* [《Git工作流程》](http://www.ruanyifeng.com/blog/2015/12/git-workflow.html)

## Git远程操作详解
* [《Git远程操作详解》](http://www.ruanyifeng.com/blog/2014/06/git_remote.html)

# maven基础

## maven入门介绍
* [《Maven入门介绍》](https://www.jianshu.com/p/39875424be3c)

## maven实战之初识Maven
* [《Maven实战之初识Maven》](https://www.jianshu.com/p/0ebebab8d413)

## maven的基本使用
* [《Maven的基本使用》](https://www.jianshu.com/p/6494be5582df)

## 两小时从零到了解
* [《两小时从零到了解》](https://www.jianshu.com/p/78c16fc600a9)

## android开发
* [《android开发》](https://pan.baidu.com/s/1Q1fSqikE7AiataTaLQYwpg#list/path=%2F)

## android自动化测试
* [《android自动化测试》](https://pan.baidu.com/s/1Ghftr611cEzLFxYSFr0_FA)

## appium教程
* [《appium教程》](https://pan.baidu.com/s/1t7PAnkvVPOo5vjIE2jxy3w)

## appium基础
* [《appium文档》](http://www.testclass.net/appium)

## 测试汇总
* [《文档教程》](http://www.testclass.net)
