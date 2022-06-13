import unittest
from unittest import mock

from src.services.search_service import SearchService, ExternalSource


class SearchServiceTests(unittest.TestCase):

    def test_initialization(self):
        sources = [mock.Mock()]
        service = SearchService(sources)

        self.assertEquals(len(service.sources), 1)

    def test_service_get_data_from_different_sources(self):
        mock_job = mock.Mock()
        mock_job_2 = mock.Mock()

        mock_external_source = mock.Mock()
        mock_source = mock.Mock()

        mock_external_source.search_jobs.return_value = [mock_job]
        mock_source.search_jobs.return_value = [mock_job_2]

        sources = [mock_external_source, mock_source]
        service = SearchService(sources)

        jobs = service.search_jobs('title', 'description', 2000, 3000, 'Colombia', [])

        self.assertEquals(jobs, [mock_job, mock_job_2])
        mock_external_source.search_jobs.assert_called_with(title='title', description='description', salary_min=2000, salary_max=3000, country='Colombia', tags=[])
        mock_source.search_jobs.assert_called_with(title='title', description='description', salary_min=2000, salary_max=3000, country='Colombia', tags=[])


class ExternalSourceTests(unittest.TestCase):

    def test_initialization(self):
        f = lambda x: x
        source = ExternalSource(source_url='xxx.xxx.xxxx',
                                search_field_mapping={'title': 'name'},
                                field_to_object_function=f)

        self.assertEquals(source.source_url, 'xxx.xxx.xxxx')
        self.assertEquals(source.search_field_mapping, {'title': 'name'})
        self.assertEquals(source.field_to_object_function, f)

    @mock.patch('src.services.search_service.requests')
    def test_search_jobs(self, mock_requests):
        field_to_object_function = mock.Mock()
        source = ExternalSource(source_url='xxx.xxx.xxxx',
                                search_field_mapping={'title': 'name'},
                                field_to_object_function=field_to_object_function)
        mock_response = mock.Mock()
        mock_requests.get.return_value = mock_response

        mock_response.ok = True
        mock_response.json.return_value = [["Jr Java Developer", 24000, "Argentina", ["Java","OOP"]],
                                              ["Java Engineer", 24000, "Mexico", ["Java"]]]

        results = source.search_jobs(title='Java')

        self.assertEquals(len(results), 2)

        mock_requests.get_assert_Called_with('xxx.xxx.xxxx?name=Java')
        calls = [mock.call(["Jr Java Developer", 24000, "Argentina", ["Java","OOP"]]),
                 mock.call(["Java Engineer", 24000, "Mexico", ["Java"]])]

        field_to_object_function.assert_has_calls(calls)


