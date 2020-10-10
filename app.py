import requests
import logging

from pages.books_page import BooksPage

FORMAT = '%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s'
DATE_FORMAT = '%d-%m-%Y %H:%M:%S'

logging.basicConfig(format=FORMAT, datefmt=DATE_FORMAT, level=logging.INFO, filename='logs.txt')
logger = logging.getLogger('scraping')

logger.info('Loading books list...')

books = []

page_content = requests.get('http://books.toscrape.com').content
page = BooksPage(page_content)

for page_num in range(page.page_count):
    url = f'http://books.toscrape.com/catalogue/page-{page_num+1}.html'
    page_content = requests.get(url).content
    logger.debug('Creating BooksPage from page content.')
    page = BooksPage(page_content)
    books.extend(page.books)
