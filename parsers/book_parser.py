import logging
from locators.book_locators import BookLocator

logger = logging.getLogger('scraping.book_parser')


class BookParser:

    RATINGS = {
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5
    }

    def __init__(self, book):
        logger.debug(f'New book parser created from `{book}`.')
        self.book = book

    def __repr__(self):
        return f'<Book {self.title}, {self.rating} stars, ${self.price}>'

    @property
    def title(self):
        logger.debug('Finding book name...')
        locator = BookLocator.TITLE
        title = self.book.select_one(locator).attrs['title']
        logger.debug(f'Found book name, `{title}`.')
        return title

    @property
    def link(self):
        logger.debug('Finding book link...')
        locator = BookLocator.LINK
        link = self.book.select_one(locator).attrs['href']
        logger.debug(f'Found book link, `{link}`.')
        return link

    @property
    def price(self):
        logger.debug('Finding book price...')
        locator = BookLocator.PRICE
        price_paragraph = self.book.select_one(locator)
        price = float(price_paragraph.string.replace('£', ''))
        logger.debug(f'Found book price, `{price}`.')
        return price

    @property
    def rating(self):
        logger.debug('Finding book rating...')
        locator = BookLocator.RATING
        star_rating_tag = self.book.select_one(locator)
        classes = star_rating_tag.attrs['class']
        rating_class = [r for r in classes if r != 'star-rating']
        rating_number = BookParser.RATINGS.get(rating_class[0])
        logger.debug(f'Found book rating, `{rating_number}`.')
        return rating_number
