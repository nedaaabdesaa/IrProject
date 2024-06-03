import pickle
from sklearn.metrics.pairwise import cosine_similarity
from QueryProcessor2 import DocumentProcessor

class Evaluator:
    def __init__(self, queries_answers):
        self.queries_answers = queries_answers

    def load_qrel_file(self):
        file_path = 'C:/Users/user/Desktop/IR/wikIR1k/training/qrels'
        qrel_data = {}
        with open(file_path, 'r') as file:
            for line in file:
                query_id, _, doc_id, _ = line.strip().split()
                query_id = str(query_id)
                doc_id = str(doc_id)
                if query_id not in qrel_data:
                    qrel_data[query_id] = []
                qrel_data[query_id].append(doc_id)
        return qrel_data

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

    def compute_evaluation(self):
        qrels = self.load_qrel_file()
        over_all_average_precision = 0
        over_all_mrr = 0
        over_all_precision = 0
        over_all_recall = 0
        evaluation = {}
        for id, answers in self.queries_answers.items():
            precision = self.compute_precision(answers, qrels[str(id)], 10)
            over_all_precision += precision
            recall = self.compute_recall(answers, qrels[str(id)])
            over_all_recall += recall
            average_precision = self.average_precision(answers, qrels[str(id)], 10)
            over_all_average_precision += average_precision
            mrr = self.compute_mrr(answers, qrels[str(id)])
            over_all_mrr += mrr
            evaluation[str(id)] = {
                "precision": precision,
                "recall": recall,
                "mrr": mrr,
                "average_precision": average_precision
            }

        evaluation["over_all"] = {
            "precision": over_all_precision / len(self.queries_answers),
            "recall": over_all_recall / len(self.queries_answers),
            "mrr": over_all_mrr / len(self.queries_answers),
            "map": over_all_average_precision / len(self.queries_answers)
        }
        return evaluation