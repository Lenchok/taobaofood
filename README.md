selenium+chrome无头模式爬取淘宝宝贝信息

工具：selenium，chrome，mysql，pyquery

原理：淘宝网经过加密，通过抓包无法获得网页内容。都是经过js文件加载后才能正常获取网页内容，
因此使用selenium+chrome模拟浏览器行为，访问网页，获取源码，再用PyQuery解析出宝贝信息。

一、selenium的安装
1、首先在环境变量PATH中加上python跟谷歌浏览器的安装路径：
C:\Users\chao\AppData\Local\Programs\Python\Python36-32;#python安装路径
C:\Users\chao\AppData\Local\Programs\Python\Python36-32\Scripts;#python安装库路径
C:\Users\chao\AppData\Local\Google\Chrome\Application #谷歌浏览器路径
2、使用pip install selenium 安装selenium库
3、在百度搜索webdriver,找到对应python版本的版本下载，一样在环境变量PATH中加上路径

二、启动浏览器
1、添加启配置
from selenium import webdriver

#定义一个配置器
option=webdriver.ChromeOptions()
#由于我的谷歌浏览安装问题，需在属性加上‘--test-type --no-sandbox’配置才能打开，所以这样也需要添加。如何平常浏览器正常打开没问题请忽略这项
option.add_argument(r"--test-type --no-sandbox=C:\Users\chao\AppData\Local\Google\Chrome\User Data\Default")
#去掉浏览器地址栏显示‘软件正受自动测试软件控制’，可增加速度
option.add_argument('disable-infobars')
#添加无头模式，即无不显示页面运行，在调试阶段可先不添加，方便直观地看到效果
option.add_argument('headless')
#在启动浏览器的时候加入这些配置即可
driver=webdriver.Chrome(chrome_options=option)

三、PyQuery库的一些基础
当然这里使用BeautifullSoup去解析也是可以的，为了学习新知识，所以用了PyQuery库解析
PyQuery可以准确滴解析js层次的内容
一些常用的css选择器方法：


详细代码在taobaofood.py里。这里也可以使用PhantomJS代替chrome模式，但PhantomJS版本有点老旧，且解析网页的时候，有部门图片没解析成功，所以我还是用了谷歌浏览器无头模式，速度快，解析工程强大。