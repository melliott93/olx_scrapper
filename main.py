import requests
import re
from bs4 import BeautifulSoup
import time
from datetime import datetime,date
from telethon import TelegramClient, sync, events

def striphtml(data):
    p = re.compile(r'<.*?>')
    n = re.compile(r'\n')
    return n.sub(' ',p.sub('', data))

last_added_time = datetime.now()
today = date.today()

telegram_client = TelegramClient('scrapper', telegram_api_id, telegram_api_hash)

url = f"https://www.olx.pl/d/nieruchomosci/stancje-pokoje/warszawa/?search%5Border%5D=created_at:desc&search%5Bfilter_float_price:from%5D=600&search%5Bfilter_float_price:to%5D=1100"
while True:
    request = requests.get(url)
    bs = BeautifulSoup(request.text, "html.parser")
    all_link = bs.find_all("a", class_='css-rc5s2u')
    for link in all_link:
        result = re.search("otodom", str(link))
        if result:
            print("Otodom bullshit!")
        else: 
            add = f"https://www.olx.pl" + link["href"]
            request = requests.get(add)
            bs = BeautifulSoup(request.text, "html.parser")
            added = bs.find("span", class_='css-19yf5ek')
            added = re.match(r'''^.*\">(.*)\</.*$''',str(added))
            try:
                match = re.match(r'''Dzisiaj''',added)
                if match:
                    time_str = re.findall(r'\d+:\d+',link)
                    time_added = datetime.strptime(str(time_str), "['%H:%M']").time()
                    final_time = datetime.combine(date.today(), time_added)

                    if last_added_time < final_time:
                        title = bs.find("h1", class_='css-swd4zc-TextStyled er34gjf0')
                        title = re.match(r'''^.*\">(.*)\</.*$''',str(title))
                        description = striphtml(str(bs.find("div", class_="css-12l22jb-TextStyled er34gjf0")))
                        price = bs.find("h3", class_="css-19cr6mc-TextStyled er34gjf0")
                        price = re.match(r'''^.*\">(.*)\</.*$''',str(price))
                        price = ''.join(e for e in str(price.group(1)) if e.isalnum())
                        images = bs.find_all("img", class_="css-1bmvjcs")

                        final = []
                        final.append(added.group(1))
                        final.append(title.group(1))
                        final.append(description)
                        final.append(price)
                        images1 = []
                        for image in images:
                            try:
                                images1.append(image["src"])
                            except:
                                images1.append(image["data-src"])
                        telegram_client.send_message(chat, final, file=images1)
                        last_added_time = final_time
            except:
                None
    time.sleep(300)