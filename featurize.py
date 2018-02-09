import gzip, sys, numpy as np

def load_subtitle_text(path):
  return [l for l in gzip.open(path).read().split('\n') if '<' not in l and '>' not in l]

