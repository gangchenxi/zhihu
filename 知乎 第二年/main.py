import bs4  # 网页解析，获取数据
import re  # 正则表达式。进行文字匹配

import urllib.request  # 制定URL。获取网页数据
import urllib.error
# import xlwt  # 进行excel操作
import sqlite3  # 进行SQLLite数据库操作
import time  # time.sleep(3)  设置等待时间3秒

cuowu = 0  # 返回错误类型

# 正则表达
# 问题自带话题
rehuati = re.compile('<meta content="(.*?)".*"/>')
# 题目
rewenti = re.compile('title">(.*)</h1>')  # <h1 class="QuestionHeader-title">马斯克称「人类如果不多生孩子，文明将会崩溃」，如何看待其言论？</h1>
# 浏览量和阅读量
reliang = re.compile('title="(.*?)"')  # <strong class="NumberBoard-itemValue" title="2388505">2388505</strong>
# 回答数量
rehuida = re.compile('<span>(.*)<!-- --> 个回答')  # <h4 class="List-headerText"><span>1,238 <!-- --> 个回答</span></h4>


def main():
    badeurl = "https://www.zhihu.com/question/"
    dbpath = "测试产业.db"               # 保存数据库文件名
    init_db(dbpath)

    # 1查询数据
    conn = sqlite3.connect("知乎产业话题精华问题.db ")  # 打开或创建数据库文件 初步提取精华文件链接
    print("成功打开数据库")
    c = conn.cursor()  # 获取游标
    sql = "select link from zhihu"

    cursor = c.execute(sql)  # 执行sql语句
    for row in cursor:
        print("id = ", row[0], "\n")
        urlnumb = row[0]
        # 1.爬取网页
        getDate(badeurl, urlnumb, dbpath)
        # print(datalist)
        # 保存数据
        # savedatadb(datalist, dbpath)


    conn.close()  # 关闭数据库连接
    print("查询完毕")




def getDate(baseurl, urlnumb, dbpath):

    # for i in range(0, 100000):  # 调用获取页面信息的函数次数

    url = baseurl + str(urlnumb)
    html = askurl(url)  # 保存获取到的网页源码
    # 2.逐一解析数据
    soup = bs4.BeautifulSoup(html, "html.parser")  # 解析器，在内存形成树形结构的对象  html.parser是使用python标准库进行解析   还能用lxml解析

    if cuowu != 404 and cuowu != 410:  # 判断页面是否为404
        # 问题
        for popover in soup.select("h1[class='QuestionHeader-title']"):
            data = []  # 保存一个问题的所有信息
            # 先保存链接id
            data.append(str(urlnumb))

            wenti = re.findall(rewenti, str(popover))[0].replace('"', "'")       # findall返回列表    猜测：文字添加数据库是需要加引号，与问题中的引号干扰
            # print(wenti)                                                 # sqlite3.OperationalError: near "很人渣": syntax error
            data.append(wenti)

        # 话题
        for popover in soup.select("meta[name='keywords']"):
            # print(popover)                       # 测试
            huati = re.findall(rehuati, str(popover))[0]  # re.findall()第二个参数需要字符串类型
            # print(huati)
            data.append(huati)
            # print(data)

        # 关注量、浏览量
        popover = soup.select('strong[class="NumberBoard-itemValue"]')
        for q in range(2):
            # print(popover[q])
            liang = re.findall(reliang, str(popover[q]))[0]
            # print(liang)
            data.append(liang)  # 第一个是关注量，第二个是被浏览量

        # 回答数量
        for popover in soup.select('h4[class="List-headerText"]'):
            popover = str(popover)
            # print(popover)
            huida = re.findall(rehuida, str(popover))[0].replace(",", "")  # replace替换文字
            # print((huida))
            data.append(huida)

    elif cuowu == 410:
        print("410该内容以删除")
        data = [str(urlnumb)]

    else:
        print("404链接无内容")
        data = [str(urlnumb)]
        # for a in range(5):
        #     data.append()

    print(data)
    savedatadb(data, dbpath)
    time.sleep(3)


# 得到指定一个URL的网页内容
def askurl(url):
    head = {  # 模拟浏览器头部信息，向豆瓣服务器发送消息 主意User-Agent中间不能有空格
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
    }
    # 用户代理，表示告诉服务去，我们是什么类型的机器、浏览器（本质上是告诉服务器，我们可以接受什么类型的文件内容。）
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            global cuowu  # 修改全局变量
            cuowu = e.code
            print(e.code)  # 把e中的错误类型打印
        if hasattr(e, "reason"):
            print(e.reason)  # e.code是错权误代码，e.reason获取的是错误的原因

    return html


def savedatadb(data, dbpath):
    # print("save.....")
    # init_db(dbpath)
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()

    if len(data) == 6:
        for index in range(len(data)):
            if index == 1 or index == 2:  # type(data(index)) != type(float)
                data[index] = '"' + data[index] + '"'  # 非数字插入数据库时需要有双引号或单引号

        sql = '''
                insert into zhihu(
                link,wenti,huati,guanzhu,liulan,huida)
                values(%s)
            ''' % ",".join(data)  # 把列表元素用逗号分割，组成字符串。%是把后面填到%s位置.join链接
        # connection.execute("INSERT INTO UTILISATEURS (FULLNAME, EMAIL, CIN, ADDRESS, PHONE, RIB) VALUES (?,?,?,?,?,?) ", (str(fullname), str(email), str(cin), str(address), str(phonenumber), str(ribnumber)))

    elif len(data) == 5:  # 没有回答的情况
        for index in range(len(data)):
            if index == 1 or index == 2:  # type(data(index)) != type(float)
                data[index] = '"' + data[index] + '"'  # 非数字插入数据库时需要有双引号或单引号
        sql = '''
        insert into zhihu(
                link,wenti,huati,guanzhu,liulan,huida)
                values(%s,NULL)
        ''' % ",".join(data)

    else:                # 空链接
        sql = '''
        insert into zhihu(link,wenti,huati,guanzhu,liulan,huida)
        values(%s,NULL,NULL,NULL,NULL,NULL)
        ''' % data[0]
    # print(sql)
    cur.execute(sql)  # 执行
    conn.commit()  # 提交

    cur.close()
    conn.close()


def init_db(dbpath):  # 创建数据库，初始化
    try:
        sql = '''
            create table zhihu
            (
            id integer primary key autoincrement,
            link int,
            wenti varchar,
            huati varchar,
            guanzhu int,
            liulan int,
            huida int
            
            )
        '''  # 创建数据表，autoincrement自增长
        conn = sqlite3.connect(dbpath)  # 如果存在就链接，不存在就创建
        cursor = conn.cursor()  # 游标
        cursor.execute(sql)  # # 执行sql语句
        conn.commit()  # 提交操作
        conn.close()
    except:
        print('已经存在表')


if __name__ == "__main__":
    main()
    print("爬取完毕")
