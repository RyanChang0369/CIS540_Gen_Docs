"""
spiders.py

Authors: rchang
Created: 2026-10-31
"""
from typing import Any, Iterable

from scrapy import Item
from scrapy.http import Response
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from items import DocumentItem


class UMDCatalogSpider(CrawlSpider):
    name = "catalog.umd.umich.edu"
    allowed_domains = ["catalog.umd.umich.edu"]
    start_urls = ["https://catalog.umd.umich.edu/"]

    rules = (
        Rule(LinkExtractor(allow=r"academic-policies-\w+/$"), follow=True),
        Rule(LinkExtractor(allow=r"academic-policies-\w+/.+$"), callback="parse_item"),
    )

    def parse_item(self, response: Response) -> Item:
        return DocumentItem(url=response.url, content=str(response.css("main#contentarea")[0]))
