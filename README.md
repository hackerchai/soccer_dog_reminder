Soccer Dog Reminder
======
一个能够自动提醒足球赛事的Python脚本

功能
----
每天在固定时间检测48小时内到来的足球赛，如果有比赛则短信提醒。

截图
----

![](https://blog.hackerchai.com/wp-content/uploads/2018/02/photo_2019-04-12_15-22-00.jpg)

![](https://blog.hackerchai.com/wp-content/uploads/2018/02/soccer_dog_reminder_result.png)


安装需求
-----
* Linux Distributions
* Python2.7
* urllib、urlib2、json

安装
----
本项目基于两个在线API，所以安装时需要另行申请注册

### 1.配置API

* 足球赛事API来源于[聚合数据](https://www.juhe.cn/docs/api/id/90),需要用户自行进行注册获取api_key，再填入`soccer_dog_reminder.py`文件对应`football_api_appkey = ""`的位置

* 短信发送API来源于阿里云市场[【官方106三网短信】短信平台/短信免费试用/短信验证码/短信通知/短信群发推广—短信API接口对接](https://market.aliyun.com/products/56928004/cmapi023305.html?spm=5176.2020520132.101.3.684b72186EMJey#sku=yuncode1730500007)，设置好短信模板后请讲模板编号写入`soccer_dog_reminder.py`文件对应`sms_api_appskin = ""`的位置，同时将阿里云后台显示的APPCODE一并写入`sms_api_appcode = ""`,需要用户自行付费购买服务，其中短信模板如下：

````
【足球狗赛事推送】您关注的球队#team1#有比赛啦！#type#对阵#team2# ，时间是#date#，还有#hour#小时开赛
````

### 2.配置crontab

完成上述API配置后请安装crontab相关服务，具体操作如下：
````bash
cd soccer_dog_reminder
chmod a+x ./soccer_dog_reminder_init.sh
./soccer_dog_reminder_init.sh
````
如果想改变提醒时间和次数等相关设置可以修改`soccer_dog_reminder_init.sh`中的crontab参数来完成

### 3.加入个性化数据
修改`soccer_dog_reminder.py`文件对应`football_club = ""`的位置，比如**巴塞罗那**，填入自己喜爱的主队名称，注意，这里一定是官方中文译名，不能是简称

同时修改`phone = ""`，填入希望接到提醒短信的手机号码，支持中国内地全网号码

## 许可证

MIT License
