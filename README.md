# Springer Free Downloader

[Springer](https://www.springer.com/) is giving near [500 books](https://link.springer.com/search?facet-content-type=%22Book%22&package=mat-covid19_textbooks&%23038;facet-language=%22En%22&%23038;sortOrder=newestFirst&%23038;showAll=true) for free, so you can learn during the quarantine due of COVID-19.

I have received this message, along with a PDF listing all the free e-books in some WhatsApp and Telegram groups.

I have downloaded manually some books, but then I thought that a Python package could help not only me, but ther people too.

I searched if someone has already made it, but only found [one in R](https://towardsdatascience.com/a-package-to-download-free-springer-books-during-covid-19-quarantine-6faaa83af13f)

So, here it is.

This package downloads the Springer books from a CSV list into a specified directory.
Each URL is an entry point for the book. Sometimes it have only a PDF, some times a PDF and an ePub. It tries to download both.

## Preparing the list of books to download

In the springer_free_downloader/lists/ there are some files:
* **list_ebooks.csv**: The file that lists all the e-books that you want to download. <=== _THIS IS THE ONE YOU NEED TO EDIT._
* *SpringerEbooks.pdf*: The original PDF received throught the grups.
* *list_ebooks_all.csv*: Extracted from the PDF
* *list_ebooks_all.ods*: If you prefer to process in LibreOffice Calc or Excel and export as CSV

So, you can copu `list_ebooks_all.csv` to `list_ebooks.csv` and then remove the lines of the books that you do not want to download (or download them all if you wish).

You need to leave the column names in place (The code looks only for the column named "OpenURL", all the other columns are only informative).

## Installing the dependencies

### Clone

Clone the code and enter the directory

```
git clone https://github.com/luiscardozo/springer_free_downloader
cd springer_free_downloader
```

### Virtual Environment and dependencies

Create a virtual environment (recommended) and install the requirements:

```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

It requires Python 3.6+ _on purpose_ (because I am using f-strings)

## Execute
(Inside the environment):

`python3 springer_downloader.py`

### Options:
-d download_dir: Where to download the files (defaults to `$HOME`/SpringerBooks )
-c csv: CSV file from where to get the URL links to download (defaults to `list/list_ebooks.csv`)

Both options are not required.

### Tested on:
* Linux (Ubuntu 19.10, Python 3.7.5)

## To Do:
* ~~Multithreading~~
* Automated Tests
* Change prints to logs

## Other things

### How did I convert from the PDF to CSV?

Using Tabula: [https://pypi.org/project/tabula-py/](https://pypi.org/project/tabula-py/)

```
import tabula
tabula.convert_into("SpringerEbooks.pdf", "list_ebooks_all.csv", output_format="csv", pages='all')
```
And then correcting some rows (the last page had some malformed rows).

### Disclaimer
I am not related in any way to Springer. The content was given "for free", AFAIK. Please visit their website [https://www.springer.com](https://www.springer.com/) to see more.