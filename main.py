import urllib
from urllib.request import urlopen
import requests
import re
import pandas as pd
from fake_useragent import UserAgent
import time
import mojaostroleka
import fourlomza
import mylomza
import zambrow

max_retries = 3

if __name__ == "__main__":
    for retries in range(max_retries):
        try:
            fourlomza.main_fourlomza()
            break
        except OSError as e:
            print("4lomza error, retry", e)
    for retries in range(max_retries):
        try:
            mylomza.main_mylomza()
            break
        except OSError as e:
            print("mylomza error, retry", e)
    for retries in range(max_retries):
        try:
            zambrow.mainzambrow()
            break
        except OSError as e:
            print("myzambrow error, retry", e)
    for retries in range(max_retries):
        try:
            mojaostroleka.main_mojaostroleka()
            break
        except OSError as e:
            print("mojaostroleka error, retry", e)
