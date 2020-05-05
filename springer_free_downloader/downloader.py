import time
import os
import threading

import requests
import bs4
import pandas as pd

BASE_URL = 'https://link.springer.com'
PDF_CLASS='test-bookpdf-link'
EBOOK_CLASS='test-bookepub-link'

class Downloader():

    def __init__(self, download_dir, csv_file, use_threads, max_threads):
        self._download_dir = download_dir
        self._csv_file = csv_file
        self._use_threads = use_threads
        self._sem_limit_download = threading.Semaphore(max_threads)

        os.makedirs(self._download_dir , exist_ok=True)
    
    def download_book(self, url):
        """
        Download specific book (PDF or ePub) in *dirname*
        """
        book_url = BASE_URL + url
        print('Book URL: ', book_url)

        res = requests.get(book_url)
        res.raise_for_status()

        try:
            #Try to get the filename from the HTTP headers
            file_name = os.path.join(self._download_dir,
                                     res.headers['content-disposition'].split('=')[1])
        except:
            # if not, name it as the URL
            file_name = os.path.join(self._download_dir, os.path.basename(url))

        print(f"Saving to {file_name}")

        with open(file_name,'wb') as book_file:
            for chunk in res.iter_content(100000):
                book_file.write(chunk)
        

    def get_ebook_url(self, soup, booktype='pdf'):
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
            self.download_book(ref)

    def parse_page(self, url):
        """
        Searchs for links to download the eBooks (PDF and ePub)
        """
        doc = requests.get(url)
        doc.raise_for_status()

        soup = bs4.BeautifulSoup(doc.text, features="html.parser")
        
        self.get_ebook_url(soup)
        self.get_ebook_url(soup, 'ebook')

    def from_list(self):
        """
        Reads the list of eBook URLs from CSV file and downloads
        them all.
        """
        df = pd.read_csv(self._csv_file)

        url_size = df['OpenURL'].size
        file_nr = 0

        start = time.perf_counter()

        threads = []
        for url in df['OpenURL']:
            if self._use_threads:
                with self._sem_limit_download:  #limit the downloading threads
                    t = threading.Thread(target=self.parse_page, args=(url,))
                    t.start()
                    threads.append(t)
            else:
                file_nr += 1
                print(f'Downloading file #{file_nr} of {url_size}')
                self.parse_page(url)
        
        for t in threads:
            t.join()
        
        end = time.perf_counter()
        print(f"downloaded {url_size} files in {end - start} seconds")
