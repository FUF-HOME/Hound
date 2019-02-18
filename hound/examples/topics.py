#!/usr/bin/env python
# -*-coding:utf-8-*-

from hound.spider.Item import Item
from hound.spider.Field import TextField
from hound.core.run import Spider

class HackerNewsItem(Item):
    target_item = TextField(css_select='tr.athing')
    title = TextField(css_select='a.storylink')


class HackerNewsSpider(Spider):
    start_urls = ['https://news.ycombinator.com/news?p=1']

    async def parse(self, response):
        async for item in HackerNewsItem.get_items(html=response.html):
            yield item
    async def process_item(self, item):
        print(item)

if __name__ == '__main__':
    HackerNewsSpider.start()