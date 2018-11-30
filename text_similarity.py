#encoding:utf-8
"""
要求，必须有输入，否则即不判断，直接返回不相似。
"""
import jieba
import jieba.analyse
import numpy as np

class SimHash(object):
    def __init__(self, content):
        self.simhash = self.get_simhash(content)

    def __str__(self):
        return str(self.simhash)

    def get_simhash(self, content):
        seg = jieba.cut(content)
        jieba.analyse.set_stop_words('./data/stopwords.txt')
        keyWord = jieba.analyse.extract_tags(
            '|'.join(seg), topK=20, withWeight=True, allowPOS=())  # 在这里对jieba的tfidf.py进行了修改
        # 将tags = sorted(freq.items(), key=itemgetter(1), reverse=True)修改成tags = sorted(freq.items(), key=itemgetter(1,0), reverse=True)
        # 即先按照权重排序，再按照词排序
        keyList = []
        for feature, weight in keyWord:
            weight = int(weight * 20)
            feature = self.string_hash(feature)
            temp = []
            for i in feature:
                if (i == '1'):
                    temp.append(weight)
                else:
                    temp.append(-weight)
            # print(temp)
            keyList.append(temp)
        list1 = np.sum(np.array(keyList), axis=0)
        if (keyList == []):  # 编码读不出来
            return '00'
        simhash = ''
        for i in list1:
            if (i > 0):
                simhash = simhash + '1'
            else:
                simhash = simhash + '0'
        return simhash

    def string_hash(self, source):
        if source == "":
            return 0
        else:
            x = ord(source[0]) << 7
            m = 1000003
            mask = 2 ** 128 - 1
            for c in source:
                x = ((x * m) ^ ord(c)) & mask
            x ^= len(source)
            if x == -1:
                x = -2
            x = bin(x).replace('0b', '').zfill(64)[-64:]
            return str(x)

    def hammingDis(self, com):
        t1 = '0b' + self.simhash
        t2 = '0b' + com.simhash
        n = int(t1, 2) ^ int(t2, 2)
        i = 0
        while n:
            n &= (n - 1)
            i += 1
        return i

    def similarity(self, other_hash):
        a = float(self.simhash)
        b = float(other_hash.simhash)
        if a > b: return b / a
        return a / b







if __name__ == '__main__':
    h1 = SimHash('av在线视频 欧美av 亚洲av 东方av av天堂 成人av 日本av av女优 日韩av 国产av')
    h2 = SimHash('不经常做爱逼很粉嫩连续爆操2次,侧面108高清版')

    print h1.hammingDis(h2)
    print h1.similarity(h2)