# get co-occurrence matrix of Insurtech keywords and company names

import os
from dotenv import load_dotenv
import re
import jieba
import pandas as pd

# load .env file
load_dotenv()

def load_doc(doc_folder_path:str=os.environ.get('doc_folder_path'))->list[str]:
    '''
    读取各年度文档
    返回一个列表，其中每一个元素表示一个年度内的所有文档

    folder_path: 所有txt文件所在文件夹
    '''
    # Get a list of text files in the folder and sort them by filename

    txt_files = sorted([f for f in os.listdir(doc_folder_path) if f.endswith(".txt")])
    
    docs_by_year = []
    for filename in txt_files:
        file_path = os.path.join(doc_folder_path, filename)

        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            docs_by_year.append(content)

    return docs_by_year



def load_uselessText(uselessText_path:str=os.environ.get("uselessText_path"))->list[str]:
    with open(uselessText_path, "r", encoding="utf-8") as f:
        whole = f.read()
        uselessText = whole.split("\n\n")
    return uselessText

def remove_nonsense(docs_by_year:list[str])->list[str]:
    '''remove useless text'''

    uselessText = load_uselessText()
    for i in range(len(docs_by_year)): # use list index to change value of list items
        for text in uselessText:
            docs_by_year[i] = docs_by_year[i].replace(text, "") # strings are immutable
    
    return docs_by_year

def remove_href(docs_by_year:list[str]):
    '''remove href link'''
    pat = "(文字快照：.*?\n)"
    for i in range(len(docs_by_year)):
        docs_by_year[i] = re.sub(pat, "", docs_by_year[i])
    return docs_by_year

def test_load_uselessText():
    uselessText = load_uselessText()
    for text in uselessText:
        print(text)
    return


def split_docs(docs_by_year:list[str], split_pattern:str=os.environ.get('split_pattern'))->list[str]:
    '''
    切分每个年度内的文档
    返回一个列表，其中每一个元素表示一篇文档

    split_pattern: 用于文档切分的pattern
    '''
    splitted_docs = []
    for docs in docs_by_year:
        doc_list = re.split(split_pattern, docs)
        doc_list = doc_list[:-1]    # remove the last part
        splitted_docs.extend(doc_list)

    return splitted_docs

def split_docs_by_year(docs_by_year:list[str], split_pattern:str=os.environ.get('split_pattern'))->list[list[str]]:
    '''
    切分每个年度内的文档
    返回一个列表，其中每一个元素为一个列表，表示一个年度内的所有文档

    split_pattern: 用于文档切分的pattern
    '''
    splittedDocsByYear = []
    for docs in docs_by_year:
        doc_list = re.split(split_pattern, docs)
        doc_list = doc_list[:-1]    # remove the last part
        splittedDocsByYear.append(doc_list)  # use append instead of extend
    return splittedDocsByYear



def split_into_sentences(splitted_docs:list[str])->list[str]:
    '''
    将文档切分为句子
    返回一个列表，其中每一个元素表示一个句子

    splitted_docs: 文档列表，一个元素代表一篇文档
    '''
    sentence_pattern = re.compile('([﹒﹔﹖﹗．；。！？]["’”」』]{0,2}|：(?=["‘“「『]{1,2}|$))')
    sentences = []
    for doc in splitted_docs:
        for i in sentence_pattern.split(doc):
            if sentence_pattern.match(i) and sentences:
                sentences[-1] += i
            elif i:
                sentences.append(i)

    return sentences


def test_split_into_sentences():
    input_text1 = '''过去十年，互联网对保险行业的影响不仅在互联网保险，对传统保险的销售和运营也有巨大的推进。例如，代理人的销售工具普遍已利用移动互联网；客户服务除了热线电话，也包含了线上客服；客户采用移动互联网APP等形式自助操作保单服务等。'''
    input_text2 = '''2021年10月，复旦大学许闲教授团队联合瑞士再保险发布了《中国保险科技发展报告》（以下简称“报告”）。报告梳理了自2010年以来，新闻媒体对保险科技与保险业务的报道数据，构建了中国保险科技整体发展指数及五大保险科技分项技术指数。通过梳理中国保险科技生态圈主要参与主体的发展策略，发现了保险科技生态圈主要参与者的业务发展策略各不相同，各类主体之间的合作和博弈关系显著分化。同时，根据复旦大学保险科技实验室团队研究，归纳出中国保险科技发展主要面临五个维度、十八项限制因素，并对目前保险科技发展面临的主要阻碍因素进行了梳理和量化分析，并对未来保险科技的发展方向进行了概括和总结。本报告全面评估了中国保险科技的发展状况和主要趋势、市场参与主体的科技转型战略，并与发达市场的发展状况进行对比。'''
    input_text3 = "美国马萨诸塞州的一家保险科技创业公司Insurify已经用人工智能替代了人类。他们发布的人工智能虚拟保险代理人Evia（Expert Virtual Insurance Agent，虚拟保险代理专家）可以通过一张车牌照片为你找到更好的汽车保险。"
    docs = [input_text1, input_text2, input_text3]
    output = split_into_sentences(docs)
    print(output)
    return output


def split_into_paragraphs(splitted_docs:list[str])->list[str]:
    '''将文档切分为段落'''

    para_list = []
    for doc in splitted_docs:
        paras = doc.split("\n\n")
        paras_drop_empty = list(filter(None, paras)) # drop empty strings from list
        para_list.extend(paras_drop_empty)
    return para_list

def extract_dict_from_excel(path:str=os.environ.get("comnpany_names_excel"), save_path=os.environ.get("dict_from_excel")):
    '''从Excel文件加载公司名，保存为jieba可以直接读取的plain text'''
    df = pd.read_excel(path, sheet_name="财险公司", usecols="B")
    names = df.values.tolist()
    names = [name[0].split(" ") for name in names]
    with open(save_path, "w", encoding="utf-8") as f:
        for company in names:
            for name in company:
                f.write(name + "\n")
    
    return



def cut(sentences:list[str], my_dict_path:str=os.environ.get('dict_from_excel'))->list[str]:
    '''
    将列表中的句子切分为词语，返回列表, 列表中每一个元素为一个分词后的句子

    my_dict_path: 自定义词典路径
    '''
    if my_dict_path:
        # 让jieba加载自定义词典
        jieba.load_userdict(my_dict_path)
    
    cut_sentences = []
    for sentence in sentences:
        tokens = [token for token in jieba.cut(sentence)]    # To-do: consider removing stopwords
        result = ' '.join(tokens)
        cut_sentences.append(result)
    return cut_sentences


def save_sentences(cut_sentences:list[str], cut_sentences_path=os.environ.get('cut_sentences_path')):
    '''
    Save the cut sentences, 1 sentence 1 line.
    '''
    try:
        with open(cut_sentences_path, "w", encoding='utf-8') as f:
            f.write("\n".join(cut_sentences)) # python's .writelines() does not add \n
    except:
        print(f"Error saving cut_sentences to {cut_sentences_path}")
    return

# not tested
def load_saved_preprocessed_corpus(path):
    '''加载保存的分词后的分段或者分句语料(a single txt file)，逐行读取到列表，去除单个换行符元素'''
    corpus = []
    with open(path, "r", encoding="utf-8") as f:
        corpus = f.readlines()
        corpus = list(filter(notNewlineCharacter, corpus))
    return corpus

def load_preprocessed_multi_corpus(folder_path=os.environ.get("cut_sentences_by_year_folder"))->list[list[str]]:
    corpusByYear = []
    txt_files = sorted([f for f in os.listdir(folder_path) if f.endswith(".txt")])

    for filename in txt_files:
        file_path = os.path.join(folder_path, filename)

        with open(file_path, "r", encoding="utf-8") as f:
            corpus = f.readlines()
            corpus = list(filter(notNewlineCharacter, corpus))
            corpusByYear.append(corpus)
    return corpusByYear

def getYearFromFilename(folder_path=os.environ.get("cut_sentences_by_year_folder"))->list[str]:
    '''return years of corpus list according to names of txt files'''
    filenames = sorted([f for f in os.listdir(folder_path) if f.endswith(".txt")])
    years = [filename[:4] for filename in filenames]
    return years

def notNewlineCharacter(line):
    if line == "\n":
        return False
    return True

# test_load_uselessText()
# slist = test_split_into_sentences()
# print(cut(slist))
# extract_dict_from_excel()