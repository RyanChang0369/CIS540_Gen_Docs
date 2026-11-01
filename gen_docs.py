# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
gen_docs.py

Authors: rchang
Created: 2026-10-31
"""

import sys
import platformdirs
from scrapy.crawler import CrawlerProcess

import pipelines
from spiders import UMDCatalogSpider

cache_path = platformdirs.user_cache_path("gen_docs", "cis540", ensure_exists=True)


def main() -> int:
    """
    Main entry point for execution.
    :return int: The program exit code.
    """
    process = CrawlerProcess(
        settings={
            "ITEM_PIPELINES": {
                pipelines.StripHtmlPipeline: 100,
                pipelines.WriteToFilePipeline: 110,
            },
            "DOWNLOADER_MIDDLEWARES": {
                "scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware": 10
            },
            "HTTPCACHE_ENABLED": True,
            "HTTPCACHE_DIR": str(cache_path),
        }
    )
    process.crawl(UMDCatalogSpider)
    process.start()
    return 0


if __name__ == "__main__":
    sys.exit(main())
