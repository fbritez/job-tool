import unittest
from unittest import mock

from src.api import get_api


class ApiTest(unittest.TestCase):

    @mock.patch('src.api.jobs')
    @mock.patch('src.api.APIRouter')
    def test_api(self, mock_router, mock_job_router):
        api_router = get_api()

        self.assertEquals(api_router, mock_router())
        api_router.include_router.assert_called_with(mock_job_router.router, prefix='/jobs')
