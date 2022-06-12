import unittest
from unittest import mock

from src.services.job_service import JobPositionService


class JobPositionServiceTests(unittest.TestCase):

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
        service = JobPositionService()
        job_position = mock.Mock()
        job_position.get_id.return_value = '1'
        service.store(job_position)
        another_job_position = mock.Mock()
        another_job_position.get_id.return_value = '2'
        service.store(another_job_position)

        job = service.get_jobs_by_id('2')

        self.assertEquals(job, another_job_position)

    def test_get_jobs_by_id_fail(self):
        service = JobPositionService()
        job_position = mock.Mock()
        job_position.get_id.return_value = '1'
        service.store(job_position)

        jobs = service.get_jobs_by_id('2')

        self.assertEquals(jobs, [])
