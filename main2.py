import pandas as pd
from QueryProcessor2 import DocumentProcessor
from Evaluator2 import Evaluator


def main():
    dataset_path = 'C:/Users/user/Desktop/IR/wikIR1k/documents.csv'
    queries_path = 'C:/Users/user/Desktop/IR/wikIR1k/training/queries.csv'

    # Load and process documents
    doc_processor = DocumentProcessor(dataset_path)
    doc_processor.load_documents()

    # Load queries
    queries_df = pd.read_csv(queries_path)
    queries_df['id_left'] = queries_df['id_left'].astype(str)
    queries_df['text_left'] = queries_df['text_left'].astype(str)
    all_queries = {queries_df.iloc[index, 0]: queries_df.iloc[index, 1] for index in range(len(queries_df))}

    # Process queries and match
    queries_answers = {}
    for id, text in all_queries.items():
        preprocessed_query = doc_processor.preprocess_query(text)
        queries_answers[id] = doc_processor.match_query(preprocessed_query)

    # Evaluate results
    evaluator = Evaluator(queries_answers)
    evaluation_results = evaluator.compute_evaluation()

    # Print evaluation results
    for e in evaluation_results.items():
        print(e)

if __name__ == "__main__":
    main()
