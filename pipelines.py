import csv
from pathlib import Path
from typing import Any

import html2text
from itemadapter import ItemAdapter
from scrapy import Item
from scrapy.exceptions import DropItem

from items import DocumentItem


class StripHtmlPipeline:
    """
    Converts HTML to Markdown for the AI to process.
    """

    def process_item(self, adapter: Any) -> Item:
        adapter = ItemAdapter(adapter)
        content = adapter.get("content")
        url = adapter.get("url")

        print("StripHtmlPipeline processing for:", url)

        if not isinstance(content, str):
            raise DropItem("Not a string")

        converter = html2text.HTML2Text()
        md_content: str = converter.handle(content)

        if len(md_content) <= 0 or md_content.isspace():
            raise DropItem("Empty or whitespace-only string")

        return DocumentItem(url=url, content=md_content)


class WriteToFilePipeline:
    """
    Writes pipelined items to a file.
    """

    __w2f_cache: dict[str, str] = {}

    def process_item(self, item: Any) -> Item:
        adapter = ItemAdapter(item)
        content = adapter.get("content")
        url = adapter.get("url")

        print("WriteToFilePipeline processing for:", url)

        if not isinstance(content, str):
            raise DropItem("Content is not a string")
        if not isinstance(url, str):
            raise DropItem("URL is not a string")

        self.__w2f_cache[url] = content

        return item

    def close_spider(self):
        with open("documents.csv", "wt") as csv_fh:
            writer = csv.DictWriter(csv_fh, fieldnames=["url", "content"])
            writer.writeheader()

            for url, content in self.__w2f_cache.items():
                writer.writerow({"url": url, "content": content})

                md_path = "./documents.d" / Path(
                    url.removeprefix("https://").strip("/")
                )
                md_path = md_path.with_suffix(".md")
                md_path.parent.mkdir(parents=True, exist_ok=True)
                md_path.write_text(content)
