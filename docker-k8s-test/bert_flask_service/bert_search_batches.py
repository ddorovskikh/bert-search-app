#!/usr/bin/env python
# coding: utf-8

import torch
import fnmatch
import os, time
import json
from transformers import AutoTokenizer, AutoModel, BertTokenizer, BertModel
from transformers import DistilBertTokenizer, DistilBertModel
import numpy as np
from sklearn.neighbors import KDTree


#start_time = time.time()
'''
if torch.cuda.is_available():
    # Tell PyTorch to use the GPU.
    device = torch.device("cuda")
    print(f'device: {device}')
    print('There are %d GPU(s) available.' % torch.cuda.device_count())
    print('We will use the GPU:', torch.cuda.get_device_name(0))
else:
    print('No GPU available, using the CPU instead.')
    device = torch.device("cpu")

tokenizer = AutoTokenizer.from_pretrained("/s/ls4/users/dasha/bert-base-uncased", do_lower_case=True)
model = AutoModel.from_pretrained("/s/ls4/users/dasha/bert-base-uncased", output_hidden_states=True).to(device)


directory_path = '/s/ls4/users/dasha/dataset-quotes/'
'''
def find_by_key(iterable, key1, key2, value):
    for index, dict_ in enumerate(iterable):
        if dict_[key1] == value or dict_[key2] == value:
            return dict_
    return None

def load_dataset_info(directory_path):
    dataset_info = []

    for root, dirnames, filenames in os.walk(directory_path):
        for filename in fnmatch.filter(filenames, '*.json'):
            with open(os.path.join(root, filename), 'r') as f:
                data = json.load(f)
                dataset_info.append(data)
    return dataset_info

def unpack(x):
    rv = []
    for v in x:
        if isinstance(v, dict):
            rv.append([*v.values()][0])
        else:
            rv.append(v)
    return rv

def load_dataset(directory_path):
    list_quotes = []
    id_quotes = {}

    for root, dirnames, filenames in os.walk(directory_path):
        if len(list_quotes) < 10000:
            for filename in fnmatch.filter(filenames, '*.json'):
                with open(os.path.join(root, filename), 'r') as f:
                    data = json.load(f)
                    list_quotes.extend(data['quotes'])
                    for q in data['quotes']:
                        if q not in id_quotes:
                            id_quotes[q] = [data['id']]
                        elif q in id_quotes and data['id'] not in id_quotes[q]:
                            id_quotes[q].append(data['id'])
        else:
            break

    return list_quotes, id_quotes

def get_embeddings(text, tokenizer, model):
    tokens=tokenizer(text, max_length=20, padding='max_length', truncation=True)
    output=model(torch.tensor(tokens['input_ids']).unsqueeze(0),
               attention_mask=torch.tensor(tokens['attention_mask']).unsqueeze(0)).hidden_states[-1]
    return torch.mean(output,axis=1).detach().cpu()

'''
list_quotes = []
id_quotes = {}

for root, dirnames, filenames in os.walk(directory_path):
    #if len(list_quotes) < 500:  # works with 1500
    for filename in fnmatch.filter(filenames, '*.json'):
        try:
            with open(os.path.join(root, filename), 'r') as f:
                data = json.load(f)
                list_quotes.extend(data['quotes'])
                for q in data['quotes']:
                    if q not in id_quotes:
                        id_quotes[q] = [data['id']]
                    elif q in id_quotes and data['id'] not in id_quotes[q]:
                        id_quotes[q].append(data['id'])
        except:
            print(f'Error with {root}/{filename}')
    #else:
    #    break
'''
'''
def get_embeddings(text):
    tokens=tokenizer(text, max_length=20, padding='max_length', truncation=True)
    output=model(torch.tensor(tokens.input_ids).unsqueeze(0).to(device),
               attention_mask=torch.tensor(tokens.attention_mask).unsqueeze(0).to(device)).hidden_states[-1]
    return torch.mean(output,axis=1).detach().cpu()

quote_embeddings = [get_embeddings(quote) for quote in list_quotes]


embeddings = torch.cat(quote_embeddings, 0)
#embeddings.shape

tree = KDTree(embeddings, leaf_size=2)


query = 'DNA and brain activity analysis using machine learning methods'
query_embeddings = get_embeddings(query)

dist, ind = tree.query(query_embeddings, k=10)


most_relevant_quotes = [list_quotes[x] for x in ind[0]]  # list_quotes[ranks[0]]

result_docs = []
for q in most_relevant_quotes:
    result_docs.append({'quote': q, 'doc_ids': id_quotes[q]})
    #result_docs[q] = id_quotes[q]

print(f'Operating time for ~{len(list_quotes)} quotes: {(time.time() - start_time) / 60} min')
#most_relevant_quotes
print(result_docs)
'''
