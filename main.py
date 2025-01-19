import requests as req
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import math
import openpyxl
import logging

formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
logger = logging.getLogger('')
logger.setLevel(logging.DEBUG)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/91.0.4472.124 Safari/537.36'
}

def num_of_ads_and_pages(url):
    """
    This method scraps the total number of ads and calculates the total number of pages
    There are 25 ads per page (hardcoded)
    :param url:
    :return: total_ads, total_pages
    """

    total_ads, total_pages = 0, 0
    response = req.get(url, headers=headers, timeout=10)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        small_tags = soup.find_all('small')
        if small_tags:
            target_small = small_tags[4].text.strip()
            total_ads = int(target_small.split('od ukupno ')[1])
            total_pages = math.ceil(total_ads / 25)
    else:
        logger.error(f"Failed to retrieve the page. Status code: {response.status_code}")
    return total_ads, total_pages


def single_ad_info(url):
    """
    This method scraps divs that contain single ad info of significance, and returns dictionary (key-value)
    :param url:
    :return: ad_info
    """
    ad_info = {}
    try:
        response = req.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            div = soup.find('div', class_='infoBox js-tutorial-contact')
            if div:
                div2 = div.find('div', class_='uk-width-1-2')
                if div2 and div2.contents:
                    city = div2.contents[0].text.strip()
                    ad_info["Mesto"] = city

            div = soup.find('div', class_='financing')
            if div:
                price = div.find('span')
                if price:
                    price = price.text.strip().replace(" €", "").replace(".", "")
                    ad_info["Cena"] = price

            divs_to_check = [
                ('uk-width-large-1-2 uk-width-medium-1-1 uk-width-1-1', None),
                ('uk-width-medium-1-2', None),
                ('uk-width-medium-1-2 uk-width-1-1', None),
                ('uk-width-medium-1-2 uk-width-1-1', None)
            ]

            for div_class, style_value in divs_to_check:
                if style_value:
                    div = soup.find('div', class_=div_class, style=style_value)
                else:
                    div = soup.find('div', class_=div_class)

                if div:
                    info = div.find_all('div', class_='uk-width-1-2')
                    for i in range(0, len(info), 2):
                        label = info[i].text.strip().rstrip(":")
                        value = info[i + 1].text.strip() if i + 1 < len(info) else ""
                        ad_info[label] = value
        else:
            logger.error(f"Failed to retrieve ad page. Status code: {response.status_code}")
    except req.exceptions.RequestException as e:
        logger.error(f"Request failed for ad URL {url}: {e}")
    return ad_info


def all_ads_info(url, total_pages, all_ads_data):
    """
    This method performs single_ad_info iteratively for all of the ads and appends the data into one list
    :param url:
    :param total_pages:
    :param all_ads_data:
    :return:
    """
    for i in range(1, total_pages + 1):
        changed_url = f"{url}?page={i}"
        response = req.get(changed_url, headers=headers, timeout=10)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = soup.find_all('article')

            for article in articles:
                link_tag = article.find('a', href=True)
                if link_tag:
                    href = link_tag.get('href')
                    parsed_url = urlparse(href)
                    ad_path = parsed_url.path
                    ad_url = 'https://www.polovniautomobili.com' + ad_path
                    ad_data = single_ad_info(ad_url)
                    all_ads_data.append(ad_data)
                    logger.info(f"Processed ad on page {i}")
        else:
            logger.error(f"Failed to retrieve page {i}. Status code: {response.status_code}")


def write_to_excel(filename, data, columns):
    """
    This method writes scrapped data into Excel file at the end of the program
    :param filename:
    :param data:
    :param columns:
    :return:
    """
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.append(columns)

    for ad_data in data:
        row = [ad_data.get(column, "") for column in columns]
        sheet.append(row)

    wb.save(filename)


if __name__ == "__main__":
    cols = [
        "Mesto", "Cena", "Stanje", "Marka", "Model", "Godište", "Kilometraža", "Karoserija",
        "Gorivo", "Kubikaža", "Snaga motora", "Fiksna cena", "Zamena",
        "Broj oglasa", "Emisiona klasa motora", "Pogon", "Menjač",
        "Broj vrata", "Broj sedišta", "Strana volana", "Klima",
        "Boja", "Materijal enterijera", "Boja enterijera", "Registrovan do",
        "Poreklo vozila", "Oštećenje", "Zemlja uvoza"
    ]

    main_url = 'https://www.polovniautomobili.com/auto-oglasi/pretraga'
    excel_filename = "ads_data.xlsx"
    ads_data = []

    try:
        num_of_ads, num_of_pages = num_of_ads_and_pages(main_url)
        all_ads_info(main_url, num_of_pages, ads_data)
    except KeyboardInterrupt:
        logger.warning("Process interrupted by user.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        if ads_data:
            write_to_excel(excel_filename, ads_data, cols)
            logger.info(f"Data saved to {excel_filename}")
        else:
            logger.warning("No data to save.")

