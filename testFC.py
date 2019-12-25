import jieba
from wordcloud import WordCloud
import jieba
import jieba.analyse
import pymysql.cursors

#测试jieba分词

str="我们一起去看电影，好不好，我们一起看电影吧，电影院不远，吃点火锅。"
tongji = {}
# seg_list = jieba.cut(str, cut_all=False)
# print ("Default Mode:", "/ ".join(seg_list))  # 精确模式

jieba.set_dictionary('testFC.txt')
jieba.analyse.set_idf_path('testFC.txt')
tags = list(jieba.analyse.extract_tags(str, topK=200, withWeight=True))

try:
    # jieba.analyse.set_stop_words('你的停用词表路径')
    tags = jieba.analyse.extract_tags(str, topK=200, withWeight=True)
    for v, n in tags:
        # 权重是小数，为了凑整，乘了一万
        if u'' + v in tongji:
            tongji[u'' + v] = tongji[u'' + v] + int(n* 10000)
        else:
            tongji[u'' + v] = int(n * 10000)
finally:
    pass

print( tags)

#绘制词云图
wordcloud = WordCloud(font_path = "simfang.ttf",background_color = 'White').generate_from_frequencies(tongji)
import matplotlib.pyplot as plt
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()