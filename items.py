from scrapy import Field, Item


class DocumentItem(Item):
    url = Field()
    content = Field()