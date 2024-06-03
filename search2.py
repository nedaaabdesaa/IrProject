from QueryProcessor import DocumentProcessor
from DocumentProcessor import TextProcessor
from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS
import json
from werkzeug.datastructures import CombinedMultiDict

app = Flask(__name__)
CORS(app, resources={r"/search": {"origins": "*"}, r"/search2": {"origins": "*"}})


class DocumentProcessor:
    def __init__(self):
       self.text_processor = TextProcessor()

    def preprocess_query(self, query):
        return self.text_processor.preprocess_text(query)


def load_qrel_file(qrel_path, is_json=True):
    if is_json:
        with open(qrel_path, 'r', encoding='utf-8') as file:
            qrels = [json.loads(line) for line in file]
    else:
        with open(qrel_path, 'r', encoding='utf-8') as file:
            qrels = [line.strip() for line in file]
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
        for line in qrels:
            parts = line.split('\t')
            print(f"Parts: {parts}")  # Add this line for debugging
            if int(parts[0]) == query_id:
                answers.extend(parts[2])
    return answers



@app.route('/search', methods=['POST'])
def search():
    try:
        print("Received search request for type1")
        data_type = request.headers.get('Content-Type')

        if 'application/json' in data_type:
            data = request.json
            query = data.get('query')
        else:
            return jsonify({'error': 'Invalid content type for type1'}), 400

        print(f"Extracted query: {query}")

        if not query:
            return jsonify({'error': 'Query parameter is missing'}), 400

        dataset_path = 'C:/Users/hp/Dropbox/My PC (DESKTOP-UULDQBN)/Desktop/IR/lotte/lifestyle/dev/collection.tsv'
        queries_path = "C:/Users/hp/Dropbox/My PC (DESKTOP-UULDQBN)/Desktop/IR/lotte/lifestyle/dev/questions.forum.tsv"
        qrel_path = 'C:/Users/hp/Dropbox/My PC (DESKTOP-UULDQBN)/Desktop/IR/lotte/lifestyle/dev/qas.forum.jsonl'

        dataset = pd.read_csv(dataset_path, sep='\t', header=None)
        queries_df = pd.read_csv(queries_path, sep='\t', header=None)
        qrels = load_qrel_file(qrel_path, is_json=True)

        processor = DocumentProcessor()
        answer_ids = get_answers_for_query(processor, query, queries_df, qrels, is_json=True)

        if not answer_ids:
            return jsonify({'message': 'No answers found for the query'}), 404

        answers = dataset[dataset[0].isin(answer_ids)][1].tolist()

        return jsonify({'answers': answers})

    except Exception as e:
        print({"message": "Search endpoint reached", "error": str(e)})
        return jsonify({"message": "Search endpoint reached", "error": str(e)}), 500


@app.route('/search2', methods=['POST'])
def search2():
    try:
        print("Received search request")

        data_type = request.headers.get('Content-Type')
        # Extracting data from the request
        if 'multipart/form-data' in data_type:

            data = CombinedMultiDict([request.form, request.files])
        
        # Extracting query and category from the data
            query = data.get('query')
        else:
            return jsonify({'error': 'Invalid content type for type1'}), 400
        # التحقق من صحة البيانات المستلمة
        if not data or '\n' not in data:
            return 'Invalid data format', 400, {'Content-Type': 'text/plain; charset=utf-8'}
        

        print(f"Extracted query: {query}")
        

        if not query:
            return jsonify({'error': 'Query parameter is missing'}), 400

        dataset_path = 'C:/Users/hp/Desktop/IR/wikIR1k/documents.csv'
        queries_path = "C:/Users/hp/Desktop/IR/wikIR1k/training/queries.csv"
        qrel_path = 'C:/Users/hp/Desktop/IR/wikIR1k/training/qrels'

        dataset = pd.read_csv(dataset_path, sep='\t', header=None)
        queries_df = pd.read_csv(queries_path, sep='\t', header=None)
        qrels = load_qrel_file(qrel_path, is_json=False)

        processor = DocumentProcessor()
        answer_ids = get_answers_for_query(processor, query, queries_df, qrels, is_json=False)

        if not answer_ids:
            return 'No answers found for the query', 404
        
        answers = dataset[dataset[0].isin(answer_ids)][1].tolist()

        return '\n'.join(answers), 200, {'Content-Type': 'text/plain; charset=utf-8'}

    except Exception as e:
      print({"message": "Search endpoint reached", "error": repr(e)})
      return 'Search endpoint reached: ' + repr(e), 500, {'Content-Type': 'text/plain; charset=utf-8'}


if __name__ == '__main__':
    app.run(debug=True)