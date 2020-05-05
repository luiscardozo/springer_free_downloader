import os
from argparse import ArgumentParser

from springer_free_downloader.downloader import Downloader

THIS_DIR=os.path.dirname(os.path.abspath(__file__))
DEFAULT_CSV = THIS_DIR + os.path.sep + 'lists/list_ebooks.csv'
DEFAULT_DIR = os.path.expanduser('~') + os.path.sep + 'SpringerBooks'

def build_argparser():
    """
    Parse command line arguments.

    :return: command line arguments
    """
    parser = ArgumentParser()
    parser.add_argument("-d", "--download_dir", required=False, type=str, default=DEFAULT_DIR, 
                        help="Directory where the e-books will be downloaded")
    parser.add_argument("-c", "--csv", required=False, type=str, default=DEFAULT_CSV,
                        help="Path to alternative CSV file")
    return parser


def main():
    args = build_argparser().parse_args()
    downloader = Downloader(args.download_dir, args.csv)
    downloader.from_list()

if __name__ == '__main__':
    main()
