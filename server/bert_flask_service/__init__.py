import pandas as pd
import fnmatch
import os, time
import json
from transformers import AutoTokenizer, AutoModel
import torch
from sklearn.neighbors import KDTree
from bert_flask_service.bert_search_batches import load_dataset_info, get_embeddings, unpack
import argparse


#parser = argparse.ArgumentParser(description='Get path to saved model, path to datasets')
#parser.add_argument('path_to_model', help='Input path to model')
#parser.add_argument('path_to_datasets', help='Input path to datasets')
#args = parser.parse_args()

#path_to_datasets = args.path_to_datasets
#path_to_model = args.path_to_model

path_to_datasets = os.environ.get("FLASK_PATH")
path_to_model = os.environ.get("BERT_MODEL")

print("path to datasets dir:", path_to_datasets)
print("path to model:", path_to_model)
print("-----------------------")

tokenizer = AutoTokenizer.from_pretrained(path_to_model, do_lower_case=True)
model = AutoModel.from_pretrained(path_to_model, output_hidden_states=True)

directory_path = path_to_datasets + '/dataset-quotes/'
path_to_dataset_info = path_to_datasets + '/dataset-info/'
path_to_big_file = path_to_datasets + '/id-quote.jsonl'

print('Loading quotes dataset...')

df = pd.read_json(path_to_big_file, lines=True, nrows=1000)
df = df.apply(unpack)
df = df.astype({"id": object, "id_from": object, "quote": object})

quote_column = df[['quote']]
quote_column_dropped = quote_column.drop_duplicates()
list_quotes = quote_column_dropped['quote'].values

print('Loading embeddings...')
quote_embeddings = [get_embeddings(quote, tokenizer, model) for quote in list_quotes]
embeddings = torch.cat(quote_embeddings, 0)

print('Making KDTree...')
tree = KDTree(embeddings, leaf_size=2)

print('Loading articles info dataset...')
dataset_info = load_dataset_info(path_to_dataset_info)

print("---------------------------------------------------------------")

#import bert_flask_service.bert_flask_service
