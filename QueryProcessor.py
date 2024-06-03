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
from DocumentProcessor import TextProcessor,DocumentProcessor

class QueryProcessor:
    def __init__(self, queries_df, vectorizer, tfidf_matrix, all_docs):
        self.queries_df = queries_df
        self.text_processor = TextProcessor()
        self.vectorizer = vectorizer
        self.tfidf_matrix = tfidf_matrix
        self.all_docs = all_docs
        self.queries = {queries_df.iloc[index, 0]: self.preprocess_query(queries_df.iloc[index, 1]) for index in range(len(queries_df))}

    def preprocess_query(self, query):
        return self.text_processor.preprocess_text(query)

    def get_most_relevant(self, similarity_scores):
        similarity_threshold = 0.01
        doc_ids = self.all_docs.keys()
        document_ranking = dict(zip(doc_ids, similarity_scores.flatten()))
        filtered_documents = {key: value for key, value in document_ranking.items() if value >= similarity_threshold}
        sorted_docs = sorted(filtered_documents.items(), key=lambda item: item[1], reverse=True)
        return sorted_docs[:10]
    
    def match_query(self, query):
        query_tfidf_matrix = self.vectorizer.transform([query])
        cosine_sim_queries = cosine_similarity(query_tfidf_matrix, self.tfidf_matrix)
        return self.get_most_relevant(cosine_sim_queries)
    
    def match_queries(self):
        queries_answers = {}
        for query_id, query_text in self.queries.items():
            queries_answers[query_id] = self.match_query(query_text)
        return queries_answers


    