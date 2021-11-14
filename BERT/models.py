import math
import json
from typing import NamedTuple

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

# from utils import split_last, merge_last

class Config(NamedTuple):
    "configuration for BERT model"
    vocab_size: int = None # Size for Vocabulary
    dim: int = 768 # Dimension of Hidden Layer in Transformer Encoder
    n_layers: int = 12 # Number of Hidden Layers
    n_heads: int = 12 # Number of Heads in Multi-Headed Attention Layers
    dim_ff: int = 768*4 # Dimension of Intermediate layers in Postionwise Feedforward Net
    #activ_fn: str = "gelu" # Non-linear Activation Function Type in Hidden Layers
    p_drop_hidden: float = 0.1 # Probability of Dropout of various Hidden layers
    p_drop_attn: float = 0.1 # Probability of Dropout of Attention Layers
    max_len: int = 512 # Maximum Length for Positional Embeddings
    n_segments: int = 2 # NUmber of Sentence Segments

    @classmethod
    def from_json(cls, file):
        return cls(**json.load(open(file,"r")))

def gelu(x):
    "Implementation of the gelu activation function by Hugging Face"
    return x * 0.5 * (1.0 + torch.erf(x/math.sqrt(2.0)))

class LayerNorm(nn.Module):
    """
    A layernorm module in the TF stype(epilon inside the square root).
    normalization + afiine transformation
    """
    def __init__(self, cfg, variance_epsilon=1e-12):
        super().__init__()
        self.gamma = nn.Parameter(torch.ones(cfg.dim))
        self.beta = nn.Parameter(torch.zeros(cfg.dim))
        self.variance_epsilon = variance_epsilon
    
    def forward(self,x): 
        u = x.mean(-1, keepdim=True)
        s = (x-u).pow(2).mean(-1,keepdim=True)
        x = (x-u) / torch.sqrt(s + self.variance_epsilon)
        return self.gamma*x + self.beta


class Embeddings(nn.Module):
    "the embedding module from word, position and token_type embeddings"
    def __init__(self,cfg):
        super().__init__()
        self.tok_embed = nn.Embedding(cfg.vocab_size, cfg.dim) #token embedding
        self.pos_embed = nn.Embedding(cfg.max_len, cfg.dim) #position embedding
        self.seg_embed = nn.Embedding(cfg.n_segments, cfg.dim) #segment(token type) embedding

        self.norm = LayerNorm(cfg)
        self.drop = nn.Dropout(cfg.p_drop_hidden)

    def forward(self, x, seg):
        seq_len = x.size(1)
        pos = torch.arange(seq_len, dtype=torch.long, device=x.device)
        pos = pos.unsqueeze(0).expand_as(x) #(S,) => (B,S)

        e = self.tok_embd(x) + self.pos_embed(pos) + self.seg_embed(seg)
        return self.drop(self.norm(e))

