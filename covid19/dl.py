"""Program to download covid19 reports of Delhi.
"""
import datetime
import logging
import os
from pathlib import Path
import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from . import helpers as h

logger = logging.getLogger(__name__)

URL = "http://health.delhigovt.nic.in/wps/wcm/connect/doit_health/Health/Home/Covid19/Health+Bulletin"
ROOT = "archive/dl"

def get_links():
    logger.info("finding links from %s", URL)
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "lxml")

    links = soup.find_all("a", string=re.compile(".*Bulletin COVID 19 Dated.*"))

    for link in links:
        filename = get_filename(link)
        yield filename, urljoin(URL, link['href'])

def get_filename(link):
    text = link.get_text()
    datestr = re.search("\d\d [^ ]* 2020", text).group()
    d = datetime.datetime.strptime(datestr, '%d %B %Y')
    return "dl-{}.pdf".format(d.date().isoformat())

def main():
    h.setup_logger()
    Path(ROOT).mkdir(parents=True, exist_ok=True)
    links = get_links()
    for filename, link in links:
        if not h.already_downloaded(link, download_root=ROOT, filename=filename):
            h.download(link, download_root=ROOT, filename=filename)
        
if __name__ == "__main__":
    main()
