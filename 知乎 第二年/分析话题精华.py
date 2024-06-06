import bs4  # 网页解析，获取数据
import re  # 正则表达式。进行文字匹配

# import urllib.request  # 制定URL。获取网页数据
# import urllib.error

import sqlite3  # 进行SQLLite数据库操作

relink = re.compile('content="https://www.zhihu.com/question/(.*?)"')
rewenti = re.compile('target="_blank">(.*)</a>')
# <meta itemprop="name" content="如何练好中文说唱的freestyle？">

dbpath = "知乎生活、艺术、文化与活动话题精华问题.db"



def main():
    data = []
    html = open('生活、艺术、文化与活动 - 知乎.html', encoding='utf-8')
    soup = bs4.BeautifulSoup(html, "html.parser")
    init_db(dbpath)
    for popover in soup.select('div[itemprop="zhihu:question"]'):
        # print(popover)
        link = re.findall(relink, str(popover))[0]
        # print(link)
        wenti = re.findall(rewenti, str(popover))[0].replace('"', "'")  # replace替换文字 sqlite3.OperationalError: near "很人渣": syntax error
                                                                    # 猜测：文字添加数据库是需要加引号，与问题中的引号干扰
        # print(wenti)
        data = []
        data.append(link)
        data.append(wenti)
        print(data)
        savedatadb(data, dbpath)



    print("一共", len(soup.select('div[itemprop="zhihu:question"]')), "个问题")


def savedatadb(data, dbpath):
    # init_db(dbpath)
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()
    for index in range(len(data)):
        if index == 1:  # type(data(index)) != type(float)
            data[index] = '"' + data[index] + '"'  # 非数字插入数据库时需要有双引号或单引号
    sql = '''
        insert or ignore into zhihu(link,wenti) 
        values(%s)
        ''' % ",".join(data)            # 解决主键问题重复

    cur.execute(sql)  # 执行
    conn.commit()  # 提交

    cur.close()
    conn.close()



def init_db(dbpath):  # 创建数据库，初始化
    try:
        sql = '''
            create table zhihu
            (
            link integer primary key,
            wenti varchar

            )
        '''  # 创建数据表，autoincrement自增长
        conn = sqlite3.connect(dbpath)
        cursor = conn.cursor()  # 游标
        cursor.execute(sql)  # # 执行sql语句
        conn.commit()  # 提交操作
        conn.close()
    except:
        print('已经存在表')


if __name__ == "__main__":
    main()
    print("分析完毕")
