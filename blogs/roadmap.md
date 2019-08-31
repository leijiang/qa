### 杂七杂八一些整理
######   Robot Framework是什么? 什么是关键字驱动测试？
>网上都是千遍一律的上来就说rf怎么搭建怎么使用，竟然没有人能把rf 说清楚，除了下面这篇文章，让人有点惊讶。
>https://blog.csdn.net/ojiawang/article/details/51476280
>https://www.open-open.com/ppt/a51d1092d1f84e85b7003ae4edd43e65.html

######   Robot Framework  和 Appium 是什么关系，是怎么联系起来的？
> 
>https://testerhome.com/topics/5131#reply-44405

######   github上面的一些资料
>这个是我看到的整理最全的自动化测试技术图谱,目前在github 上已经有3000多个star了
>https://github.com/atinfo/awesome-test-automation/blob/master/python-test-automation.md

######   两个阿里开源的自动化测试框架
>https://macacajs.github.io/zh/guide/  和https://github.com/alibaba/f2etest 


######   接口自动化测试平台
>https://github.com/githublitao/api_automation_test

######  讯飞脚本
>讯飞那个脚本我简单看下了，如果你要是理解了https://www.open-open.com/ppt/a51d1092d1f84e85b7003ae4edd43e65.html 这篇ppt说的内容你就理解了，
![设计分层](/images/WechatIMG1.jpeg)
>rf 测试设计是分层的：1） 描述层（写用例，不需要了解关键字以及关键字的实现） 2）实现层（需要熟悉关键字和rf 语法） 3）驱动层 （关键字的实现）
>讯飞这个包里面我看了 什么Lib结尾的就是<strong style='color:read'>关键字的实现</strong>，所以一定是开发的人写的，相当于开发测试库
>多说一句，我觉得要是做自动化测试，至少2、3 层都要会写，1）2）层都是在使用 ，算不上自动化测试，就是用table 、xml、html的方式写用例
>