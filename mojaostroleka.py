import urllib
from urllib.request import urlopen
import requests
import re
import pandas as pd
from fake_useragent import UserAgent
import time

ua = UserAgent()

headers = {
    "User-Agent": ua.random
}

url = "https://ogloszenia.moja-ostroleka.pl/dam-prace,9,1.html"

response = requests.get(url, headers=headers, timeout=100)
initial_html = response.text

pattern_site_number = r'>(\d+)<'
site_number_matches = re.findall(pattern_site_number, initial_html, re.IGNORECASE)

numbers_int = list(map(int, site_number_matches))
max_number = max(numbers_int)
print(max_number)

pattern_even = r'<div class="row premium even">\s*<a\s+href="([^"]+)".*?title="([^"]+)">'
pattern_odd = r'<div class="row premium odd">\s*<a\s+href="([^"]+)".*?title="([^"]+)">'
pattern_megaeven = r'<div class="row mega_promo even">\s*<a\s+href="([^"]+)".*?title="([^"]+)">'
pattern_megaodd = r'<div class="row mega_promo odd">\s*<a\s+href="([^"]+)".*?title="([^"]+)">'
pattern_rowzwykleodd = r'<div class="row zwykle odd">\s*<a\s+href="([^"]+)".*?title="([^"]+)">'
pattern_rowzwykleeven = r'<div class="row zwykle even">\s*<a\s+href="([^"]+)".*?title="([^"]+)">'
pattern_toread = re.compile(r'<span id="intertext1">\s*(.*?)\s*</span>', re.DOTALL)

links_list = []
links_combined_data = []


def link_loop(link, title):
    max_retries = 3
    delay = 150
    cleaned_text = ""
    for retries in range(max_retries):
        try:
            req = urllib.request.Request(url=link, headers=headers)
            data_toread = urlopen(req, timeout=100)
            data_toread_html = data_toread.read().decode("utf-8")
            match = pattern_toread.search(data_toread_html)
            print(link)
            if match:
                content = match.group(1)
                cleaned_text = re.sub(r'<[/]?b>|<br[/]?>|<[/]?strong>|<[/]?center>|<[/]?(.*?)[/]?>', '', content)
                print(cleaned_text)
            if not match:
                cleaned_text = ""
            links_list.append({"Tytuł": title, "Link": link, "Tekst": cleaned_text})
            break
        except urllib.error.URLError as e:
            print("mojaostroleka connection error, retry ", e)
            time.sleep(delay)
            delay *= 2


def main_mojaostroleka():
    links_combined_data = ""
    for i in range(max_number):

        new_url = url.replace("9,1", "9," + str(i))
        new_page = urlopen(new_url)
        new_html = new_page.read().decode("utf-8")
        matches_odd = re.findall(pattern_even, new_html)
        matches_even = re.findall(pattern_odd, new_html)
        matches_megaodd = re.findall(pattern_megaodd, new_html)
        matches_megaeven = re.findall(pattern_megaeven, new_html)
        matches_zwykleodd = re.findall(pattern_rowzwykleodd, new_html)
        matches_zwykleeven = re.findall(pattern_rowzwykleeven, new_html)

        for link, title in matches_odd:
            link_loop(link, title)

        for link, title in matches_even:
            link_loop(link, title)

        for link, title in matches_megaodd:
            link_loop(link, title)

        for link, title in matches_megaeven:
            link_loop(link, title)

        for link, title in matches_megaeven:
            link_loop(link, title)

        for link, title in matches_zwykleodd:
            link_loop(link, title)

        for link, title in matches_zwykleeven:
            link_loop(link, title)

        links_combined_data = [{"Tytuł:": item["Tytuł"], "Link:": item["Link"], "Tekst:": item["Tekst"]} for item in
                               links_list]
        print(new_url)

    df = pd.DataFrame(links_combined_data)
    with pd.ExcelWriter("data_base.xlsx", engine="openpyxl", mode='a', if_sheet_exists='replace') as writer:
        df.to_excel(writer, sheet_name="Moja_ostroleka", index=True)



