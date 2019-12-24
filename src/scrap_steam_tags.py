import os
import requests
from bs4 import BeautifulSoup
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import argparse

from utils import maybe_make_directory

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', type=str,
                        default='reviews',
                        help='Directory path to the reviews. (default: %(default)s)')
    parser.add_argument('--output_dir', type=str,
                        default='figures',
                        help='Directory path to the figures. (default: %(default)s)')
    args = parser.parse_args()

    maybe_make_directory(args.output_dir)
    
    return args

args = parse_args()

data = requests.get("https://store.steampowered.com/tag/browse/#global_492")

soup = BeautifulSoup(data.text, 'html.parser')

tag_query = soup.find_all("div", class_="tag_browse_tag")

game_types = []

for tag in tag_query:
    game_types.append(tag.text)
print(game_types)
print(f"Number of game types: {len(game_types)}")

review_input_path = os.path.join(args.input_dir, "reviews.txt")

with open(review_input_path, 'r', encoding='utf8') as f:
    gt_list = []
    for line in f:
        for gt in game_types:
            if gt in line:
                gt_list.append(gt)
    counts = Counter(gt_list)

    df = pd.DataFrame.from_dict(counts, orient='index').reset_index()
    df = df.rename(columns={'index':'gametype', 0:'count'})
    df = df[df['count'] >= 25]
    df = df.sort_values(by='count', ascending=False)

    f, ax = plt.subplots(figsize=(10, 10))
    ax = sns.barplot(
        y='gametype',
        x='count',
        data=df)
    _ = ax.set(xlabel='Counts', ylabel='Game Type', title='Game Type frequency')

    ax.figure.savefig(os.path.join(args.output_dir, 'gametype_distrib.png'))