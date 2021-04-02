import requests
from bs4 import BeautifulSoup
import pandas as pd
import lxml


URL = 'https://www.imdb.com/chart/tvmeter/'

imdb = requests.get(URL)

soup = BeautifulSoup(imdb.content, "lxml")


title = soup.select('tr td.titleColumn a')

title_mod = [i.text for i in title]



urls = ['https://www.imdb.com' + i['href'] for i in title]

rank = soup.find_all(class_='velocity')

rank_mod = [i.text for i in rank]

rank_mod = [i.split('\n')[0] for i in rank_mod]

rating = soup.select('tr td.ratingColumn.imdbRating')

rating_mod = [i.text for i in rating]
new_rating = []
for i in rating:
    new = ''
    if 'strong' not in str(i):
        new = '0.0'
    else:
        new = i.text
    new_rating.append(new)

new_rating_mod = [i.replace('\n', '') for i in new_rating]

imdb_top = {
    'Rank': rank_mod,
    'Title': title_mod,
    'Rating': new_rating_mod,
    'Url': urls
}



pd.DataFrame(imdb_top).to_csv('imdb.csv', index=False)

