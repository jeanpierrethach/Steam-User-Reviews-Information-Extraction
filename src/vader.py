import os
import sys
import ast
import numpy as np
import pandas as pd
import pickle
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk import pos_tag, pos_tag_sents
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import argparse

from utils import maybe_make_directory

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', type=str,
                        default='../data/australian_user_reviews.json',
                        help='Directory path to the data. (default: %(default)s)')
    parser.add_argument('--input_dir', type=str,
                        default='reviews',
                        help='Directory path to the reviews. (default: %(default)s)')
    parser.add_argument('--output_dir', type=str,
                        default='bin',
                        help='Directory path to the pickle output. (default: %(default)s)')
    parser.add_argument('--verbose', action='store_true',
                        help='Boolean flag activating console prints. (default: False)')
    
    args = parser.parse_args()
    
    maybe_make_directory(args.output_dir)

    return args

args = parse_args()

analyser = SentimentIntensityAnalyzer()

def sentiment_analyzer_scores(sentence):
    score = analyser.polarity_scores(sentence)
    if args.verbose:
        print("{:-<40} {}".format(sentence, str(score)))
    return score

reviews = []
scores = []
sentiments = []
neg = []
neu = []
pos = []

review_input_path = os.path.join(args.input_dir, "reviews.txt")

with open(review_input_path, 'r') as reviews_file:
    for line in reviews_file:
        score = sentiment_analyzer_scores(line)
        reviews.append(line)
        scores.append(score)
        neg.append(score['neg'])
        neu.append(score['neu'])
        pos.append(score['pos'])
        idx = np.argmax(np.array([score['neg'], score['neu'], score['pos']]))
        if idx == 0:
            sentiments.append('NEG')
        elif idx == 1:
            sentiments.append('NEU')
        elif idx == 2:
            sentiments.append('POS')

recommendations = []

with open(args.data_path) as json_file:
    for line in json_file:
        data_dict = ast.literal_eval(line)
        for review in data_dict['reviews']:
            recommendations.append(review['recommend'])

def enhance_pos_tag(df):
    dataframe = df
    dataframe['pos_tag'] = pos_tag_sents(df['reviews'].apply(word_tokenize).tolist())
    return dataframe

df = pd.DataFrame(list(zip(reviews, scores, neg, neu, pos, recommendations, sentiments)), 
                    columns=['reviews', 'scores', 'neg', 'neu', 'pos', 'recommended', 'sentiments'])

df = enhance_pos_tag(df)

df_output_path = os.path.join(args.output_dir, "df_vader.pickle")

with open(df_output_path, 'wb') as f:
    pickle.dump(df, f)