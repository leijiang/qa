###	dubbo 原理及自动化测试
####	dubbo 原理
######	注册中心zookeeper			
*	zookeeper是什么
>ZooKeeper是一个分布式的，开放的的分布式应用程序协调服务，现在由apache 基金会维护；

*	zookeeper有什么用
	*	统一命名服务
		*	zookeeper 存储数据的方式类似于在操作系统中的文件存储方式，分层存储，在zk系统中创建的节点可以保证在分布式服务器上是全局唯一的；
		*	zk存储数据，	![zk存储数据](http://img.my.csdn.net/uploads/201304/24/1366780464_8137.png)
	*	配置管理
		*	把配置信息存储到zk上，能够保证高可用，为啥能高可用？内部的zab协议保证的
	*	分布式一致性
		*	节点数据分发
		*	一台机器宕机了，zk的其他节点还是可用，当宕机机器恢复时可以同步其他机器信息
*	zookeeper原理
	*	zab协议，主要是两个部分广播 和恢复； [zab协议传送门](https://www.jianshu.com/p/fb527a64deee) 

*	zookeeper 在dubbo 中有做什么
	*	 注册中心
		*	 dubbo 通过注册zookeeper 进行服务的暴露，把服务的具体信息注册到zookeeper 上，类似这样的dubbo://192.168.0.1/com.xxx.TxxService?version=1.0.0
	*	 服务上线、下线通知
		*	 这种场景比方说大促的时候，需要增加服务，相当于新增了provider ，需要把新增加的服务通知到服务调用端 consumer 	
		*	 服务下线通知，比方说我的provider服务进行发布，需要重新启动机器，这个时候consumer 不应该再调用过来，不然提供不了服务；
######	dubbo 介绍
*	dubbo 是什么
	*	阿里开源的分布式治理框架；不仅仅提供RPC（Remote Procedure Call，相对于本地的调用，远程调用简单理解就是服务的提供跟服务的使用不在一台机器上，需要跨网络）的调用，还提供了服务的发现、暴露、软负载均衡、监控统计、failover
*	dubbo 有哪些功能
>解析服务、注册服务、发现服务、远程调用、服务调用的软负载均衡、调用情况统计、失败转移failover 

*	dubbo原理
>![avatar](https://img-blog.csdn.net/20160626200720063)

>[原理](https://blog.csdn.net/qq_33101675/article/details/78701305)
>


*	dubbo类似框架有哪些
>grpc 、tesa 、hsf
####	dubbo 自动化测试
####	基于telnet的调用
>这个是dubbo内部基于telnet协议（平时调用是dubbo协议）实现的调用，好处是直接使用命令行形式，不依赖第三方的API包，简单；python的dubbo的自动化测试 就是基于这个来写的～
####	基于泛化调用
>这种还是dubbo协议，但是不需要第三方的API包，原理是通过一个通用的服务GenericSerivice来调用，把服务的元数据描述信息通过参数封装起来；这个我也封装过，有兴趣再说




