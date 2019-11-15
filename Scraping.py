from bs4 import BeautifulSoup
from requests import get
import pandas as pd
from time import sleep
from random import randint
from IPython.core.display import clear_output
headers = {"Accept-Language": "en-US, en;q=0.5"}
address = [str(i) for i in range(51,100,50)] #(number 301-depends on the number of pages you need to scrape)
requests = 0
movie_names = []
year_of_release = []
imdb_ratings = []
run_tym = []
votes = []
genres = []
for each in address:
    response = get('https://www.imdb.com/search/title?title_type=feature&release_date=2017-01-01,2018-12-31&start='+each+'&ref_=adv_nxt',headers = headers)
    sleep(randint(8,15))
    requests += 1
    print('Request:{}; Frequency: {} requests/s'.format(requests, requests))
    clear_output(wait = True)
    if requests > 6: #number depends on end count provided in line 8(in this code 301/50(per page))
        warn('Number of requests was greater than expected.')  
        break 
    html_soup = BeautifulSoup(response.text, 'html.parser')
    movie_block = html_soup.find_all('div', class_ = 'lister-item-content')
    for block in movie_block:
        name = block.a.text
        movie_names.append(name)
        year = block.h3.find('span', class_ = 'lister-item-year text-muted unbold').text
        year_of_release.append(year[-5:-1])
        rating = float(block.strong.text)
        imdb_ratings.append(rating)
        run_time=block.find('span', class_ = 'runtime').text
        run_tym.append(run_time)
        vote = block.find('span', attrs = {'name':'nv'})['data-value']
        votes.append(int(vote))
        genre=block.find('span', class_ = 'genre').text
        genres.append((genre[1:]))
test_df = pd.DataFrame({'Movie': movie_names,
                       'Year': year_of_release,
                       'IMDB': imdb_ratings,
                       'Run_Time': run_tym,
                       'Votes': votes,
                       'Genre': genres})


print(test_df.info())
test_df.to_json(orient='records')
test_df.to_csv('Movies_List')