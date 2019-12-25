import os
import pandas as pd
import pickle
import argparse

from collections import Counter

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', type=str,
                        default='bin',
                        help='Directory path to the dataframe pickle. (default: %(default)s)')
    parser.add_argument('--output_dir', type=str,
                        default='reviews',
                        help='Directory path to the output sequences. (default: %(default)s)')
    parser.add_argument('--recommend', type=int,
                        required=True, choices=[0, 1],
                        help='Recommendation attribute of reviews. (required)')
    parser.add_argument('--sentiment', type=str,
                        required=True, choices=['pos', 'neu', 'neg'],
                        help='Sentiment connotation of reviews. (required)')
    parser.add_argument('--topn', type=int,
                        default=10,
                        help='Number of the most of common sequences. (default: %(default)s)')
    parser.add_argument('--write', action='store_true',
                        help='Boolean flag activating writing file output. (default: False)')
    
    args = parser.parse_args()

    return args

args = parse_args()

with open(os.path.join(args.input_dir, "df_vader.pickle"), "rb") as f:
    df = pickle.load(f)

    df = df[((df['recommended'] == args.recommend) & (df['sentiments'] == args.sentiment.upper()))]
    print(f"Recommended={True if args.recommend == 1 else 0}, Sentiment={args.sentiment.upper()}, counts={len(df)}")

    def extract_adjectives_word(df):
        adjectives_word = []
        for pos_tag in df['pos_tag']:
            for idx,(word, tag) in enumerate(pos_tag):
                if tag in ['JJ', 'JJR', 'JJS']:
                    if idx+1 < len(pos_tag) and pos_tag[idx+1][1] in ['NN', 'NNS', 'NNP', 'NNPS']:
                        adjectives_word.append((word, pos_tag[idx+1][0]))
        counts = Counter(adjectives_word).most_common(args.topn)
        if args.write:
            with open(os.path.join(args.output_dir, f"recommend_{'true' if args.recommend == 1 else 'false'}_{args.sentiment}_pairs_topn_{args.topn}"), "w") as f:
                for word, _ in counts:
                    f.write(word[0] + " " + word[1] + "\n")
        else:
            print("\nAdjective and noun sequences\n")
            for word, count in counts:
                print(word[0] + " " + word[1], count)
   
    extract_adjectives_word(df)

    def extract_adjectives(df):
        adjectives = []
        for pos_tag in df['pos_tag']:
            for word, tag in pos_tag:
                if tag in ['JJ', 'JJR', 'JJS']:
                    adjectives.append(word)
        counts = Counter(adjectives).most_common(args.topn)

        if args.write:
            with open(os.path.join(args.output_dir, f"recommend_{'true' if args.recommend == 1 else 'false'}_{args.sentiment}_adj_topn_{args.topn}"), "w") as f:   
                for word, _ in counts:
                    f.write(word + "\n")
        else:
            print("\nAdjective sequences\n")
            for word, count in counts:
                print(word, count)
 
    extract_adjectives(df)