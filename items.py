from scrapy import Field, Item


class DocumentItem(Item):
    name = Field()
    content = Field()