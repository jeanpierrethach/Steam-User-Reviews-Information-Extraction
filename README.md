# Steam User Reviews Information Extraction


## Setup
#### Dependencies:
* python3, [stanford_openie](https://github.com/philipperemy/Stanford-OpenIE-Python), [vaderSentiment](https://github.com/cjhutto/vaderSentiment), etc.
#### To install the dependencies:
```
pip3 install -r requirements.txt
```

## Usage


## Extracting reviews
```
python3 extract_reviews.py [-h] <arguments> 
```
*Example*:
```
python3 extract_reviews.py --data_path ../data/australian_user_reviews.json
```

#### Arguments
* `--data_path`: Directory path to the data. *Default*: `../data/australian_user_reviews.json`
* `--output_dir`: Directory path to the output. *Default*: `reviews`

## Extracting recommended and unrecommended reviews
```
python3 extract_recommended.py [-h] <arguments> 
```
*Example*:
```
python3 extract_recommended.py --data_path ../data/australian_user_reviews.json --lower
```

#### Arguments
* `--data_path`: Directory path to the data. *Default*: `../data/australian_user_reviews.json`
* `--output_dir`: Directory path to the outputs. *Default*: `reviews`
* `--lower`: Boolean flag activating lowercasing of the reviews output. *Default*: `False`

## Extracting steam tags and plotting a distribution of game type frequency
```
python3 scrap_steam_tags.py [-h] <arguments> 
```
*Example*:
```
python3 scrap_steam_tags.py
```

#### Arguments
* `--input_dir`: Directory path to the reviews. *Default*: `reviews`
* `--output_dir`: Directory path to the figures. *Default*: `figures`

## Sentiment analysis with VADER and output a pickle file
```
python3 vader.py [-h] <arguments> 
```
*Example*:
```
python3 vader.py --data_path ../data/australian_user_reviews.json --verbose
```

#### Arguments
* `--data_path`: Directory path to the data. *Default*: `../data/australian_user_reviews.json`
* `--input_dir`: Directory path to the reviews. *Default*: `reviews`
* `--output_dir`: Directory path to the pickle output. *Default*: `bin`
* `--verbose`: Boolean flag activating console prints. *Default*: `False`

## Extracting sequences from the pickle file
```
python3 sequences.py [-h] <arguments> 
```
*Example*:
```
python3 sequences.py --recommend 1 --sentiment pos --topn 200 --write
```

#### Arguments
* `--input_dir`: Directory path to the dataframe pickle. *Default*: `bin`
* `--output_dir`: Directory path to the output sequences. *Default*: `reviews`
* `--recommend`: Recommendation attribute of reviews. *Choices*: `{0, 1}`. 0 = False, 1 = True. **(required)** *Default*: `None`
* `--sentiment`: Sentiment connotation of reviews. *Choices*: `{pos, neu, neg}` **(required)** *Default*: `None`
* `--topn`: Number of the most of common sequences. *Default*: `10`
* `--write`: Boolean flag activating writing file output. *Default*: `False`

## Extracting triples with StanfordOpenIE
```
python3 stanfordopenie.py [-h] <arguments> 
```
*Example*:
```
python3 stanfordopenie.py --input_path ./reviews/reviews_recommended_true.txt --interval 0 90000
```

#### Arguments
* `--input_path`: Input path to a review. **(required)** *Default*: `None`
* `--output_dir`: Directory path to the triples output. *Default*: `triples`
* `--interval`: Interval of lines to read. **(required; 2 arguments)** *Default*: `None`



# Authors 
Thach Jean-Pierre *- University of Montreal*

Wong Leo *- University of Montreal*