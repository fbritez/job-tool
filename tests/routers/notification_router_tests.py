import unittest
from unittest import mock

from starlette import status

from src.routers.notification_router import new_subscribe, all_subscriptions, notify_new_job


class NotificationRouterTest(unittest.TestCase):

    @mock.patch('src.routers.notification_router.service')
    def test_new_subscribe(self, mock_service):
        subscription = mock.Mock()
        subscription.dict.return_value = {
            'email': 'prueba@prueba.com',
            'title': 'title'
        }

        response = new_subscribe(subscription)

        mock_service.new_subscription.assert_called()
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(response.body.decode("UTF-8"), '{"message":"Subscription successful"}')

    @mock.patch('src.routers.notification_router.service')
    def test_all_subscriptions(self, mock_service):
        expected_subscriptions = [mock.Mock()]
        mock_service.get_all.return_value = expected_subscriptions
        subscription = mock.Mock()
        subscription.dict.return_value = {
            'email': 'prueba@prueba.com',
            'title': 'title'
        }
        mock_service
        subscriptions = all_subscriptions()

        self.assertEquals(subscriptions, expected_subscriptions)
        self.assertTrue(mock_service.get_all.has_called)

    @mock.patch('src.routers.notification_router.logging')
    @mock.patch('src.routers.notification_router.service')
    def test_notify_new_job(self, mock_service, mock_logging):
        job_position = mock.Mock()
        response = notify_new_job(job_position)

        mock_logging.info.assert_called_with(f'New Position received: %s', job_position)
        mock_service.notify_new_job.assert_called_with(job_position)
        self.assertEquals(response, 'Sucess')