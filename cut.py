import json
import time
from wordcloud import WordCloud
import jieba
import jieba.analyse
import pymysql.cursors

#初始化开始时间，分词字典，词频统计字典
firsttime = time.time()

jieba.set_dictionary('dictionary/中医药大全.txt')  #分词字典
jieba.analyse.set_idf_path('dictionary/中医药大全.txt') #语料库字典
def check_state():
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             db='test',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    start = time.time()
    #此处SQL按需修改
    #sql = "select doctor_answer from fuck_ill where id>"+id+" order by ill_id asc limit 100000"
    sql = "select doctor_answer from fuck_ill"
    cursor.execute(sql)
    results = list(cursor.fetchall())
    end1 = time.time()
    es = end1 - start
    print('>>>>>>: 数据库第一步耗时：'+str(es)+'秒')
    start = time.time()
    #解决编码问题
    line = results.__str__()
    #line = line.decode('unicode_escape')
    #for循环效率很低，感兴趣的可以试试看为什么
    # for row in results:
    #     ill_detail = row['doctor_answer']
    #     line = line + ill_detail
    cursor.close()
    end1 = time.time()
    es = end1 - start
    print('>>>>>>: 数据库第二步耗时：' + str(es)+'秒')
    print('>>>>>>: 一共'+str(len(results))+'条数据')
    return line

statistic = {}   #统计的结果集
def analyse(content):
    try:
        # jieba.analyse.set_stop_words('你的停用词表路径')
        global statistic
        tags = jieba.analyse.extract_tags(content, topK=200, withWeight=True)
        for v, n in tags:
            # 权重是小数，为了凑整，乘了一万
            if u'' + v in statistic:
                statistic[u'' + v] = statistic[u'' + v] + int(n * 10000)
            else:
                statistic[u'' + v] = int(n * 10000)
    finally:
        pass

start = time.time()
content = check_state()
end = time.time()
escape = end - start
print('>>>>>>: 本次数据库读取时间：' + str(escape)+'秒')

start = time.time()
print('>>>>>>: 开始分析词频')
analyse(content)
end = time.time()
escape = end - start
print('\n>>>>>>: 词频分析完成')
print('>>>>>>: 本次词频分析耗时：' + str(escape)+'秒')

#打印结果
print(statistic)

#绘制词云图
wordcloud = WordCloud(font_path = "simfang.ttf",width=1920, height=1080,scale=1,background_color = 'White').generate_from_frequencies(statistic)
#保存图片
wordcloud.to_file('wordcloud.png')
import matplotlib.pyplot as plt
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
end = time.time()
escape = end - firsttime
print('>>>>>>: 总耗时：'+str(escape)+"秒")