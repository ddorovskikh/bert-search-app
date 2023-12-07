# -*- coding: utf-8 -*-

from flask import Flask, request, json, jsonify
from flask_cors import CORS
from marshmallow import Schema, fields, validate, ValidationError
import os, time

from bert_flask_service import tokenizer, model, df, list_quotes, tree, dataset_info
from bert_flask_service.bert_search_batches import load_dataset, load_dataset_info, get_embeddings, find_by_key, unpack



app = Flask(__name__)
CORS(app, resource = { r"/": { "origins":"*"} })

class MySchema(Schema):
    query = fields.String(required=True, validate=validate.Length(max=200, error='Query must be a string shorter than 200 letters.'))

@app.route('/', methods=['GET', 'POST'])
def getQueryFromReactReturnJson():
    if request.method == 'POST':
        start_time = time.time()
        response = json.loads(request.get_data().decode("utf-8"))
        schema = MySchema()
        try:
            schema_data = schema.load(response)
        except ValidationError as err:
            return {
              'table_data': {},
              'result_docs': [],
              'time': (time.time() - start_time) / 60,
              'error': err.messages['query'][0]
            }
        query = schema_data['query']
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

        json_response =  {
            'table_data': table_data,
            'result_docs': result_docs,
            'time': (time.time() - start_time) / 60,
            'error': ''
          }

        return json_response

    else:
        print(request)
        return request.get_data()

if __name__ == '__main__':

    app.run(debug=False, host='0.0.0.0', port=5000)
