import arxiv
import pandas as pd
import utils
import argparse
import datetime
import logging

logger = logging.getLogger(__name__)

def get_translated_metadata(result):
    
    entry_id = result.entry_id
    pdf = result.pdf_url
    
    year = str(result.published.year)
    month = str(result.published.month)
    day = str(result.published.day)
    
    cate = ", ".join(result.categories)
    author = ", ".join([str(athr) for athr in result.authors])
    if result.comment is None:
        comment = ""
    else:
        comment = result.comment
    
    title_en = result.title
    abst_en = result.summary.replace("\n", " ")

    # Translate paper title and abstract
    title_ja = utils.deepl(title_en)["translations"][0]["text"]
    abst_ja = utils.deepl(abst_en)["translations"][0]["text"]
    
    return [entry_id, pdf, year, month, day, cate, author, comment, title_en, abst_en, title_ja, abst_ja]


def search(query, categories, max_results=100, pub_date=None, 
           return_type="df", excluded_paper_list=[]):
    """
        Args:
            query: [Str]: Search query for paper title
            categories: [List]: Which category of papers to retrieve
            max_results: [Int]: Upper limit on how many papers you want to get
            pub_date: [datetime.datetime]: Retrieve papers submitted after this date.
            return_type: [Str]: Return type. You can choose DataFrame (df) or list.
            excluded_paper_list: [List]: Excluded paper entry IDs.
            
        Return:
            df: [pandas.DataFrame]: Search results
    
        Example:
        >>> query = "transformer"
        >>> categories = ['cs.CL',   # Computation and Language
                          'cs.IR',   # Information Retrieval
                          'cs.LG',   # Learning
                          'cs.CV',   # Computer Vision and Pattern Recognition
                          'stat.ML', # Machine Learning
                          'cs.AI',   # Artificial Intelligence
                          'cs.NE',   # Neural and Evolutionary Computing
                          ]
        >>> max_results = 10
        >>> pub_date = datetime.datetime(2020, 1, 1, 0, 0, 0, 0, datetime.timezone.utc)
        >>> search(query, categories, max_results, pub_date)
    """
    
    categories = set(categories)
    
    logger.info('Searching...')
    search = arxiv.Search(
      query = query,
      max_results = max_results,
      sort_by = arxiv.SortCriterion.SubmittedDate
    )

    logger.info('Translating...')
    paper_list = []
    for result in search.results():
        
        cond1 = len(list(set(result.categories) & categories))
        
        if pub_date is None:
            cond2 = True
        else:
            pub_date = pub_date.astimezone(datetime.timezone.utc)
            cond2 = result.published >= pub_date
            
        if result.entry_id in excluded_paper_list:
            cond3 = False
        else:
            cond3 = True
            
        # Translate
        if cond1 and cond2 and cond3:
            paper_list.append(get_translated_metadata(result))
            
    if return_type == "df":
        df = pd.DataFrame(paper_list, columns=["entry_id", "pdf", "year", "month", "day", 
                                               "cate", "author", "comment", 
                                               "title_en", "abst_en", 
                                               "title_ja", "abst_ja"])
        return df
    elif return_type == "list":
        return paper_list


if __name__ == '__main__':
    """
        Example:
        $ python search.py -q prompt -d 2021/1/1 -m 100
    """
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-q',  type=str, required=True, help="Search query for paper title")
    parser.add_argument('-m',  type=int, default=10, help="Upper limit on how many papers you want to get")
    parser.add_argument('-d',  type=str, default="2022/1/1", help="Retrieve papers submitted after this date.")
    parser.add_argument('-f',  type=str, default="result.tsv", help="Result file name")
    args = parser.parse_args()
    
    logging.basicConfig(level=logging.INFO)

    categories = ['cs.CL',   # Computation and Language
                  'cs.IR',   # Information Retrieval
                  'cs.LG',   # Learning
                  'cs.CV',   # Computer Vision and Pattern Recognition
                  'stat.ML', # Machine Learning
                  'cs.AI',   # Artificial Intelligence
                  'cs.NE',   # Neural and Evolutionary Computing
                  ]
    
    #pub_date = datetime.datetime(2020, 1, 1, 0, 0, 0, 0, datetime.timezone.utc)
    pub_date = datetime.datetime.strptime(args.d, '%Y/%m/%d')
    df = search(args.q, categories, args.m, pub_date)
    df.to_csv(args.f, sep="\t")
    logger.info('Saved at {}'.format(args.f))