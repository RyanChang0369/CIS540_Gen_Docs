"""
gen_docs.py

Authors: rchang
Created: 2026-10-31
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from scrapy.crawler import CrawlerProcess
from doc_gen_spider import DocGenSpider

def main() -> int:
    """
    Main entry point for execution.
    :return int: The program exit code.
    """
    process = CrawlerProcess()
    process.crawl(DocGenSpider)
    process.start()
    return 0


if __name__ == "__main__":
    sys.exit(main())
