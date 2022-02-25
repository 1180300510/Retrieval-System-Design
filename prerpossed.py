import json
from re import A
import jieba
import math
from sklearn.feature_extraction.text import TfidfVectorizer

class Pocessed():
    def readtext(self,filename):#读取JSON文件，文章内容和编号
        try:
            with open(filename,'r',encoding='utf-8') as file:
                data=[]
                for line in file.readlines():
                    data.append(line)
                return data
        except:
            print("文件读取失败")
            return None

    def LoadStopWords(self,filepath):#加载停用词表
        WordsList=[]
        with open(filepath,'r',encoding='utf-8') as file:
            for line in file.readlines():
                line=line.strip('\n')
                WordsList.append(line)
        return WordsList

    #对每一个句子进行分词，去除停用词
    def segmentWords(self,sentence):
        WordsList=self.LoadStopWords('./stopwords(new).txt')
        sentence=''.join(sentence.split())#去除空格
        seg_words=[x for x in jieba.cut(sentence)]#使用jieba库分词精确模式，得到单词列表
        seg_words=list(filter(lambda x: x not in WordsList,seg_words))
        return seg_words

    #统计词频和单词出现的文章数目
    def cal_nums(self,all_list,df,tf):
        for i in range(len(all_list)):
            words_list=all_list[i]
            for word in words_list:
                if word not in tf.keys():#该单词第一次出现
                    tf.setdefault(word,{i:1})
                    if word not in df.keys():
                        df.setdefault(word,1)
                    else:
                        df[word]+=1
                else:
                    if i not in tf[word].keys():#该文章该单词第一次出现
                        tf[word].setdefault(i,1)
                        df[word]+=1
                    else:
                        tf[word][i]+=1
    

    #计算df_idf的值,N为文档的数量
    def cal_dfidf(self,matric_weight,tf,df,N):
        for word in tf.keys():
            idf_value=math.log10(N/df[word])
            for article in tf[word].keys():
                tf_value=(1+math.log10(tf[word][article]))
                tf_idf=idf_value*tf_value
                if tf_idf==0.0:#由于权重矩阵非常稀疏，为保证存储效率，对于权重为0的不进行存储
                    continue
                if word not in matric_weight.keys():
                    matric_weight.setdefault(word,{article:tf_idf})
                else:
                    matric_weight[word].setdefault(article,tf_idf)


    def write_dfidf(self,filename,matric_weight):
    
        with open(filename,'w',encoding='utf-8') as file:
            for word in matric_weight.keys():
                file.write(str(word)+':')
                for i in matric_weight[word].keys():
                    file.write(str(i)+','+str(matric_weight[word][i])+' ')
                file.write('\n')
    

    def generate_index(self):
        data=self.readtext('./data/passages_multi_sentences.json')
        text_dict=[]
        matric_weight={}#权重矩阵：记录一个词在每一篇文章中出现的TF-IDF值
        tf={}#单词在每篇文章中的词频，value为一个字典，每一个元素的value为一个对应pid的词频，如果该单词未在该文章中出现，不记录，查询时默认为0
        df={}#单词出现的文章数目
        for i in range(len(data)):
            temp=json.loads(data[i])
            text_dict.append(temp['document'])
        N=len(text_dict)
        #将句子分词
        all_list=[]#列表中每一个元素是每篇文章的句子
        for i in range(len(text_dict)):
            word_list=[]
            for j in range(len(text_dict[i])):
                sentence=text_dict[i][j]
                word_list.extend(self.segmentWords(sentence))
            all_list.append(word_list)
    
        self.cal_nums(all_list,df,tf)
    

    
        self.cal_dfidf(matric_weight,tf,df,N)
        self.write_dfidf('./prerpocessed/tf_idf.txt',matric_weight)
    
    def read_indexfile(self,filename):
        tf_idf={}
        try:
            with open(filename,'r',encoding='utf-8') as file:
                for line in file.readlines():
                    line=line.strip()
                    line=line.split(':')
                    tf_idf.setdefault(line[0],{})
                    index=line[1].split()
                    for i in range(len(index)):
                        temp=index[i].split(',')
                        tf_idf[line[0]].setdefault(int(temp[0]),float(temp[1]))
            return tf_idf
        except:
            print("文件读取失败")
            return None
    #查询与问题最相关问题
    def search_first(self,tf_idf,sentence):
        words_list=self.segmentWords(sentence)
        score=[]#记录每一篇文章和该问题的相似程度
        for i in range(17469):
            temp_score=0
            for word in words_list:
                if word not in tf_idf.keys():#分出来的词没有在文章中出现
                    continue
                if i not in tf_idf[word].keys():
                    continue
                else:
                    temp_score+=tf_idf[word][i]
            score.append(temp_score)
        first_value=-1
        first_index=0
        for i in range(len(score)):
            if first_value<score[i]:
                first_value=score[i]
                first_index=i
        return first_index
    #查询与问题最相关的前三个问题
    def search_article(self,tf_idf,sentence):
        words_list=self.segmentWords(sentence)
        score=[]#记录每一篇文章和该问题的相似程度
        for i in range(17469):
            temp_score=0
            for word in words_list:
                if word not in tf_idf.keys():#分出来的词没有在文章中出现
                    continue
                if i not in tf_idf[word].keys():
                    continue
                else:
                    temp_score+=tf_idf[word][i]
            score.append(temp_score)
        first_value=-1
        first_index=0
        for i in range(len(score)):
            if first_value<score[i]:
                first_value=score[i]
                first_index=i
        second_value=-1
        second_index=0
        for i in range(len(score)):
            if second_value<score[i] and i!=first_index:
                second_value=score[i]
                second_index=i
        third_value=-1
        third_index=0
        for i in range(len(score)):
            if third_value<score[i] and i!=first_index and i!=second_index:
                third_value=score[i]
                third_index=i
        return [first_index,second_index,third_index]
    
    def get_trainfile(self,filename):
        train_line=self.readtext(filename)
        train_data=[]
        for line in train_line:
            temp=json.loads(line)
            train_data.append([temp['question'],temp['pid']])
        return train_data


if __name__=='__main__':
    pocessed=Pocessed()
    tf_idf=pocessed.read_indexfile('./prerpocessed/tf_idf.txt')#读取tf_idf，数据结构为字典，key为单词，value为一个字典，所在的文章编号和tf_idf值
    train_data=pocessed.get_trainfile('./data/train.json')
    
    predicted_article=[]
    for i in range(len(train_data)):
        question=train_data[i][0]
        predicted_article.append(pocessed.search_article(tf_idf,question))
    match_num_top1=0
    match_num_top3=0
    for i in range(len(predicted_article)):
        if train_data[i][1]==predicted_article[i][0]:
            match_num_top1+=1
            match_num_top3+=1
        elif train_data[i][1]==predicted_article[i][1] or train_data[i][1]==predicted_article[i][2]:
            match_num_top3+=1
    top1=match_num_top1/len(predicted_article)
    top3=match_num_top3/len(predicted_article)
    print(top1)
    print(top3)
    