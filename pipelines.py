from typing import Any

import html2text
from itemadapter import ItemAdapter
from scrapy import Item
from scrapy.exceptions import DropItem

from items import DocumentItem


class StripHtmlPipeline:
    """
    Converts HTML to markdown for the AI to process.
    """
    def process_item(self, adapter: Any) -> Item:
        adapter = ItemAdapter(adapter)
        content = adapter.get("value")
        name = adapter.get("name")
        
        if not isinstance(content, str):
            raise DropItem("Not a string")
        
        converter = html2text.HTML2Text()
        content = converter.handle(content)
        
        if len(content) <= 0 or content.isspace():
            raise DropItem("Empty or whitespace-only string")
        
        return DocumentItem(value=content)


