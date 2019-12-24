import os
from openie import StanfordOpenIE
import argparse

from utils import maybe_make_directory

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_path', type=str,
                        required=True,
                        help='Input path to a review. (required) (default: %(default)s)')
    parser.add_argument('--output_dir', type=str,
                        default='triples',
                        help='Directory path to the triples output. (default: %(default)s)')
    parser.add_argument('--interval', type=int, nargs=2,
                        required=True,
                        help='Interval of lines to read. (default: %(default)s)')
    
    
    args = parser.parse_args()
    
    maybe_make_directory(args.output_dir)

    return args

args = parse_args()

with StanfordOpenIE() as client:
    with open(args.input_path, 'r', encoding='utf8') as file:
        corpus = file.read().replace('\n', ' ').replace('\r', '')
    
    triples_corpus = client.annotate(corpus[args.interval[0]:args.interval[1]])
    print('Found %s triples in the corpus.' % len(triples_corpus))

    basename = os.path.basename(args.input_path)
    filename = os.path.splitext(basename)[0]
    with open(os.path.join(args.output_dir, f"{filename}_{args.interval[0]}_{args.interval[1]}.txt"), 'w') as output_file:
        for triple in triples_corpus:
            output_file.write(str(triple) + "\n")