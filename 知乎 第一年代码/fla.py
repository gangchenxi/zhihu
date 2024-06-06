from flask import Flask, render_template
import sqlite3



app = Flask(__name__)


# 路由解析，通过用户访问的路径，匹配相应的函数
@app.route('/')
def home():
    return render_template("index.html")



@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/movie')
def movie():
    return render_template("movie.html")


# 展示数据
@app.route('/chaxun/<name>')         # 通过访问路径，获取用户的字符串参数
def movies(name):
    datalist = []
    names = name + '.db'
    con = sqlite3.connect(names)
    cur = con.cursor()
    sql = "select * from zhihu"
    data = cur.execute(sql)
    for item in data:
        datalist.append(item)
    cur.close()
    con.close()
    name = name.replace("已获取知乎", "")
    return render_template("chaxun.html",  movies=datalist, name=name)


# 图表
@app.route('/score')
def score():

    return render_template("score.html")


# echarts图表
@app.route('/score/<name>')         # 通过访问路径，获取用户的字符串参数
def scores(name):
    datalist = []
    names = name + '.db'
    con = sqlite3.connect(names)
    cur = con.cursor()
    sql = "select * from zhihu"
    data = cur.execute(sql)
    for item in data:
        datalist.append(item)
    cur.close()
    con.close()
    name = name.replace("已获取知乎", "")
    huidaliulan = []
    for list in datalist:
        lis = []
        lis.append(int(str(list[6]).replace("None", "0")))     # 部分数据回答量为None  不适用数值转换会报 'int' object has no attribute 'replace'
        lis.append(list[5])
        huidaliulan.append(lis)
    print(huidaliulan)

    return render_template("tubiao.html", data=huidaliulan, name=name)


@app.route('/score/quanbu')         # 通过访问路径，获取用户的字符串参数
def scoress():
    datalist = []
    huidaliulan = []
    nam = ['已获取知乎根话题精华问题', '已获取知乎「未归类」话题精华问题', '已获取知乎学科话题精华问题', '已获取知乎实体话题精华问题', '已获取知乎「形而上」话题精华问题', '已获取知乎产业话题精华问题', '已获取知乎生活、艺术、文化与活动话题精华问题']
    for name in nam:
        names = name + '.db'
        con = sqlite3.connect(names)
        cur = con.cursor()
        sql = "select * from zhihu"
        data = cur.execute(sql)
        for item in data:
            datalist.append(item)
        cur.close()
        con.close()
        for list in datalist:
            lis = []
            lis.append(int(str(list[6]).replace("None", "0")))     # 部分数据回答量为None  不适用数值转换会报 'int' object has no attribute 'replace'
            lis.append(list[5])
            huidaliulan.append(lis)

    name = '全部'

    return render_template("tubiao.html", data=huidaliulan, name=name)





@app.route('/word')
def word():
    return render_template("word.html")


@app.route('/team')
def team():
    return render_template("team.html")








if __name__ == '__main__':
    app.run(debug=True)
