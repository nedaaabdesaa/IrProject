import re
import pandas as pd
import pickle
from collections import defaultdict
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
import json
from Evaluator import load_qrel_file,Evaluator
from DocumentProcessor import DocumentProcessor
from QueryProcessor import QueryProcessor


def main():
    dataset_path = 'C:/Users/hp/Dropbox/My PC (DESKTOP-UULDQBN)/Desktop/IR/lotte/lifestyle/dev/collection.tsv'

    query_files = [
        "C:/Users/hp/Dropbox/My PC (DESKTOP-UULDQBN)/Desktop/IR/lotte/lifestyle/dev/questions.forum.tsv",
        "C:/Users/hp/Dropbox/My PC (DESKTOP-UULDQBN)/Desktop/IR/lotte/lifestyle/dev/questions.search.tsv"
    ]

    qrel_files = [
        'C:/Users/hp/Dropbox/My PC (DESKTOP-UULDQBN)/Desktop/IR/lotte/lifestyle/dev/qas.forum.jsonl',
        'C:/Users/hp/Dropbox/My PC (DESKTOP-UULDQBN)/Desktop/IR/lotte/lifestyle/dev/qas.search.jsonl'
    ]

    dataset = pd.read_csv(dataset_path, sep='\t', header=None,nrows=1000)

    # دمج ملفات الاستعلامات
    queries_df = pd.concat([pd.read_csv(query_file, sep='\t', header=None) for query_file in query_files])

    # دمج ملفات الإجابات الصحيحة
    qrels = {}
    for qrel_file in qrel_files:
        qrels.update(load_qrel_file(qrel_file))

    doc_processor = DocumentProcessor(dataset)
    doc_processor.save_model()
    
    query_processor = QueryProcessor(queries_df, doc_processor.vectorizer, doc_processor.tfidf_matrix, doc_processor.all_docs)
    queries_answers = query_processor.match_queries()

    evaluator = Evaluator(queries_answers, qrels)
    evaluation = evaluator.evaluate()

    for e in evaluation.items():
        print(e)

if __name__ == "__main__":
    main()
