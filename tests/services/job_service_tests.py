import unittest
from unittest import mock

from src.filter.filters import GreaterThanFilter, EqualsThanFilter, ContainsFilter, LessThanFilter, MultiContainsFilter
from src.services.job_service import JobPositionService


class JobPositionServiceTests(unittest.TestCase):

    def _mock_job(self, job_id, title, description, salary_min, salary_max, country, tags):
        job = mock.Mock()
        job.get_id.return_value = job_id
        job.title = title
        job.description = description
        job.salary_min = salary_min
        job.salary_max = salary_max
        job.country = country
        job.tags = tags

        return job

    def setUp(self):
        self.service = JobPositionService()
        self.job_position = self._mock_job('1', 'Java Developer', 'Searching a Java developer with experience', 1500, 3500, 'Argentina', ['SSR'])
        self.another_job_position = self._mock_job('2', 'Scala Developer', 'Developer without experience', 1000, 2500, 'Colombia', ['Jr', 'Junior'])

        self.service.store(self.job_position)
        self.service.store(self.another_job_position)

    def test_initialize_service(self):
        service = JobPositionService()

        self.assertIsNotNone(service.get_persistence_service())

    @mock.patch('src.services.job_service.logging')
    def test_store_job_position(self, mock_logger):
        service = JobPositionService()
        job_position = mock.Mock()

        service.store(job_position)

        self.assertIn(job_position, service.get_persistence_service())
        self.assertTrue(mock_logger.info.called)

    def test_get_all(self):
        service = JobPositionService()
        job_position = mock.Mock()

        service.store(job_position)
        service.store(job_position)

        self.assertEquals(len(service.get_all()), 2)

    def test_get_jobs_by_id(self):

        job = self.service.get_jobs_by_id('2')

        self.assertEquals(job, [self.another_job_position])

    def test_get_jobs_by_id_fail(self):

        jobs = self.service.get_jobs_by_id('300')

        self.assertEquals(jobs, [])

    def test_filter_jobs_by_title(self):
        filters = [ContainsFilter('title', 'Java')]
        jobs = self.service.filter_jobs(filters)

        self.assertEquals(jobs, [self.job_position])

    def test_filter_jobs_by_description(self):
        filters = [ContainsFilter('description', 'without experience')]
        jobs = self.service.filter_jobs(filters)

        self.assertEquals(jobs, [self.another_job_position])

    def test_filter_jobs_by_salary_min(self):
        filters = [GreaterThanFilter('salary_min', 1200)]
        jobs = self.service.filter_jobs(filters)

        self.assertEquals(jobs, [self.job_position])

    def test_filter_jobs_by_salary_max(self):
        filters = [LessThanFilter('salary_max', 6000)]
        jobs = self.service.filter_jobs(filters)

        self.assertEquals(jobs, [self.job_position, self.another_job_position])

    def test_filter_jobs_by_country(self):
        filters = [EqualsThanFilter('country', 'Argentina')]
        jobs = self.service.filter_jobs(filters)

        self.assertEquals(jobs, [self.job_position])

    def test_filter_jobs_by_tags(self):
        filters = [MultiContainsFilter('tags', ['Junior', 'SSR'])]
        jobs = self.service.filter_jobs(filters)

        self.assertEquals(jobs, [self.job_position, self.another_job_position])

    def test_filter_jobs_by_more_than_one_filter(self):
        filters = [LessThanFilter('salary_max', 6000),
                   EqualsThanFilter('country', 'Argentina')]
        jobs = self.service.filter_jobs(filters)

        self.assertEquals(jobs, [self.job_position])