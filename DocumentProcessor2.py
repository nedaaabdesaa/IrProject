import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer

class TextProcessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        self.stemmer = PorterStemmer()

    def cleaned_text(self, text):
        try:
            text = re.sub(r'\n', ' ', text)
            text = re.sub(r'\W', ' ', text)
            text = re.sub(r'\s+', ' ', text)
            return text
        except Exception as e:
            print(f"Error cleaning text: {e}")
            raise e

    def normalization_example(self, text):
        return text.lower()

    def stemming_example(self, text):
        try:
            words = word_tokenize(text)
            stemmed_words = [self.stemmer.stem(word) for word in words]
            return ' '.join(stemmed_words)
        except Exception as e:
            print(f"Error stemming text: {e}")
            raise e

    def lemmatization_example(self, text):
        try:
            words = word_tokenize(text)
            lemmatized_words = [self.lemmatizer.lemmatize(word) for word in words]
            return ' '.join(lemmatized_words)
        except Exception as e:
            print(f"Error lemmatizing text: {e}")
            raise e

    def remove_stopwords(self, text):
        try:
            words = word_tokenize(text)
            filtered_words = [word for word in words if word.lower() not in self.stop_words]
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
            text = self.cleaned_text(text)
            text = self.normalization_example(text)
            text = self.stemming_example(text)
            text = self.lemmatization_example(text)
            text = self.remove_stopwords(text)
            text = self.remove_punctuation(text)
            return text
        except Exception as e:
            print(f"Error processing text: {e}")
            return str(e)
