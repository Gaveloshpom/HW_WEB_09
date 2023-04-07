import json

import requests
from bs4 import BeautifulSoup

base_url = 'https://quotes.toscrape.com'
urls = []

quotes_list = []
authors_list = []

cache = []

for i in range(1, 11):
    urls.append(f'{base_url}/page/{i}/')


def quotes_parser():
    for url in urls:

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')

        quotes = soup.find_all('span', class_='text')
        tags = soup.find_all('div', class_='tags')
        quotes_authors = soup.find_all('small', class_='author')

        for i in range(0, len(quotes)):
            quotes_result = {'tags': [n.text for n in tags[i].find_all('a', class_='tag')],
                             'author': quotes_authors[i].text, 'quote': quotes[i].text}
            quotes_list.append(quotes_result)


def authors_parser():
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')

        quote_card = soup.find_all('div', class_='quote')
        authors_urls = []

        for data in quote_card:  # Робимо посилання на авторів

            author_link = base_url + data.find('a').get('href')
            authors_urls.append(author_link)

        for link in authors_urls:  # Оброблюємо авторів

            response = requests.get(link)
            soup = BeautifulSoup(response.text, 'lxml')

            fullname = soup.find('h3', class_='author-title').text.strip()

            if fullname not in cache:  # перевіряємо чи вже не записаний автор

                if fullname == 'Alexandre Dumas-fils':    #Це ім'я ламає потім завантаження до БД, я не знаю як ще це пофіксити
                    fullname = 'Alexandre Dumas fils'

                born_date = soup.find('span', class_='author-born-date').text
                born_location = soup.find('span', class_='author-born-location').text
                description = soup.find('div', class_='author-description').text.strip()

                authors_result = {'fullname': fullname, 'born_date': born_date, 'born_location': born_location,
                                  'description': description}

                cache.append(fullname)
                authors_list.append(authors_result)
            else:
                continue


def main():
    quotes_parser()
    authors_parser()

    with open('quotes.json', 'w', encoding='utf-8') as fd:
        json.dump(quotes_list, fd, indent=4, ensure_ascii=False)

    with open('authors.json', 'w', encoding='utf-8') as fd:
        json.dump(authors_list, fd, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()

