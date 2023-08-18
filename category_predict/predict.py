import numpy as np
import pandas as pd

from pathlib import Path
from typing import *

import torch
import torch.optim as optim
import multiprocessing
from fastai import *
from fastai.vision import *
from fastai.text import *
# from fastai.callbacks import *

from sklearn.model_selection import train_test_split
from pytorch_pretrained_bert.modeling import BertConfig, BertForSequenceClassification
from pytorch_pretrained_bert import BertTokenizer

class Config(dict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for k, v in kwargs.items():
            setattr(self, k, v)

    def set(self, key, val):
        self[key] = val
        setattr(self, key, val)

class FastAiBertTokenizer(BaseTokenizer):
    """Wrapper around a BertTokenizer to be a BaseTokenizer in fastai"""
    def __init__(self, tokenizer: BertTokenizer, max_seq_len: int=128, **kwargs):
        self._pretrained_tokenizer = tokenizer
        self.max_seq_len = max_seq_len

    def __call__(self, *args, **kwargs):
        return self

    def tokenizer(self, t:str) -> List[str]:
        """Limits the maximum sequence length"""
        return ["[CLS]"] + self._pretrained_tokenizer.tokenize(t)[:self.max_seq_len - 2] + ["[SEP]"]

learner = load_learner(r"D:\four2\Graduating Design\nlp\category_predict\models")

def predict(input):
    return int(learner.predict(input)[1].item())


if __name__=="__main__":
    print(predict("有五排三列椅子和桌子。"))