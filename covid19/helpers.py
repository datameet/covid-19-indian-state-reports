import datetime
import logging
from pathlib import Path
import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

def find_links(url, link_pattern):
    """Finds all the links in webpage specified by the URL matching the link_pattern, a regular expression.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    re_link = re.compile(link_pattern)
    return [urljoin(url, a['href']) 
        for a in soup.select("a") 
        if a.get("href") and re_link.search(a['href'])]

DATETIME_PATTERNS = [
    re.compile(r"(?P<year>20\d\d)-(?P<month>\d\d)-(?P<day>\d\d)-(?P<hour>\d\d)(?P<minute>\d\d)hrs"),
    re.compile(r"(?P<day>\d\d)-(?P<month>\d\d)-(?P<year>20\d\d)")
]

def extract_datetime(filename: str) -> datetime.datetime:
    """Extracts datetime from the URL.
    """
    for d in DATETIME_PATTERNS:
        m = d.search(filename)
        if m:
            groups = m.groupdict()
            return _prepare_datetime(groups)

def _prepare_datetime(groups):
    y = int(groups['year'])
    m = int(groups['month'])
    d = int(groups['day'])

    date = datetime.date(y, m, d)

    hour = 0
    minute = 0
    if 'hour' in groups:
        hour = int(groups['hour'])
    if 'minute' in groups:
        minute = int(groups['hour'])

    return datetime.datetime(y, m, d, hour, minute)

def download(url, download_root, filename=None):
    filename = filename or url_to_filename(url)
    path = Path(download_root) / filename

    logger.info("download: %s -> %s", url, path)
    content = requests.get(url).content
    path.write_bytes(content)

def url_to_filename(url):
    """Converts URL to filename.
    """
    scheme, netloc, path, query, fragment = urllib.parse.urlsplit    
    return path.split("/")[-1]

def already_downloaded(url, download_root, filename=None):
    filename = filename or url_to_filename(url)
    path = Path(download_root) / filename
    return path.exists()

def setup_logger():
    logging.basicConfig(
        level="INFO",
        format='[%(asctime)s] %(message)s',
        datefmt='%H:%M:%S')
