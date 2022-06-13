import unittest
from unittest import mock

from src.services.search_service import SearchService


class SearchServiceTests(unittest.TestCase):

    def test_initialization(self):
        sources = [mock.Mock()]
        service = SearchService(sources)

        self.assertEquals(len(service.sources), 1)