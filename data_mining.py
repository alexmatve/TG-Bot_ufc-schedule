from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests


def get_events_from_card(data):
    fights = data.find_all('li', {'class': 'l-listing__item'})
    events = []
    for fight in fights:
        left_fighter = fight.find('div', {'class': 'c-listing-fight__corner-name--red'}).find('a').find_all('span')
        right_fighter = fight.find('div', {'class': 'c-listing-fight__corner-name--blue'}).find('a').find_all('span')

        left_fighter_name = " ".join([left_fighter[i].text for i in range(len(left_fighter))])
        right_fighter_name = " ".join([right_fighter[i].text for i in range(len(right_fighter))])
        events.append(left_fighter_name + " VS " + right_fighter_name)
    return events


url = "https://ufc.ru"
req = requests.get(url + "/events")

src = req.text
soup = BeautifulSoup(src, 'html.parser')

amount_tournaments = int(soup.find('div', {'class': 'althelete-total'}).text[-1])
events = soup.find_all('div', {'class': 'l-listing__item views-row'}, limit=amount_tournaments)

df = pd.DataFrame(columns=['url', 'date', 'main_card', 'prelims', 'events'])

for event in events:
    info = event.find('h3', {'class': 'c-card-event--result__headline'})
    href = info.find('a')['href']
    name = info.find('a').text
    if name == "TBD vs TBD":
        continue
    date = event.find('div', {'class': 'c-card-event--result__date'}).find('a').text
    df = pd.concat(
        [df, pd.DataFrame(data={'url': url + href, 'date': date, 'main_card': None, 'prelims': None, 'events': None},
                          index=[name])])
for name in df.index:
    url = df.loc[name, :]['url']
    req = requests.get(url)
    src = req.text
    soup = BeautifulSoup(src, 'html.parser')
    main_card = soup.find('div', {'class': 'main-card'})
    prelims_card = soup.find('div', {'class': 'fight-card-prelims'})

    if main_card is None or prelims_card is None:
        fight_card = soup.find('div', {'class': 'l-main__content'})
        events = get_events_from_card(fight_card)
        df.loc[name, 'events'] = events
    else:
        fights_main = get_events_from_card(main_card)
        fights_prelims = get_events_from_card(prelims_card)
        df.loc[name, 'main_card'] = fights_main
        df.loc[name, 'prelims'] = fights_prelims
