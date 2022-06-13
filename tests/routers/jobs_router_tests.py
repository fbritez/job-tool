import unittest
from unittest import mock

from starlette import status

from src.routers.jobs_router import create_job, all_jobs, get_job, filter_jobs


class JobRouterTest(unittest.TestCase):

    def test_create_job(self):
        jobPosition = mock.Mock()
        jobPosition.get_id.return_value = 'ABCD1234'
        response = create_job(jobPosition)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(response.body.decode("UTF-8"), '{"message":"Job code: ABCD1234 was created successfully"}')

    @mock.patch('src.routers.jobs_router.service')
    def test_all_jobs(self, mock_service):
        mock_service.get_all.return_value = [1, 3, 7]

        jobs = all_jobs()

        self.assertEquals(jobs, [1, 3, 7])
        self.assertTrue(mock_service.get_all.has_called)

    @mock.patch('src.routers.jobs_router.service')
    def test_jobs_by_id(self, mock_service):
        job_id = 'ABCD1234'
        mock_job = mock.Mock()
        mock_service.get_jobs_by_id.return_value = [mock_job]

        job = get_job(job_id)

        self.assertEquals(mock_job, job)
        mock_service.get_jobs_by_id.assert_called_with(job_id)

    @mock.patch('src.routers.jobs_router.service')
    def test_jobs_by_id_job_does_not_exist(self, mock_service):
        job_id = 'ABCD1234'
        mock_service.get_jobs_by_id.return_value = []

        response = get_job(job_id)

        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEquals(response.body.decode("UTF-8"), '{"message":"Job not found. Job Id: ABCD1234"}')

    @mock.patch('src.routers.jobs_router.logging')
    @mock.patch('src.routers.jobs_router.generate_filter')
    @mock.patch('src.routers.jobs_router.service')
    def test_filter_jobs(self, mock_service, mock_generate_filter, mock_logging):
        mock_filter = mock.Mock()
        mock_generate_filter.return_value = [mock_filter]
        mock_service.filter_jobs.return_value = []

        jobs = filter_jobs(title='title', description='description', salary_min=0, salary_max=900, country='country', tags=['tags'])

        self.assertEquals(jobs, [])
        mock_generate_filter.assert_called_with('title', 'description', 0, 900, 'country', ['tags'])
        mock_service.filter_jobs.assert_called_with([mock_filter])
        mock_logging.info.assert_called_with('Preparing filter for: %s', [mock_filter])
