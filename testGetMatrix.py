# test getMatrix.py

import getMatrix as gm
import preprocess as pr
from dotenv import load_dotenv
import os

load_dotenv()

keywords_path = os.environ.get("keywords_path")
keywords_path2 = os.environ.get("keywords_path2")
company_names_path = os.environ.get("company_names_path")
matrix_save_path = os.environ.get("matrix_save_path")
cut_sentences_path = os.environ.get("cut_sentences_path")

def test_load_words():
    keywords = gm.load_words(keywords_path)
    company_names = gm.load_words(company_names_path)
    print("keywords:", keywords)
    print("company_names:", company_names)
    return

def test_init_matrix():
    keywords = gm.load_words(keywords_path)
    company_names = gm.load_words(company_names_path)
    matrix = gm.init_matrix(keywords, company_names)
    print(matrix)
    return

def test_count_co_occur():
    keywords = gm.load_words(keywords_path)
    company_names = gm.load_words(company_names_path)
    matrix = gm.init_matrix(keywords, company_names)
    corpus = pr.load_saved_preprocessed_corpus(cut_sentences_path)
    # corpus = pr.load_saved_preprocessed_corpus(cut_paragraphs_path)
    # testCorpus = ["还有 一些 保险公司 虽然 没有 对外 宣布 在 区块链 的 业务 进展 ， 但 也 保持 了 极大 关注 ， 比如 人保 财险 执行 副总裁 王 和 ， 曾 撰文 称 “ 区块 链 将 成为 保险 创新 新动力 ， 它 带来 的 不仅仅 是 新 技术 ， 更 有 基于 “ 底层 变革 ” 的 商业模式 创新 与 迭代 。 ”",
    #               "作为 财险 行业 的 老兵 ， 人保 财险 监事会 主席 王 和 指出 ， 保险科技 变革 最 核心 的 是 基于 新 技术创新 应用 的 商业模式 创新 ， 量子 理论 、 纳米技术 、 智能化 是 其三 大 支撑 。"]
    result = gm.count_co_occur(keywords, company_names, matrix, corpus, matrix_save_path)
    print(result)
    return result


# test_load_words()
# test_init_matrix()
# test_count_co_occur()