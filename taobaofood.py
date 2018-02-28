from selenium import webdriver
from selenium.webdriver.common.by import By #用来选择元素类型，css_selector\Xpath
from selenium.webdriver.support.ui import WebDriverWait #等待元素位置选取
from selenium.webdriver.support import expected_conditions as EC #定位元素位置
import re
from selenium.common.exceptions import TimeoutException
from pyquery import PyQuery as pq
import pymysql

#添加启动项配置
option=webdriver.ChromeOptions()
#我的chrome启动项里加了--test-type --no-sandbox才能正常访问网页，右键查看属性
option.add_argument(r"--test-type --no-sandbox=C:\Users\chao\AppData\Local\Google\Chrome\User Data\Default")
#去掉浏览器正受到自动测试软件的控制
option.add_argument('disable-infobars')
#使用无头模式浏览器
option.add_argument('headless')
#按照配置打开浏览器
driver=webdriver.Chrome(chrome_options=option)
#访问淘宝首页
driver.get('https://www.taobao.com/')
#等待浏览器加载
wait=WebDriverWait(driver, 10)

def get_ona_page(keyword):
    print('正在搜索')
    try:
        # 选取输入框并等待加载完成
        input = wait.until( EC.presence_of_element_located((By.CSS_SELECTOR, "#q")))
        # 选取搜索按钮并等待加载
        sumbit=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#J_TSearchForm > div.search-button > button')))
        input.send_keys(keyword) #传入值
        sumbit.click() #点击按钮
        # 等待总页数加载出来并获取其内容
        sum_page=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.total')))
        #解析页面内容
        parser_one_page(keyword)
        return sum_page.text
    except TimeoutException :#加载超时异常，重新执行
        return get_ona_page(keyword)

def netx_page(i,keyword):
        print('正在翻页', i)
        try:
            page_input=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.form > input')))#获取页码输入框
            page_sumbit=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))#获取点击确定按钮
            page_input.clear()
            page_input.send_keys(i)
            page_sumbit.click()
            #判断页面是否加载成功
            wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > ul > li.item.active > span'),str(i)))#判断加载的页面的 页码是否与输入的一致，一致则成功加载
            parser_one_page(keyword)
        except TimeoutException:
            netx_page(i,keyword)

#解析网页
def parser_one_page(keyword):
    #判断'#mainsrp-itemlist .items .item'标签的内容加载完成
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-itemlist .items .item')))
    #返回网页源码
    html=driver.page_source
    #初始化页面
    doc=pq(html)
    #查找‘mainsrp-itemlist’标签下的‘items’标签下的‘item’标签/.items()是获取其内容
    items=doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        data={
            'img':item.find('.pic .img').attr('src'),#获取标签属性时用attr（）
            'title': item.find('.title').text(),#获取标签内容时用text（）
            'price': item.find('.price').text(),
            'shop': item.find('.shop').text(),
            'deal': item.find('.deal-cnt').text()[:-3],
            'location': item.find('.location').text()
        }
        # print(data)
        try:
            write_to_database(data,keyword)
            print('存储到数据库成功！')
        except TimeoutException:
            print('存储到数据库失败！正在重新存储到数据库')
            write_to_database(data,keyword)
            print('存储到数据库成功！')

#存入数据库
def write_to_database(data,keyword):
    #创建数据库连接
    conn=pymysql.connect(host='127.0.0.1', user='root', password='root', db='taobao', port=3306, charset='utf8')
    #创建游标
    curser=conn.cursor()
    sql = 'insert into  taobao values (%s,%s,%s,%s,%s,%s,%s)' % (
    "'" + data['img'] + "'", "'" + data['title'] + "'", "'" + data['price'] + "'", "'" + data['shop'] + "'","'" + data['deal'] + "'", "'" + data['location'] + "'", "'"+keyword+"'")
    #执行sql语句
    curser.execute(sql)
    #提交
    conn.commit()
    #关闭
    curser.close()
    conn.close()


def main():
    keyword=input('请输入需要搜索的宝贝关键字：')
    #获取总页码
    totle=get_ona_page(keyword)
    #提取出数值
    page=int(re.compile('(\d+)').search(totle).group(1))
    for i in range(2,page+1):
        netx_page(i,keyword)

    #关闭浏览器
    driver.close()


if __name__=='__main__':
    main()