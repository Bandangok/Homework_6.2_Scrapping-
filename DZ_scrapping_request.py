from pprint import pprint
import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import json


headers = Headers(os='win', browser='firefox')


response = requests.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2', headers=headers.generate())
main_html_data = response.text
main_soup = BeautifulSoup(main_html_data, 'lxml')


vacancy_list = main_soup.find(class_='vacancy-serp-content')
vacancy_card = vacancy_list.find_all(class_='vacancy-serp-item__layout')

json_list = []

for vacancy in vacancy_card:
    link_tag = vacancy.find('a', class_='bloko-link')
    link = link_tag['href']

    wages_tag = vacancy.find('span', class_='bloko-header-section-2')
    if wages_tag != None:
        wages = wages_tag.text
    else:
        wages = "Заработная плата не указана"


    company_tag = vacancy.find('a', class_='bloko-link bloko-link_kind-tertiary')
    company = company_tag.text

    city_tag = vacancy.find('div', class_='vacancy-serp-item__info')
    if 'Москва' in city_tag.text:
        city = 'Москва'
    elif 'Санкт-Петербург' in city_tag.text:
        city = 'Санкт-Петербург'
    else:
        city = 'Город не указан'

    response_1 = requests.get(link, headers=headers.generate())
    vacancy_html_data = response_1.text
    vacancy_soup = BeautifulSoup(vacancy_html_data, 'lxml')

    vacancy_desc_tag = vacancy_soup.find('div', class_='bloko-columns-row')
    vacancy_desc = vacancy_desc_tag.text



    if "Django" in vacancy_desc and "Flask" in vacancy_desc:
        json_list.append(
            {
                'Ссылка на вакансию': link,
                'Заработная плата': wages,
                'Название компании': company,
                'Город': city
           }
              )


with open("vacancy.json", "w", encoding='utf-8') as file:
    json.dump(json_list, file, ensure_ascii=False, indent=4)
pprint(json_list)