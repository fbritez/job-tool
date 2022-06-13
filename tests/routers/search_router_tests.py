import unittest
from unittest import mock

from src.routers.search_router import search_jobs, log_parameters


class SearchRouterTest(unittest.TestCase):

    @mock.patch('src.routers.search_router.log_parameters')
    @mock.patch('src.routers.search_router.logging')
    @mock.patch('src.routers.search_router.service')
    def test_search_jobs(self, mock_service, mock_logging, mock_log_parameter):
        mocked_jobs = [mock.Mock()]
        mock_service.search_jobs.return_value = mocked_jobs

        jobs = search_jobs(title='Java dev')

        mock_service.search_jobs.assert_called_with('Java dev', None, None, None, None, None)
        mock_logging.info.assert_called_with('Found Jobs: %s', mocked_jobs)
        mock_log_parameter.assert_called_with('Java dev', None, None, None, None, None)

    @mock.patch('src.routers.search_router.logging')
    def test_log_parameters(self, mock_logging):
        log_parameters('Java', 'experience 10 years', 1000, 4000, 'Mexico', ['Java', 'OOP'])
        mock_logging.info.assert_called_with('Seargh paramters: %s',
                                             " - title: Java - description: experience 10 years - salary_min: 1000 - salary_max: 4000 - country: Mexico - tags: ['Java', 'OOP']")

