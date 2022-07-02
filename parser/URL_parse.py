import requests
from bs4 import BeautifulSoup


def url_parse(page, output_file):

    ''' В аргументах указать кол-во страниц каталога компаний(226 сейчас),  название json файла на выходе с данными'''

    persons_url_list = []

    for i in range(0, page):
        url = f'https://xn--b1aedfedwrdfl5a6k.xn--p1ai/producers?region=23077&page={i}'

        q = requests.get(url)
        result = q.content

        soup = BeautifulSoup(result, 'lxml')
        persons1 = soup.find_all(class_='manufacturers-card-img')
        persons2 = soup.find_all(class_='manufacturers-card-img-3')

        for person in persons1:
            person_page_url = person.get('href')
            persons_url_list.append('https://xn--b1aedfedwrdfl5a6k.xn--p1ai' + person_page_url)

            print(f'Пройдена страница {i}, {person_page_url}')

        for person in persons2:
            person_page_url = person.get('href')
            persons_url_list.append('https://xn--b1aedfedwrdfl5a6k.xn--p1ai' + person_page_url)

            print(f'Пройдена страница {i}, {person_page_url}')

    with open(output_file, 'a') as file:
        for line in persons_url_list:
            file.write(f'{line}\n')


# url_parse(486, 'urls_moscow.txt')