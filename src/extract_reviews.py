import os
import sys
import ast
import argparse

from utils import maybe_make_directory

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', type=str,
                        default='../data/australian_user_reviews.json',
                        help='Directory path to the data. (default: %(default)s)')
    parser.add_argument('--output_dir', type=str,
                        default='reviews',
                        help='Directory path to the reviews. (default: %(default)s)')
    
    args = parser.parse_args()
    
    maybe_make_directory(args.output_dir)

    return args

args = parse_args()

review_output_path = os.path.join(args.output_dir, "reviews.txt")

with open (review_output_path, 'w') as output_file:
    with open(args.data_path) as json_file:
        for line in json_file:
            data_dict = ast.literal_eval(line)
            for review in data_dict['reviews']:
                output_file.write(review['review'] + "\n")
