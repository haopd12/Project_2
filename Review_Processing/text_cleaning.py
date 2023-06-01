import pandas as pd
import numpy as np

# data visualization
import matplotlib.pyplot as plt
import seaborn as sns

# text processing
import re
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')
stopwords = set(stopwords.words('english'))

# utils
import os
from tqdm import tqdm
tqdm.pandas()
from collections import Counter

class TextCleaning:
    
    def rm_link(self,text):
        return re.sub(r'https?://\S+|www\.\S+', '', text)

# handle case like "shut up okay?Im only 10 years old"
# become "shut up okay Im only 10 years old"
    def rm_punct2(self,text):
        # return re.sub(r'[\!\"\#\$\%\&\'\(\)\*\+\,\-\.\/\:\;\<\=\>\?\@\[\\\]\^\_\`\{\|\}\~]', ' ', text)
        return re.sub(r'[\"\#\$\%\&\'\(\)\*\+\/\:\;\<\=\>\@\[\\\]\^\_\`\{\|\}\~]', ' ', text)

    def rm_html(self,text):
        return re.sub(r'<[^>]+>', '', text)

    def space_bt_punct(self,text):
        pattern = r'([.,!?-])'
        s = re.sub(pattern, r' \1 ', text)     # add whitespaces between punctuation
        s = re.sub(r'\s{2,}', ' ', s)        # remove double whitespaces    
        return s

    def rm_number(self,text):
        return re.sub(r'\d+', '', text)

    def rm_whitespaces(self,text):
        return re.sub(r' +', ' ', text)

    def rm_nonascii(self,text):
        return re.sub(r'[^\x00-\x7f]', r'', text)

    def rm_emoji(self,text):
        emojis = re.compile(
            '['
            u'\U0001F600-\U0001F64F'  # emoticons
            u'\U0001F300-\U0001F5FF'  # symbols & pictographs
            u'\U0001F680-\U0001F6FF'  # transport & map symbols
            u'\U0001F1E0-\U0001F1FF'  # flags (iOS)
            u'\U00002702-\U000027B0'
            u'\U000024C2-\U0001F251'
            ']+',
            flags=re.UNICODE
        )
        return emojis.sub(r'', text)

    def spell_correction(self,text):
        return re.sub(r'(.)\1+', r'\1\1', text)

    def clean_pipeline(self,text):    
        no_link = rm_link(text)
        no_html = rm_html(no_link)
        space_punct = space_bt_punct(no_html)
        no_punct = rm_punct2(space_punct)
        no_number = rm_number(no_punct)
        no_whitespaces = rm_whitespaces(no_number)
        no_nonasci = rm_nonascii(no_whitespaces)
        no_emoji = rm_emoji(no_nonasci)
        spell_corrected = spell_correction(no_emoji)
        return spell_corrected

    # preprocessing
    def tokenize(self,text):
        return word_tokenize(text)

    def rm_stopwords(self,text):
        return [i for i in text if i not in stopwords]

    def lemmatize(self,text):
        lemmatizer = WordNetLemmatizer()    
        lemmas = [lemmatizer.lemmatize(t) for t in text]
        # make sure lemmas does not contains sotpwords
        return rm_stopwords(lemmas)

    def preprocess_pipeline(self,text):
        tokens = tokenize(text)
        no_stopwords = rm_stopwords(tokens)
        lemmas = lemmatize(no_stopwords)
        return ' '.join(lemmas)