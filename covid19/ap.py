"""Program to download covid19 reports for Andhra Pradesh.
"""
import datetime
import logging
import os
from pathlib import Path
from . import helpers as h

logger = logging.getLogger(__name__)

URL = "http://hmfw.ap.gov.in/covid_19_dailybulletins.aspx"
ROOT = "archive/ap"

def get_links():
    logger.info("finding links from %s", URL)
    links = h.find_links(URL, 'covid_19_datewisebulletins')
    for link in links:
        for pdf in h.find_links(link, '.pdf'):
            yield pdf

def exists(url):
    dt = h.extract_datetime(url)
    # already downloaded till this date
    if dt <= datetime.datetime(2020, 3, 26):
        return True
    filename = url.split("/")[-1]
    return os.path.exists(os.path.join(ROOT, filename))

def main():
    h.setup_logger()
    Path(ROOT).mkdir(parents=True, exist_ok=True)
    links = get_links()
    for link in links:
        if not exists(link):
            h.download(link, download_root=ROOT)

if __name__ == "__main__":
    main()
