from bs4 import BeautifulSoup
import urllib3
import requests
import pandas as pd


def setSoup(url, year):
    http = urllib3.PoolManager()
    html = requests.get(url)
    print(html)
    source = html
    return BeautifulSoup(source)


if __name__ == "__main__":
    year = 2019
    url = f"https://www.basketball-reference.com/leagues/{year}.html"
    soup = setSoup(url, year)
    '''
    soup.findAll('tr', limit=2)

    headers = [th.getText()
               for th in soup.findAll('tr', limit=2)[0].findAll('th')]

    headers = headers[1:]

    # print(headers)

    rows = soup.findAll('tr')[1:]
    player_stats = [[td.getText() for td in rows[i].findAll('td')]
                    for i in range(len(rows))]

    stats = pd.DataFrame(player_stats, columns=headers)
    stats.head(10)

    print(player_stats)
    print(headers)
    '''
