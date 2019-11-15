from bs4 import BeautifulSoup
from requests import get
import pandas as pd
import argparse
from time import sleep
from IPython.core.display import clear_output
import random

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ROWS_COUNT", help="Enter the no of films to scrape(Multiples of 50)", required=True, type=int)
    parser.add_argument("--COLUMN", help="Enter the specific column code of films to scrape"
                                         "  'ALL'=Complete details of a movie 'MY'=Movie name and Year"
                                         " 'MR'=Movie name and Rating   'MV'=Movie name and Votes"
                                             , required=True, type=str, choices=["ALL", "MY", "MR", "MV"])
    args = parser.parse_args()
    requests = 0
    headers = {"Accept-Language": "en-US, en;q=0.5"}
    movie_names = []
    year_of_release = []
    imdb_ratings = []
    votes = []
    count = args.ROWS_COUNT
    row = int(count) + 2
    address = [str(i) for i in range(51, row, 50)]
    for each_url in address:
        response = get('https://www.imdb.com/search/title?title_type=feature&release_date=2017-01-01,2018-12-31&start='
                       + each_url + '&ref_=adv_nxt')
        sleep(random.randint(8, 15))
        requests += 1
        print('Request:{}; Frequency: {} requests/s'.format(requests, requests))
        clear_output(wait=True)
        html_soup = BeautifulSoup(response.text, 'html.parser')
        movie_block = html_soup.find_all('div', class_='lister-item-content')
        for block in movie_block:
            name = block.a.text
            movie_names.append(name)
            year = block.h3.find('span', class_='lister-item-year text-muted unbold').text
            year_of_release.append(year[-5:-1])
            rating = float(block.strong.text)
            imdb_ratings.append(rating)
            vote = block.find('span', attrs={'name': 'nv'})['data-value']
            votes.append(int(vote))
        test_df = pd.DataFrame({'MOVIE': movie_names,
                                'YEAR': year_of_release,
                                'IMDB_RATING': imdb_ratings,
                                'VOTES': votes})
    print(test_df.info())
    if args.COLUMN == "ALL":
        print(test_df)
    elif args.COLUMN == "MY":
        print(test_df[['Movie', 'Year']])
    elif args.COLUMN == "MR":
        print(test_df[['MOVIE', 'IMDB_RATING']])
    else:
        print(test_df[['Movie', 'Votes']])