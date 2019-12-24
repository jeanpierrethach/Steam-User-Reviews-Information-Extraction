import os
import sys
import ast
import argparse

from utils import maybe_make_directory

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', type=str,
                        default='../data/australian_user_reviews.json',
                        help='Directory path to the data. (required) (default: %(default)s)')
    parser.add_argument('--output_dir', type=str,
                        default='reviews',
                        help='Directory path to the reviews. (default: %(default)s)')
    parser.add_argument('--lower', action='store_true',
                        help='Boolean flag activating lowercasing of the reviews output. (default: False)')
    
    args = parser.parse_args()
    
    maybe_make_directory(args.output_dir)

    return args

args = parse_args()

LOWER_REVIEWS = args.lower
JSON_DATAPATH = args.data_path

if LOWER_REVIEWS:
    filename_rt = os.path.join(args.output_dir, "reviews_recommended_true_lowered.txt")
    filename_rf = os.path.join(args.output_dir, "reviews_recommended_false_lowered.txt")
else:
    filename_rt = os.path.join(args.output_dir, "reviews_recommended_true.txt")
    filename_rf = os.path.join(args.output_dir, "reviews_recommended_false.txt")

with open (filename_rt, 'w') as output_file:
    with open(JSON_DATAPATH) as json_file:
        for line in json_file:
            data_dict = ast.literal_eval(line)
            for review in data_dict['reviews']:
                if review['recommend'] == True:
                    if LOWER_REVIEWS:
                        output_file.write(review['review'].lower() + "\n")
                    else:
                        output_file.write(review['review'] + "\n")

with open (filename_rf, 'w') as output_file:
    with open(JSON_DATAPATH) as json_file:
        for line in json_file:
            data_dict = ast.literal_eval(line)
            for review in data_dict['reviews']:
                if review['recommend'] == False:
                    if LOWER_REVIEWS:
                        output_file.write(review['review'].lower() + "\n")
                    else:
                        output_file.write(review['review'] + "\n")
