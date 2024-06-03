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

# ('overall', {'precision': 0.1042957042957029, 'recall': 0.3184499316380594, 'mrr': 0.3650583543440685, 'map': 0.33714405909346373}

print('hiiiiiiiiiiiiiii')
print('hiiiiiiiiiiiiiii')

class TextProcessor:
    def __init__(self):
        pass

    def cleaned_text(self, text):
        try:
            cleaned_text = re.sub(r'\n', ' ', text)
            cleaned_text = re.sub(r'\W', ' ', cleaned_text)
            cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
            return cleaned_text
        except Exception as e:
            print(f"Error cleaning text: {e}")
            raise e

    def normalization_example(self, text):
        return text.lower()

    def stemming_example(self, text):
        try:
            words = word_tokenize(text)
            stemmed_words = [PorterStemmer().stem(word) for word in words]
            return ' '.join(stemmed_words)
        except Exception as e:
            print(f"Error stemming text: {e}")
            raise e

    def lemmatization_example(self, text):
        try:
            words = word_tokenize(text)
            lemmatized_words = [WordNetLemmatizer().lemmatize(word) for word in words]
            return ' '.join(lemmatized_words)
        except Exception as e:
            print(f"Error lemmatizing text: {e}")
            raise e

    def remove_stopwords(self, text):
        try:
            stop_words = set(stopwords.words('english'))
            words = word_tokenize(text)
            filtered_words = [word for word in words if word.lower() not in stop_words]
            return ' '.join(filtered_words)
        except Exception as e:
            print(f"Error removing stopwords: {e}")
            raise e

    def remove_punctuation(self, text):
        try:
            return re.sub(r'[^\w\s]', '', text)
        except Exception as e:
            print(f"Error removing punctuation: {e}")
            raise e

    def preprocess_text(self, text):
        try:
            processed_text = self.cleaned_text(text)
            processed_text = self.normalization_example(processed_text)
            processed_text = self.stemming_example(processed_text)
            processed_text = self.lemmatization_example(processed_text)
            processed_text = self.remove_stopwords(processed_text)
            processed_text = self.remove_punctuation(processed_text)
            return processed_text
        except Exception as e:
            print(f"Error processing text: {e}")
            return str(e)

class DocumentProcessor:
    def __init__(self, dataset):
        self.dataset = dataset
        self.text_processor = TextProcessor()
        self.vectorizer = TfidfVectorizer(preprocessor=self.text_processor.preprocess_text,
                                          min_df=2,
                                          use_idf=True,
                                          smooth_idf=True)
        self.all_docs = self.process_documents()
        self.tfidf_matrix = self.vectorizer.fit_transform(list(self.all_docs.values()))
        
    def process_documents(self):
        all_docs = {}
        for index in range(len(self.dataset)):
            doc_id = self.dataset.iloc[index, 0]
            doc_text = self.dataset.iloc[index, 1]
            if pd.isna(doc_text):
                continue
            processed_text = self.text_processor.preprocess_text(doc_text)
            all_docs[doc_id] = processed_text
        return all_docs
    
    def save_model(self):
        with open("vectorizer.pkl", "wb") as file:
            pickle.dump(self.vectorizer, file)
        with open("tfidf_matrix.pkl", "wb") as file:
            pickle.dump(self.tfidf_matrix, file)