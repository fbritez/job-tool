import unittest
from unittest import mock

from src.services.notification_service import NotificationService


class NotificationServiceTests(unittest.TestCase):

    def test_initialization(self):
        mock_email_server = mock.Mock()
        service = NotificationService(mock_email_server)

        self.assertEquals(service.persistence_service, [])
        self.assertEquals(self.email_server, mock_email_server)

    def test_new_subscription(self):
        mock_email_server = mock.Mock()
        mock_subscription = mock.Mock()
        service = NotificationService(mock_email_server)

        service.new_subscription(mock_subscription)

        self.assertIn(mock_subscription, service.get_persistence_service())

    def test_get_all(self):
        mock_email_server = mock.Mock()
        service = NotificationService(mock_email_server)

        self.assertEquals(service.get_all(), [])

    def test_notify_new_job(self):
        mock_job = mock.Mock()
        mock_email_server = mock.Mock()
        mock_subscription = mock.Mock()
        mock_subscription.email = 'abcd@efgh.com'
        mock_subscription.match_with.return_value = True

        service = NotificationService(mock_email_server)

        service.new_subscription(mock_subscription)

        service.notify_new_job(mock_job)

        mock_email_server.send.assert_called_with('abcd@efgh.com', mock_job)


