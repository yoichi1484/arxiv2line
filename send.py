import requests
import search
import datetime
import argparse
from tqdm import tqdm

import logging
logger = logging.getLogger(__name__)

# webhook POST URL
with open("web-post-url.txt") as f:
    POST_URL = f.read()
    
if __name__ == '__main__':
    """
        Example:
        $ python send.py -q prompt -d 2021/1/1 -m 100
    """
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-q',  type=str, required=True, help="Search query for paper title")
    parser.add_argument('-m',  type=int, default=10, help="Upper limit on how many papers you want to get")
    parser.add_argument('-d',  type=str, default="2022/1/1", help="Retrieve papers submitted after this date.")
    parser.add_argument('-f',  type=str, default="result.tsv", help="Result file name")
    args = parser.parse_args()
    
    logging.basicConfig(level=logging.INFO)

    # Query and info for searching
    args.q = args.q.replace("_", " ") # e.g. foundation_model => foundation model
    logger.info('Query: {}'.format(args.q))
    
    categories = ['cs.CL',   # Computation and Language
                  'cs.IR',   # Information Retrieval
                  'cs.LG',   # Learning
                  'cs.CV',   # Computer Vision and Pattern Recognition
                  'stat.ML', # Machine Learning
                  'cs.AI',   # Artificial Intelligence
                  'cs.NE',   # Neural and Evolutionary Computing
                  ]
    pub_date = datetime.datetime.strptime(args.d, '%Y/%m/%d')
    excluded_paper_list = []
    return_type="list"
    
    # Get paper info via arXiv API
    paper_list = search.search(args.q, categories, args.m, pub_date, 
                               return_type, excluded_paper_list)

    # Post paper info
    logger.info('Post paper info in LINE ...')
    for paper in tqdm(paper_list):
        message = "\n".join(["<br>タイトル:  " + paper[-2], 
                             "<br><br> 検索クエリ: " + query,
                             "<br><br>PDF: " + paper[1], 
                             "<br><br>出版日: {}/{}/{}".format(paper[2], paper[3], paper[4]), 
                             "<br><br>カテゴリ: " + paper[5],
                             "<br><br>著者: " + paper[6],
                             #"<br><br>Title:  " + paper[-4], 
                             #"<br><br>Abstract: " + paper[-3],
                             #"<br><br>タイトル:  " + paper[-2], \
                             "<br><br>概要: " + paper[-1],
                            ])
        requests.post(POST_URL, data={"value1": message})

