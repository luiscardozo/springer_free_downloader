import time
import os

import requests
import bs4
import pandas as pd

DEFAULT_CSV = os.path.dirname(__file__) + '/lists/list_ebooks.csv'
DEFAULT_DIR = os.path.expanduser('~') + os.path.sep + 'SpringerBooks'

BASE_URL = 'https://link.springer.com'
PDF_CLASS='test-bookpdf-link'
EBOOK_CLASS='test-bookepub-link'


def download_book(url, dirname=DEFAULT_DIR):
    """
    Download specific book (PDF or ePub) in *dirname*
    """
    os.makedirs(dirname, exist_ok=True)

    book_url = BASE_URL + url
    print('Book URL: ', book_url)

    res = requests.get(book_url)
    res.raise_for_status()

    try:
        file_name = os.path.join(dirname,res.headers['content-disposition'].split('=')[1])
    except:
        file_name = os.path.join(dirname, os.path.basename(url))

    print(f"Guardando a {file_name}")

    with open(file_name,'wb') as book_file:
        for chunk in res.iter_content(100000):
            book_file.write(chunk)
    

def get_ebook_url(soup, booktype='pdf'):
    """
    Select the link for the booktype (pdf or ebook) and downloads it.
    """

    if booktype == 'pdf':
        klass = PDF_CLASS
    else:
        klass = EBOOK_CLASS

    downBook = soup.select(f'a.{klass}')
    if downBook == []:
        print(f'It seems to be no {booktype} book to download')
    else:
        ref = downBook[0].get('href')
        download_book(ref)

def parse_page(url):
    """
    Searchs for links to download the eBooks (PDF and ePub)
    """
    doc = requests.get(url)
    doc.raise_for_status()

    soup = bs4.BeautifulSoup(doc.text, features="html.parser")
    
    get_ebook_url(soup)
    get_ebook_url(soup, 'ebook')

def from_list(csv=DEFAULT_CSV):
    """
    Reads the list of eBook URLs from CSV file and downloads
    them all.
    """
    df = pd.read_csv(csv)

    url_size = df['OpenURL'].size
    file_nr = 0

    start = time.perf_counter()

    for url in df['OpenURL']:
        file_nr += 1

        print(f'Downloading file #{file_nr} of {url_size}')
        parse_page(url)
    
    end = time.perf_counter()
    print(f"downloaded {url_size} files in {end - start} seconds")
