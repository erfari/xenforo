from bs4 import BeautifulSoup
import requests
import pandas as pd
from tabulate import tabulate


def drug_data(base_url, page_number):
    # return "https://www.disboards.com/threads/mike-and-suzys-honeymoon-at-disney-world.1696567/page-" + str(page_number)
    return base_url + "page-" + str(page_number)


def get_pages(soup):
    page_block = soup.find_all(class_='pageNav-main')[0]
    pages = []
    for page in page_block:
        try:
            int(page.text)
            pages.append(page.text)
        except:
            continue
    return pages


def get_messages(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    users = [str(user.get('data-author')) for user in soup.css.select('article') if user.get('data-author') is not None]
    msg = [str(msg.text) for msg in soup.find_all(class_='bbWrapper')]
    result = {'user': users, 'msg': msg}
    return result


def get_data(base_url):
    # base_url = "https://www.disboards.com/threads/mike-and-suzys-honeymoon-at-disney-world.1696567/"
    page_data = requests.get(base_url)
    soup = BeautifulSoup(page_data.text, 'html.parser')
    data = pd.DataFrame()
    for i in range(1, len(get_pages(soup)) + 1):
        data = pd.concat([data, pd.DataFrame(get_messages(drug_data(base_url, i)))])
    print(tabulate(data, headers='keys'))
    data.to_csv('out.csv', index=False)


if __name__ == '__main__':
    print("Enter url for parse xenforo-forum")
    url = input()
    get_data(url)
