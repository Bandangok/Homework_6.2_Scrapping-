from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.chrome.options import Options

def wait_element(browser, delay_seconds=1, by=By.TAG_NAME, value=None):
    return WebDriverWait(browser, delay_seconds).until(
        expected_conditions.presence_of_element_located((by, value)))


chrome_webdriver_path = ChromeDriverManager().install()
browser_service = Service(executable_path=chrome_webdriver_path)
options = Options()
options.add_argument('--headless')
browser = Chrome(service=browser_service, options=options)
browser.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2')

vacancy_list_tag = wait_element(browser, 1, By.CLASS_NAME, 'vacancy-serp-content')
vacancy_card = vacancy_list_tag.find_elements(By.CLASS_NAME, 'vacancy-serp-item__layout')
json_list = []

for vacancy in vacancy_card:
    link_tag = wait_element(vacancy, 1, By.CLASS_NAME, 'bloko-link')
    link = link_tag.get_attribute('href')

    salary_tag = wait_element(vacancy, 1, By.CLASS_NAME, 'bloko-header-section-2')
    if salary_tag != None:
        salary = salary_tag.text.strip()
    else:
        salary = "Заработная плата не указана"

    company_tag = wait_element(vacancy, 1, By.CLASS_NAME, 'bloko-link bloko-link_kind-tertiary')
    company = company_tag.get_attribute('class')

    json_list.append({
        'сслыка': link,
        'вилка зп': salary,
        'название компании': company
    })


# with open("vacancy.json", "w", encoding="utf-8") as file:
#     json.dump(json_list, file, indent=4)
# print(json_list)