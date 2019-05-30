# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from urllib.request import urlopen
from ..items import QuoteSpiderItem

class BookScrapeSpider(scrapy.Spider):
    name = 'book_scrape'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/catalogue/page-1.html']
    page_no = 1
    next_page = 'http://books.toscrape.com/catalogue/page-' + str(page_no) + '.html'

    def parse(self, response):
        items = QuoteSpiderItem()
        html = urlopen(BookScrapeSpider.next_page)
        url_string = 'http://books.toscrape.com/catalogue/'
        html_obj = BeautifulSoup(html.read(), 'html.parser')

        for i in response.css('.price_color::text').extract():
            string = str(i)
            price = string.replace("£", " ")
            price = float(price)
            limit = 35.00

            if price < limit:
                title = html_obj.find("p", string=i).parent.find_previous_sibling('h3').find('a')['title']
                link = html_obj.find("p", string=i).parent.find_previous_sibling('h3').find('a')['href']
                amount = price

                yield {
                    'title': title,
                    'cost': amount,
                    'link': url_string + link

                }

        if BookScrapeSpider.page_no <= 50:
            print("page info", BookScrapeSpider.page_no)
            BookScrapeSpider.page_no += 1
            BookScrapeSpider.next_page = 'http://books.toscrape.com/catalogue/page-' + str(
                BookScrapeSpider.page_no) + '.html'
            yield response.follow(BookScrapeSpider.next_page, callback=self.parse)
