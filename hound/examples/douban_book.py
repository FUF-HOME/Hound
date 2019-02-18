#!/usr/bin/env python
# -*-coding:utf-8-*-
from hound.core.run import Spider
from hound.spider.Field import TextField,AttrField
from hound.spider.Item import Item
import aiofiles

class DoubanItem(Item):
    target_item = TextField(css_select='tr.item')
    title = TextField(css_select='div.pl2>a')
    # cover = AttrField(css_select='div.pic>a>img', attr='src')
    abstract = TextField(css_select='span.inq')

    async def clean_title(self, title):
        if isinstance(title, str):
            return title
        else:
            return ''.join([i.text.strip().replace('\xa0', '') for i in title])


class DoubanSpider(Spider):
    start_urls = ['https://book.douban.com/top250?start']
    request_config = {
        'RETRIES': 3,
        'DELAY': 0,
        'TIMEOUT': 20
    }
    concurrency = 10
    # proxy config
    # kwargs = {"proxy": "http://0.0.0.0:1087"}
    kwargs = {}

    async def parse(self, response):
        etree = response.html_etree
        pages = ['https://book.douban.com/top250?start=0'] + [i.get('href') for i in etree.cssselect('.paginator>a')]
        for index, page in enumerate(pages):
            url = page
            yield self.request(
                url=url,
                metadata={'index': index},
                callback=self.parse_item
            )

    async def parse_item(self, response):
        async for item in DoubanItem.get_items(html=response.html):
            yield item

    async def process_item(self, item: DoubanItem):

        async with aiofiles.open('./doubanbook.txt', 'a',encoding='UTF-8') as f:
            await f.write(str(item.title)+":"+str(item.abstract) + '\n')


if __name__ == '__main__':
    DoubanSpider.start()