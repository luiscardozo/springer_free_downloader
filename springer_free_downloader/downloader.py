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
    

def try_download(soup, booktype='pdf'):
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

def download_url(url):
    doc = requests.get(url)
    doc.raise_for_status()

    soup = bs4.BeautifulSoup(doc.text, features="html.parser")
    
    try_download(soup)
    try_download(soup, 'ebook')

def from_list(csv=DEFAULT_CSV):
    df = pd.read_csv(csv)

    url_size = df['OpenURL'].size
    file_nr = 0

    start = time.perf_counter()

    for url in df['OpenURL']:
        file_nr += 1

        print(f'Downloading file #{file_nr} of {url_size}')
        download_url(url)
    
    end = time.perf_counter()
    print(f"downloaded {url_size} files in {end - start} seconds")
