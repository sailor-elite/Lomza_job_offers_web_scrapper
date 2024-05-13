from urllib.request import urlopen
import re
import pandas as pd


def main_fourlomza():
    url = "https://www.4lomza.pl/ogl2.php?co=pokaz&k=4&t=&s=0"
    initial_page = urlopen(url)
    initial_html = initial_page.read().decode("utf-8")
    contact_list = []
    normal_text_content_list = []
    filtered_normal_text_content_list = []
    filtered_contact_list = []

    pattern_site_number = r'>(\d+)<'
    site_number_matches = re.findall(pattern_site_number, initial_html, re.IGNORECASE)
    numbers_int = list(map(int, site_number_matches))
    max_number = max(numbers_int)

    for i in range(max_number):
        phone = 0
        email = 0
        new_url = url.replace("s=0", "s=" + str(i))
        page = urlopen(new_url)
        html = page.read().decode("utf-8")
        pattern_text_content = "<div class='oglli1'>.*?<br />"
        pattern_supertext_content = "<div class='oglli5'>.*?<br />"
        pattern_mediumtext_content = "<div class='oglli4'>.*?<br />"
        pattern_data = "<div class='oglli1'>.*?</div>"
        pattern_data_oglli5 = "<div class='oglli5'>.*?</div>"
        pattern_data_oglli4 = "<div class='oglli4'>.*?</div>"

        text_content_matches = re.findall(pattern_text_content, html, re.IGNORECASE)
        pattern_data_matches = re.findall(pattern_data, html, re.IGNORECASE)
        pattern_mediumtext_matches = re.findall(pattern_mediumtext_content, html, re.IGNORECASE)
        pattern_supertext_matches = re.findall(pattern_supertext_content, html, re.IGNORECASE)
        pattern_data_oglli5_matches = re.findall(pattern_data_oglli5, html, re.IGNORECASE)
        pattern_data_oglli4_matches = re.findall(pattern_data_oglli4, html, re.IGNORECASE)

        for match in pattern_mediumtext_matches:
            pattern_mediumtext_content = re.sub("<.*?>", "", match)
            normal_text_content_list.append({'Tekst:': pattern_mediumtext_content})

        for match in pattern_data_oglli4_matches:

            pattern_data_oglli4 = re.sub("<.*?>", "", match)
            match_phone = re.search(r'telefon: (\d+)', pattern_data_oglli4)
            match_email = re.search(r'e-mail: (\S+)', pattern_data_oglli4)
            if match_phone:
                phone = match_phone.group(1)
            elif not match_phone:
                phone = None
            if match_email:
                email = match_email.group(1)
            elif not match_email:
                email = None
            contact_list.append({'Telefon:': phone, 'Email:': email})

        for match in text_content_matches:
            pattern_text_content = re.sub("<.*?>", "", match)
            normal_text_content_list.append({'Tekst:': pattern_text_content})

        for match in pattern_data_matches:

            pattern_data = re.sub("<.*?>", "", match)
            match_phone = re.search(r'telefon: (\d+)', pattern_data)
            match_email = re.search(r'e-mail: (\S+)', pattern_data)
            if match_phone:
                phone = match_phone.group(1)
            elif not match_phone:
                phone = None
            if match_email:
                email = match_email.group(1)
            elif not match_email:
                email = None
            contact_list.append({'Telefon:': phone, 'Email:': email})

        for match in pattern_supertext_matches:
            pattern_supertext_content = re.sub("<.*?>", "", match)
            normal_text_content_list.append({'Tekst:': pattern_supertext_content})

        for match in pattern_data_oglli5_matches:
            pattern_data_oglli5 = re.sub("<.*?>", "", match)
            match_phone = re.search(r'telefon: (\d+)', pattern_data_oglli5)
            match_email = re.search(r'e-mail: (\S+)', pattern_data_oglli5)
            if match_phone:
                phone = match_phone.group(1)
            elif not match_phone:
                phone = None
            if match_email:
                email = match_email.group(1)
            elif not match_email:
                email = None
            contact_list.append({'Telefon:': phone, 'Email:': email})

    for n, item in enumerate(normal_text_content_list):
        job_filter = re.search(r'szuka pracy', item['Tekst:'], flags=re.IGNORECASE)
        job_filter2 = re.search(r'szukam pracy', item['Tekst:'], flags=re.IGNORECASE)
        job_filter3 = re.search(r'poszukują pracy', item['Tekst:'], flags=re.IGNORECASE)
        job_filter4 = re.search(r'podejmie', item['Tekst:'], flags=re.IGNORECASE)
        job_filter5 = re.search(r'zatrudnię się', item['Tekst:'], flags=re.IGNORECASE)
        job_filter6 = re.search(r'poszukuje pracy', item['Tekst:'], flags=re.IGNORECASE)
        job_filter7 = re.search(r'poszukuję pracy', item['Tekst:'], flags=re.IGNORECASE)
        job_filter8 = re.search(r'wywalę', item['Tekst:'], flags=re.IGNORECASE)
        job_filter9 = re.search(r'zaopiekuję się', item['Tekst:'], flags=re.IGNORECASE)
        job_filter10 = re.search(r'szukam zlecenia', item['Tekst:'], flags=re.IGNORECASE)
        job_filter11 = re.search(r'szuka stażu', item['Tekst:'], flags=re.IGNORECASE)
        job_filter12 = re.search(r'szukam stażu', item['Tekst:'], flags=re.IGNORECASE)
        job_filter13 = re.search(r'szuka dodatkowej', item['Tekst:'], flags=re.IGNORECASE)
        job_filter14 = re.search(r'posprzątam', item['Tekst:'], flags=re.IGNORECASE)

        if not (
                job_filter or job_filter2 or job_filter3 or job_filter4 or job_filter5 or job_filter6 or job_filter7 or job_filter8 or job_filter9
                or job_filter10 or job_filter11 or job_filter12 or job_filter13 or job_filter14):
            filtered_normal_text_content_list.append(item)
            filtered_contact_list.append(contact_list[n])

    combined_4lomza_list = zip(filtered_normal_text_content_list, filtered_contact_list)

    combined_data = [{"Tekst:": item1["Tekst:"], "Telefon:": item2["Telefon:"], "Email:": item2["Email:"]} for
                     item1, item2 in combined_4lomza_list]

    for m, item in enumerate(combined_data):
        print(
            f"Element {m} ma telefon: {item['Telefon:']} i email: {item['Email:']} oraz zawartość tekstu {item['Tekst:']}")

    df = pd.DataFrame(combined_data)
    with pd.ExcelWriter("data_base.xlsx", engine="openpyxl", mode='a', if_sheet_exists='replace') as writer:
        df.to_excel(writer, sheet_name="4lomza", index=True)
