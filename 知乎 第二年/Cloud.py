from wordcloud import WordCloud
import jieba
from matplotlib import pyplot as plt                # Matplotlib 是一个综合库，用于在 Python 中创建静态、动画和交互式可视化。
from PIL import Image                               # 图像处理
import numpy as np                                   # 矩阵运算
import sqlite3



# 准备词云所需的词
con = sqlite3.connect("已获取知乎产业话题精华问题.db")
cur = con.cursor()
sql = 'select wenti from zhihu'
data = cur.execute(sql)
text = ""
for item in data:
    text = text + item[0]
    # print(item[0])
print(text)
cur.close()
con.close()


cut = jieba.cut(text, use_paddle=True)         # 返回对象<generator object Tokenizer.cut at 0x000001D7E5169200>
string = ' '.join(cut)
# print(string)


# 创建停用词
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords


# 去除停用词
def seg_sentence(sentence):
    sentence_seged = jieba.cut(sentence.strip())
    stopwords = stopwordslist('cn_stopwords.txt')  # 这里加载停用词的路径
    outstr = ''
    for word in sentence_seged:
        if word not in stopwords:
            if word != '\t':
                outstr += word
                # outstr += " "
    return outstr


string = seg_sentence(string)
print(string)
print(len(string))



img = Image.open(r'./static/assets/img/tree.jpg')         # r  转义字符  背景图路径
ing_array = np.array(img)                                # 将图片转换成数组
wc = WordCloud(
    scale=16,
    background_color="white",
    mask=ing_array,
    font_path="STXINWEI.TTF"                          # C:\Windows\Fonts    字体
)
wc.generate_from_text(string)



# 绘制图片
fig = plt.figure(1)
plt.imshow(wc)
plt.axis('off')             # 是否显示坐标轴
# plt.show()                  # 显示生成的词云图片
# 输出词云图片到文件
plt.savefig(r'./static/assets/img/答辩测试.jpg', dpi=800)






