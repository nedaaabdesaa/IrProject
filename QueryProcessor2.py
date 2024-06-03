import pandas as pd
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from DocumentProcessor2 import TextProcessor

class DocumentProcessor:
    def __init__(self, dataset_path,nrows=None):
        self.dataset_path = dataset_path
        self.text_processor = TextProcessor()
        self.vectorizer = TfidfVectorizer(preprocessor=self.text_processor.preprocess_text)
        self.all_docs = {}
        self.tfidf_matrix = None
        self.nrows = nrows

    def load_documents(self):
        dataset = pd.read_csv(self.dataset_path,nrows=1000)
        dataset['id_right'] = dataset['id_right'].astype(str)
        dataset['text_right'] = dataset['text_right'].astype(str)
        self.all_docs = {dataset.iloc[index, 0]: dataset.iloc[index, 1] for index in range(len(dataset))}
        self.tfidf_matrix = self.vectorizer.fit_transform(list(self.all_docs.values()))

        with open("vectorizer.pkl", "wb") as file:
            pickle.dump(self.vectorizer, file)

        with open("tfidf_matrix.pkl", "wb") as file:
            pickle.dump(self.tfidf_matrix, file)

    def preprocess_query(self, query):
        return self.text_processor.preprocess_text(query)

    def match_query(self, query):
        query_tfidf_matrix = self.vectorizer.transform([query])
        cosine_sim_queries = cosine_similarity(query_tfidf_matrix, self.tfidf_matrix)
        return self.get_most_relative(cosine_sim_queries[0])

    def get_most_relative(self, similarity_scores):
        similarity_threshold = 0.02
        doc_ids = self.all_docs.keys()
        document_ranking = dict(zip(doc_ids, similarity_scores))
        filtered_documents = {key: value for key, value in document_ranking.items() if value >= similarity_threshold}
        sorted_dict = sorted(filtered_documents.items(), key=lambda item: item[1], reverse=True)
        return sorted_dict
