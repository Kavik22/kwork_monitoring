from bs4 import BeautifulSoup
from fake_useragent import FakeUserAgent
from selenium import webdriver


def get_answer(data: dict, numbers):
    keywords = data['keywords']
    mode = data['mode']
    pages_count = data['pages_count']

    if mode == 'Одноразовый':
        if pages_count == 'Все':
            tenders, new_numbers = get_data(keywords=keywords, number_last_page='Last', numbers=[])
        else:
            tenders, new_numbers = get_data(keywords=keywords, number_last_page=pages_count, numbers=[])
    else:
        tenders, new_numbers = get_data(keywords=keywords, number_last_page=1, numbers=numbers)

    if not tenders:
        return False, False

    answer = ''
    print(tenders)
    for tender in tenders:
        answer += f'''<b><u><a href="{tender['link']}">{tender['name']}</a></u></b>\n{tender['text']}\n{tender['price']}. {tender['offers']}\n*******************************************\n'''
    return answer, new_numbers


def get_data(keywords, number_last_page, numbers):
    options = webdriver.FirefoxOptions()
    options.add_argument(f'user-agent={FakeUserAgent().random}')
    options.add_argument('accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8')
    options.add_argument('--headless')
    driver = webdriver.Firefox(options=options)

    try:
        driver.get(url='https://kwork.ru/projects?c=11&page=1')
        driver.implicitly_wait(5)

        result = []

        soup = BeautifulSoup(driver.page_source, 'lxml')

        if number_last_page == 'Last':
            number_last_page = int(soup.find('div', class_='paging').find_all('li')[-2].text)

        new_numbers = []

        for number_page in range(1, number_last_page + 1):
            url = f'https://kwork.ru/projects?c=11&page={str(number_page)}'
            driver.get(url)
            driver.implicitly_wait(5)
            soup = BeautifulSoup(driver.page_source, 'lxml')
            tenders = soup.find_all('div', class_='card__content pb5')
            for tender in tenders:
                header = tender.find('div', class_='wants-card__left')
                try:
                    name = header.find('a').text
                except:
                    continue

                flag = True
                for keyword in keywords:
                    if keyword in name.lower():
                        flag = False
                        break
                if flag:
                    continue

                try:
                    text = header.find('div', class_='d-inline breakwords first-letter').text
                except:
                    text = 'Нет описания'
                try:
                    price_min = tender.find('div',
                                            class_='wants-card__header-price wants-card__price m-hidden').text.replace(
                        '\xa0', '')
                except:
                    price_min = 'Нет цены'
                link = 'https://kwork.ru' + header.find('a').get('href')

                number = link.split('/')[-1]
                new_numbers.append(number)
                if number in numbers:
                    continue

                try:
                    offers = tender.find('div', class_='force-font force-font--s12 mr8').find_all('span')[-1].text
                except:
                    offers = 'Нет предложений'
                result.append(
                    {
                        'name': name,
                        'text': text,
                        'price': price_min,
                        'link': link,
                        'offers': offers
                    }
                )
        return result, new_numbers

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()
