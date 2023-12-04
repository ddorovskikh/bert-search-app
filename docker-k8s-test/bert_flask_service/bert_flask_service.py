# -*- coding: utf-8 -*-

from flask import Flask, request, json, jsonify
from bert_search_batches import load_dataset, load_dataset_info, get_embeddings, find_by_key, unpack
import torch
import fnmatch
import os, time
#import json
from transformers import AutoTokenizer, AutoModel, BertTokenizer, BertModel, BertForSequenceClassification
from transformers import DistilBertTokenizer, DistilBertModel
import numpy as np
import pandas as pd
from sklearn.neighbors import KDTree
import argparse
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resource = { r"/": { "origins":"*"} })

@app.route('/', methods=['GET', 'POST'])
def getQueryFromReactReturnJson():
    if request.method == 'POST':
        query = request.get_data().decode("utf-8")
        '''
        return json.dumps({
           'table_data': {'test_query': query},
           'result_docs': [query],
           'time': (time.time()) / 60
        })
        '''
        start_time = time.time()
        query_embeddings = get_embeddings(query, tokenizer, model)
        dist, ind = tree.query(query_embeddings, k=100)
        most_relevant_quotes = [list_quotes[x] for x in ind[0]]
        result_docs = []
        table_data = {}
        response_num = 1
        for q in most_relevant_quotes:
            result_docs.append({
                'quote': str(q),
                'doc_ids': list(df.loc[df['quote'] == q].id.values), # list(df.loc[df['quote'] == q].id.values) -> id_quotes[q]
                'id_from': list(df.loc[df['quote'] == q].id_from.values)
            })
            #result_docs[response_num] = {'quote': q, 'doc_ids': id_quotes[q]}
            response_num += 1
        sorted_count = 0
        for quote_info in result_docs:
            for doc_id in quote_info['doc_ids']:
                sorted_count += 1
                if doc_id not in table_data:
                    find_article = find_by_key(dataset_info, 'pmid', 'doi', doc_id)
                    if find_article is not None:
                        table_data[doc_id] = {  # sorted_count -> doc_id
                            'title': str(find_article['article-title']),
                            'authors': list(find_article['authors']),
                            'doc_id': str(doc_id),
                            'abstract': str(find_article['abstract']),
                            'quotes': list([quote_info['quote']])
                        }
                else:
                    table_data[doc_id]['quotes'].append(str(quote_info['quote'])) # sorted_count -> doc_id

        #table_data['time'] = (time.time() - start_time) / 60
        
        json_response =  {
            'table_data': table_data,
            'result_docs': result_docs,
            'time': (time.time() - start_time) / 60
          }
        
        return json_response

    else:
        print(request)
        return request.get_data()

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Get path to saved model, path to datasets')

    parser.add_argument('path_to_model', help='Input path to saved model')
    parser.add_argument('path_to_datasets', help='Input path to datasets')

    args = parser.parse_args()

    path_to_model =  args.path_to_model
    path_to_datasets = args.path_to_datasets
    #  on server

    if torch.cuda.is_available():
        device = torch.device("cuda")
    else:
        device = torch.device("cpu")

    #tokenizer = AutoTokenizer.from_pretrained("/s/ls4/users/dasha/bert-base-uncased", do_lower_case=True)
    #model = AutoModel.from_pretrained("/s/ls4/users/dasha/bert-base-uncased", output_hidden_states=True).to(device)

    #path_to_model = "/mss_users/dasha/docker-k8s-test/bert_flask_service/model_save_v2_10k_20e" # bio1
    #path_to_model = "/home/dasha/docker-k8s-test/bert_flask_service/model_save_v2_10k_20e" # wn75
    #path_to_dataset = "/mss_users/dasha/dataset_quotes" # bio1
    #path_to_dataset = "/home/dasha/datasets" # wn75

    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased", do_lower_case=True)
    model = AutoModel.from_pretrained("bert-base-uncased", output_hidden_states=True).to(device)

    directory_path = path_to_datasets + '/dataset-quotes/'
    path_to_dataset_info = path_to_datasets + '/dataset-info/'
    path_to_big_file = path_to_datasets + '/id-quote.jsonl'


    #  local
    '''
    #tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased", do_lower_case=True)
    #model = AutoModel.from_pretrained("bert-base-uncased", output_hidden_states=True)
    tokenizer = BertTokenizer.from_pretrained('C:\\Users\\User\\bert_flask_service\\model_save_v2_10k_20e')
    model = BertForSequenceClassification.from_pretrained('C:\\Users\\User\\bert_flask_service\\model_save_v2_10k_20e', output_hidden_states=True)
    #tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
    #model = BertForSequenceClassification.from_pretrained("bert-base-uncased", output_hidden_states=True)

    directory_path = 'D:\\Users\\Антон\\Documents\\dataset-quotes\\'
    path_to_dataset_info = 'D:\\Users\\Антон\\Documents\\dataset-info\\'
    path_to_big_file = 'C:\\Users\\User\\get_quotes\\id-quote.jsonl'
    #directory_path = '/mss_users/dasha/dataset_quotes/dataset-quotes/'
    #path_to_dataset_info = '/mss_users/dasha/dataset_quotes/dataset-info/'
    '''

    print('Loading quotes dataset...')
    print(path_to_big_file)
    df = pd.read_json(path_to_big_file, lines=True, nrows=1000)
    df = df.apply(unpack)
    df = df.astype({"id": object, "id_from": object, "quote": object})
    #print(df.dtypes)
    quote_column = df[['quote']]
    quote_column_dropped = quote_column.drop_duplicates()
    list_quotes = quote_column_dropped['quote'].values
    # list_quotes = df['quote'].values
    # _, id_quotes = load_dataset(directory_path)
    print('Loading embeddings...')
    quote_embeddings = [get_embeddings(quote, tokenizer, model) for quote in list_quotes]
    embeddings = torch.cat(quote_embeddings, 0)
    print('Making KDTree...')
    tree = KDTree(embeddings, leaf_size=2)
    print('Loading articles info dataset...')
    dataset_info = load_dataset_info(path_to_dataset_info)

    app.run(debug=False, host='0.0.0.0', port=5000)
    #app.run(host='127.0.0.1', port=5555, debug=False)
