from abc import ABC, abstractmethod
from typing import Any, Generator, Iterable

from requests import Response
from scrapy import Request
from scrapy.http import TextResponse

from items import DocumentItem


def response_handler_chain() -> Generator[ResponseHandler]:

    """
    Generates the `ResponseHandler`s that are used to handle the response.
    :return Generator[ResponseHandler]: The response handlers.
    """
    yield UmdGraduatePoliciesHandler()


class ResponseHandler(ABC):
    @abstractmethod
    def handle_response(
        self, response: Response
    ) -> Any | Request | Iterable[Request] | None:
        """
        Attempts to handle a response, returning a request (or series of
        requests) or the document contents.

        :param Response response: The response to handle.
        :return str | None: The contents of the document, a request(s) to
            fulfill, or None if the handler cannot handle the `response`.
        """
        pass


class UmdGraduatePoliciesHandler(ResponseHandler):
    def handle_response(
        self, response: Response
    ) -> Any | Request | Iterable[Request] | None:

        if not isinstance(response, TextResponse):
            return None
        if not response.url.startswith("https://catalog.umd.umich.edu/"):
            return None

        if response.url.endswith("academic-policies-graduate/"):
            # Handle landing page
            links = (
                response.selector.css("main#contentarea div#textcontainer p a")
                .xpath("@href")
                .getall()
            )

            return (Request(l) for l in links)
        else:
            # Handle content page
            content = response.selector.css("main#contentarea").get()
            return DocumentItem(value=content)
