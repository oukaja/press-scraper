# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from scrapy import Spider
from pressscraper.items import ArticleItem
from scrapy.http import Request
from bidi.algorithm import get_display
import arabic_reshaper
from urllib.parse import urlparse
import simplejson as json
import os
import re


class AppSpider(Spider):
    name = 'app'
    start_urls = []
    data = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sites.json')))
    for url in open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "start_url.txt"), 'r'):
        start_urls.append(url.replace("\n", ""))

    @staticmethod
    def cleanhtml(raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        # s = re.sub(r'[^\w\s]', '', cleantext)
        s = cleantext.replace("\\", "").replace("\"", "")
        return s.strip().rstrip().lstrip().replace("\n", " ")

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        dn = self.data[str(urlparse(response.url).hostname).split('.')[-2]]
        slidespath = dn["slid"]
        urls = response.xpath(slidespath).extract()
        for url in urls:
            req = Request(response.urljoin(url), callback=self.parse_links, dont_filter=True)
            req.meta["dn"] = dn
            yield req

    def parse_links(self, response):
        dn = response.meta['dn']
        item = ArticleItem()
        item["journal"] = str(urlparse(response.url).hostname).split('.')[-2]
        item["title"] = get_display(
            arabic_reshaper.reshape(u'' + self.cleanhtml(response.xpath(dn["article"]["titre"]).extract_first())))
        item["author"] = get_display(
            arabic_reshaper.reshape(u'' + self.cleanhtml(response.xpath(dn["article"]["author"]).extract_first())))
        item["photo"] = response.xpath(dn["article"]["photo"]).extract_first()
        item["link"] = response.urljoin('')
        yield item
