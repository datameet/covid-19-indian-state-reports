"""Program to download covid19 reports of Karnataka.
"""
import logging
import os
from pathlib import Path
from . import helpers as h

logger = logging.getLogger(__name__)

URL = "https://karunadu.karnataka.gov.in/hfw/kannada/Pages/covid-19.aspx"
ROOT = "archive/ka"
LINK_PATTERN = r"/\d\d-\d\d-\d\d\d\d\(.*\).pdf"

def get_links():
    logger.info("finding links from %s", URL)
    return h.find_links(URL, LINK_PATTERN)

def exists(url):
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
