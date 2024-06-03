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


class Evaluator:
    def __init__(self, queries_answers, qrels):
        self.queries_answers = queries_answers
        self.qrels = qrels

    def compute_precision(self, answers, right_answers, k=10):
        count = 0
        for answer in answers[:k]:
            if answer[0] in right_answers:
               count += 1 
        return count / k

    def compute_recall(self, answers, right_answers):
        count = 0
        for answer in answers:
            if answer[0] in right_answers:
                count += 1
                if count == len(right_answers):
                    break
        return count / len(right_answers)

    def average_precision(self, answers, right_answers, k=10):
        relevant_positions = [i for i, doc in enumerate(answers[:k]) if doc[0] in right_answers]
        if not relevant_positions:
            return 0.0
        precisions = [(i + 1) / (pos + 1) for i, pos in enumerate(relevant_positions)]
        return sum(precisions) / len(relevant_positions)

    def compute_mrr(self, answers, right_answers):
        for i, answer in enumerate(answers):
            if answer[0] in right_answers:
                return 1.0 / (i + 1)
        return 0.0

    def evaluate(self):
        overall_precision = 0
        overall_recall = 0
        overall_avg_precision = 0
        overall_mrr = 0
        evaluation = {}
        
        for id, answers in self.queries_answers.items():
            precision = self.compute_precision(answers, self.qrels[str(id)], 10)
            overall_precision += precision
            recall = self.compute_recall(answers, self.qrels[str(id)])
            overall_recall += recall
            avg_precision = self.average_precision(answers, self.qrels[str(id)], 10)
            overall_avg_precision += avg_precision
            mrr = self.compute_mrr(answers, self.qrels[str(id)])
            overall_mrr += mrr
            evaluation[str(id)] = {
                "precision": precision,
                "recall": recall,
                "mrr": mrr,
                "average_precision": avg_precision
            }
        
        evaluation["overall"] = {
            "precision": overall_precision / len(self.queries_answers),
            "recall": overall_recall / len(self.queries_answers),
            "mrr": overall_mrr / len(self.queries_answers),
            "map": overall_avg_precision / len(self.queries_answers)
        }
        
        return evaluation


def load_qrel_file(filepath):
    qrel_data = {}
    with open(filepath, 'r', encoding='latin1') as file:
        for line in file:
            data = json.loads(line.strip())
            query_id = str(data['qid'])  # Convert query_id to string if necessary
            answer_pids = data['answer_pids']  # List of document IDs

            if query_id not in qrel_data:
                qrel_data[query_id] = answer_pids
            else:
                qrel_data[query_id].extend(answer_pids)

    return qrel_data