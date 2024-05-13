import urllib
from urllib.request import urlopen
import requests
import re
import pandas as pd
from fake_useragent import UserAgent

ua = UserAgent()

headers = {
    "User-Agent": ua.random
}

pattern_site_number = r'<div class="pagination">(.*?)</div>'
pattern_text_content = r'<div class="classified__header">(.*?)</div>'
pattern_text_title = r'<h3 class="classified__title">(.*?)</h3>'
pattern_link = r'<a href="/oferta(.*?)"'

url_physical = "https://mylomza.pl/ogloszenia/praca/praca-fizyczna/dam-prace/strona1"

url_driver = "https://mylomza.pl/ogloszenia/praca/praca-kierowca/dam-prace/strona1"

url_office = "https://mylomza.pl/ogloszenia/praca/praca-biurowa/dam-prace/strona1"

url_additional = "https://mylomza.pl/ogloszenia/praca/praca-dodatkowa/dam-prace/strona1"

url_cook = "https://mylomza.pl/ogloszenia/praca/praca-w-gastronomi/dam-prace/strona1"

url_shop = "https://mylomza.pl/ogloszenia/praca/praca-w-sklepie/strona1"

url_other = "https://mylomza.pl/ogloszenia/praca/praca-pozostale/dam-prace/strona1"

url_IT = "https://mylomza.pl/ogloszenia/praca/praca-it--informatyk/strona1"

urls_list = [url_physical, url_driver, url_office, url_additional, url_cook, url_shop, url_other, url_IT]

max_number_list = []
contact_list = []
filtered_contact_list = []


def main_mylomza():
    pattern_site_number_only = r'>(\d+)\s*<'
    for urls in urls_list:
        print(urls)
        response = requests.get(urls, headers=headers, timeout=100)
        initial_html = response.text
        result = re.search(pattern_site_number, initial_html, re.DOTALL)
        content_between_divs = result.group(1)
        site_number_matches = re.findall(pattern_site_number_only, content_between_divs, re.IGNORECASE)
        numbers_int = list(map(int, site_number_matches))
        print(numbers_int)
        if numbers_int:
            max_number = max(numbers_int)
            print(max_number)
        else:
            max_number = 1
        max_number_list.append(max_number)

    for i in range(len(urls_list)):
        for n in range(max_number_list[i]):
            new_url = urls_list[i].replace("strona1", "strona" + str(n + 1))
            new_response = requests.get(new_url, headers=headers, timeout=100)
            new_html = new_response.text
            text_title_matches = re.findall(pattern_text_title, new_html, re.DOTALL)
            link_matches = re.findall(pattern_link, new_html, re.DOTALL)
            print(text_title_matches)

            prefix_links = ["https://mylomza.pl/oferta" + links for links in link_matches]
            link_list = []
            seen = set()

            for links in prefix_links:
                if links not in seen:
                    link_list.append(links)
                    seen.add(links)
                else:
                    seen.remove(links)
            contact_list.append({'Tytuł:': text_title_matches, 'Linki:': link_list})
            print(link_list)

    for m, item in enumerate(contact_list):
        print(f"Element {m} ma Tytuł: {item['Tytuł:']} i Linki: {item['Linki:']}")
        for item['Tytuł:'], item['Linki:'] in zip(item['Tytuł:'], item['Linki:']):
            filtered_contact_list.append((item['Tytuł:'], item['Linki:']))

    print(filtered_contact_list)

    df = pd.DataFrame(filtered_contact_list)
    with pd.ExcelWriter("data_base.xlsx", engine="openpyxl", mode='a', if_sheet_exists='replace') as writer:
        df.to_excel(writer, sheet_name="mylomza", index=True)
