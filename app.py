import requests
import logging
import aiohttp
import asyncio
import async_timeout

from pages.books_page import BooksPage

FORMAT = '%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s'
DATE_FORMAT = '%d-%m-%Y %H:%M:%S'

logging.basicConfig(format=FORMAT, datefmt=DATE_FORMAT, level=logging.INFO, filename='logs.txt')
logger = logging.getLogger('scraping')

logger.info('Loading books list...')


async def fetch_page(session, url):
    async with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.text()

 
async def get_multiple_pages(loop, *urls):
    tasks = []
    async with aiohttp.ClientSession(loop=loop) as session:
        for url in urls:
            tasks.append(fetch_page(session, url))
        grouped_tasks = asyncio.gather(*tasks)
        return await grouped_tasks


books = []

page_content = requests.get('http://books.toscrape.com').content
page = BooksPage(page_content)

urls = [f'http://books.toscrape.com/catalogue/page-{page_num + 1}.html' for page_num in range(page.page_count)]

loop = asyncio.get_event_loop()

pages = loop.run_until_complete(get_multiple_pages(loop, *urls))


for page_content in pages:
    logger.debug('Creating BooksPage from page content.')
    page = BooksPage(page_content)
    books.extend(page.books)
