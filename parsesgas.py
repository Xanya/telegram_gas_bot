import requests
from bs4 import BeautifulSoup


URL = 'https://auto.ria.com/uk/toplivo/ivano-frankovsk/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 OPR/69.0.3686.77'}
HOST = 'https://auto.ria.com/uk/toplivo/ivano-frankovsk'


def get_html(url):
    r = requests.get(url, headers=HEADERS)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find('table', class_='refuel table fuel-table-region azs h').find_all('tr')[1:]
    
    gas = []
    
    for item in items:
        gas.append({
            'a-95+': item.find('td', class_='a95p').text.strip(),
            'a-95': item.find('td', class_='a95').text.strip(),
            'a-92': item.find('td', class_='a92').text.strip(),
            'дп': item.find('td', class_='dt').text.strip(),
            'газ': item.find('td', class_='gaz').text.strip(),
            #'price': item.find_all('div', class_='t-cell')[1].text
        })

    return(gas)


def main():
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.text)
    else:
        print('Error')


if __name__ == "__main__":
    main()