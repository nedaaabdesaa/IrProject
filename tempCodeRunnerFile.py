
from DocumentProcessor import TextProcessor,DocumentProcessor
from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app, resources={r"/search": {"origins": "*"}})

class QueryProcessor:
    def __init__(self):
        self.text_processor = TextProcessor()

    def preprocess_query(self, query):
        return self.text_processor.preprocess_text(query)

def load_qrel_file(qrel_path, is_json=True):
    if is_json:
        with open(qrel_path, 'r', encoding='utf-8') as file:
            qrels = [json.loads(line) for line in file]
    else:
        qrels = pd.read_csv(qrel_path, sep='\t', header=None)
    return qrels

def get_answers_for_query(processor, query, queries_df, qrels, is_json=True):
    query_id = None
    cleaned_query = processor.preprocess_query(query)
    for _, row in queries_df.iterrows():
        if processor.preprocess_query(row[1].strip().lower()) == cleaned_query:
            query_id = int(row[0])
            break

    if query_id is None:
        return []

    answers = []
    if is_json:
        for qrel in qrels:
            if qrel['qid'] == query_id:
                answers.extend(qrel['answer_pids'])
    else:
        for _, row in qrels.iterrows():
            if row[0] == query_id:
                answers.append(row[2])
    return answers

@app.route('/search', methods=['POST'])
def search():
    try:
        print("Received search request")
        data = request.json
        print(f"Received data: {data}")
        
        query = data.get('query')
        category = data.get('category')  # الحصول على الفئة من الطلب

        print(f"Extracted query: {query}")

        if not query:
            print({'error': 'Query parameter is missing'})
            return jsonify({'error': 'Query parameter is missing'}), 400
        else:
            dataset_path = 'C:/Users/hp/Dropbox/My PC (DESKTOP-UULDQBN)/Desktop/IR/lotte/lifestyle/dev/collection.tsv'
            queries_path = "C:/Users/hp/Dropbox/My PC (DESKTOP-UULDQBN)/Desktop/IR/lotte/lifestyle/dev/questions.forum.tsv"
            qrel_path = 'C:/Users/hp/Dropbox/My PC (DESKTOP-UULDQBN)/Desktop/IR/lotte/lifestyle/dev/qas.forum.jsonl'

            dataset = pd.read_csv(dataset_path, sep='\t', header=None)
            queries_df = pd.read_csv(queries_path, sep='\t', header=None)
            qrels = load_qrel_file(qrel_path)

            processor = QueryProcessor()

            # البحث عن الأجوبة المطابقة للكويري والفئة
            answer_ids = get_answers_for_query(processor, query, queries_df, qrels, category)
            
            if not answer_ids:
                return jsonify({'message': 'No answers found for the query'}), 404
            
            answers = dataset[dataset[0].isin(answer_ids)][1].tolist()
            
            # إرجاع النتائج كاستجابة JSON
            return jsonify({'answers': answers})
    except Exception as e:
        print({"message": "Search endpoint reached", "error": str(e)})
        return jsonify({"message": "Search endpoint reached", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)











#  from flask import Flask, request, jsonify, abort
# import pandas as pd
# from flask_cors import CORS
# from Evaluator import load_qrel_file, Evaluator
# from DocumentProcessor import DocumentProcessor
# from QueryProcessor import TextProcessor
# import pickle
# import glob
# import json
# import re

# app = Flask(__name__)
# CORS(app, resources={r"/search": {"origins": "*"}})

# class QueryProcessor:
#     def __init__(self):
#         self.text_processor = TextProcessor()

#     def preprocess_query(self, query):
#         return self.text_processor.preprocess_text(query)

# def load_qrel_file(qrel_path):
#     with open(qrel_path, 'r', encoding='utf-8') as file:
#         qrels = [json.loads(line) for line in file]
#     return qrels

# def get_answers_for_query(processor, query, queries_df, qrels):
#     query_id = None
#     cleaned_query = processor.preprocess_query(query)
#     for _, row in queries_df.iterrows():
#         if processor.preprocess_query(row[1].strip().lower()) == cleaned_query:
#             query_id = int(row[0])
#             break

#     if query_id is None:
#         return []

#     answers = []
#     for qrel in qrels:
#         if qrel['qid'] == query_id:
#             answers.extend(qrel['answer_pids'])
#     return answers

# @app.route('/search', methods=['POST'])
# def search():
#     try:
#         print("Received search request")
#         data_type = request.headers.get('Content-Type')

#         if 'application/json' in data_type:
#             data = request.json
#             query = data.get('query')
#             search_category = data.get('type')
#         else:
#             query = request.form.get('query')
#             search_category = request.form.get('type')

#         print(f"Extracted query: {query}")
#         print(f"Search category: {search_category}")

#         if search_category == 'type1':
#             dataset_path = 'C:/Users/hp/Dropbox/My PC (DESKTOP-UULDQBN)/Desktop/IR/lotte/lifestyle/dev/collection.tsv'
#             queries_path = "C:/Users/hp/Dropbox/My PC (DESKTOP-UULDQBN)/Desktop/IR/lotte/lifestyle/dev/questions.forum.tsv"
#             qrel_path = 'C:/Users/hp/Dropbox/My PC (DESKTOP-UULDQBN)/Desktop/IR/lotte/lifestyle/dev/qas.forum.jsonl'
#         elif search_category == 'type2':
#             dataset_path = 'C:/Users/hp/Desktop/IR/wikIR1k/documents.csv'
#             queries_path = "C:/Users/hp/Desktop/IR/wikIR1k/training/queries.csv"
#             qrel_path = 'C:/Users/hp/Desktop/IR/wikIR1k/training/qrels'
#         else:
#             return jsonify({'error': 'Invalid category specified'}), 400

#         dataset = pd.read_csv(dataset_path, sep='\t', header=None)
#         queries_df = pd.read_csv(queries_path, sep='\t', header=None)
#         qrels = load_qrel_file(qrel_path)

#         processor = QueryProcessor()

#         answer_ids = get_answers_for_query(processor, query, queries_df, qrels)
        
#         if not answer_ids:
#             return jsonify({'message': 'No answers found for the query'}), 404
        
#         answers = dataset[dataset[0].isin(answer_ids)][1].tolist()

#         if search_category == 'type1':
#             return jsonify({'answers': answers})
#         elif search_category == 'type2':
#             return '\n'.join(answers), 200, {'Content-Type': 'text/plain; charset=utf-8'}

#     except Exception as e:
#         print({"message": "Search endpoint reached", "error": str(e)})
#         return jsonify({"message": "Search endpoint reached", "error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True)
