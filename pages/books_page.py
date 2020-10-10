import re
import logging
from bs4 import BeautifulSoup

from locators.books_pages_locators import BooksPageLocator
from parsers.book_parser import BookParser

logger = logging.getLogger('scraping.books_page')


class BooksPage:
    def __init__(self, page):
        logger.debug('Parsing page content with Beautiful Soup HTML Parser.')
        self.soup = BeautifulSoup(page, 'html.parser')

    @property
    def books(self):
        logger.debug(f'Finding all books in the page using `{BooksPageLocator.BOOKS}`')
        locator = BooksPageLocator.BOOKS
        book_tags = self.soup.select(locator)
        return [BookParser(book) for book in book_tags]

    @property
    def page_count(self):
        logger.debug('Finding all number of catalogue pages available...')
        locator = BooksPageLocator.PAGER
        content = self.soup.select_one(locator).string
        logger.info(f'Found number of catalogue pages available: `{content}`.')
        pattern = 'Page [0-9]+ of ([0-9]+)'
        matcher = re.search(pattern, content)
        pages = int(matcher.group(1))
        logger.debug(f'Extracted number of pages as integer: `{pages}`.')
        return pages
