# Lomza_web_scrapper

## A tool for scraping jobs offers in Łomża, Ostrołęka and Zambrów

The automation process of crawling through job offers posted on MyLomza.pl, 4Lomza.pl, mojaostroleka.pl and zambrow.org.
Job offers are presented in a data_base.xlsx file.

### Requirements

git

Python 3.12

Pip3

fake_useragent

pandas

Requests


### Installation

Clone the git repository:

```bash
git clone https://github.com/sailor-elite/Lomza_job_offers_web_scrapper && cd Lomza_job_offers_web_scrapper
cp -nv .venv.sample .venv  # copy and update the env variables
```

Install necessary dependencies:

```bash
pip install -U -r requirements.txt
```

### Usage

To scrap data run main.py:

```bash
python main.py
```


