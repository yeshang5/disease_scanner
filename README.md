# 运行环境
python3 

### 爬虫
扫描医疗问答的爬虫文件为`scanner.py`，加入多线程后，爬虫隔一段时间效率会下降，甚至卡死，研究了半天也没什么好办法，所以又写了一个监控程序，也就是`monitor.py` ，它会每隔五秒钟看一下新增的数据，如果低于一定数量，就重启一次爬虫

### jieba

使用jieba并结合语料库实现分词及词频统计。

jieba 词频统计的函数是 `jieba.analyse.extract_tags` 

```python
jieba.analyse.set_idf_path('dic_for_idf.txt') #配置自定义字典
tags = jieba.analyse.extract_tags(content, topK=200, withWeight=True)
```

但这样出现的结果很混乱，因为虽然配置了词频的字典，但是分词的时候会产生许多字典之外的词，他们也有权重，而且这些通用词出现频率更高，会完全压制自定义字典里的词，导致做词频统计，统计到的都不是自定义字典中的

所以我接下来加了一行代码，也同时配置了 jieba 分词的字典

```python
jieba.set_dictionary('dic_for_use.txt') #配置自定义字典
jieba.analyse.set_idf_path('dic_for_idf.txt') #配置自定义字典
tags = jieba.analyse.extract_tags(content, topK=200, withWeight=True)
```

但还是不行，网上找了资料，发现 jieba 其实还有新词发现功能，需要关闭隐马尔科夫模型，虽然```jieba.cut```可以配置隐马尔科夫模型的开关，但我调用的```jieba.analyse.extract_tags```却并没有这个参数，因此我只能修改 jieba 的源码，手动把 隐马尔科夫模型（HMM）给关闭了，修改的地方在 jieba库目录/posseg/__init__.py，搜索HMM就能找到许多，都改成False即可

为了保险起见，在`\Lib\site-packages\jieba\analyse\tfidf.py` 词频分析核心文件中的103行插入以下语句进行判断
```python
 if w not in self.idf_freq:
                continue
```
这样一来就可以完全过滤掉自定义字典之外的词

### 语料库
项目中收集了部分医疗相关的语料词典，可自行根据需求更改查询sql及引用的语料库实现不同类别的信息分析统计。

我发现[搜狗的词库](https://pinyin.sogou.com/dict/cate/index/132/download/9)真的是个很不错的地方，有许多医疗相关的语料，不过要注意的是，下载下来不能直接使用，需要使用工具解码，这里推荐『深蓝词库转换』，使用非常方便
![深蓝词库](https://img.niucodata.com/slck.png)



