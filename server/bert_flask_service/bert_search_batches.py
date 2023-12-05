#!/usr/bin/env python
# coding: utf-8

import torch
import fnmatch
import os, time
import json
import numpy as np


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

