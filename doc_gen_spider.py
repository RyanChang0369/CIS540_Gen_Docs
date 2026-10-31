from requests import Response
from scrapy import Request, Spider

from response_handler import response_handler_chain


class DocGenSpider(Spider):
    name = "doc_gen"
    start_urls = ["https://catalog.umd.umich.edu/academic-policies-graduate/"]

    # async def start(self):
    #     print("Starting")
    #     yield Request(
    #         "https://catalog.umd.umich.edu/academic-policies-graduate/"
    #     )

    def parse(self, response: Response):
        for handler in response_handler_chain():
            result = handler.handle_response(response)
            print(f"Trying response handler '{type(result)}' ... ", end=None)

            if result is not None:
                # Found the correct handler.
                print(f"Success (result = {result})")
                return result

            print("Failed")
        return None
