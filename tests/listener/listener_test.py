import unittest
from unittest import mock

from src.listener.listener import ExternalListener


class ExternalListenerTests(unittest.TestCase):

    def test_initialization(self):
        listener = ExternalListener('xxxx.xxxx.xxx')

        self.assertEquals(listener.source_url, 'xxxx.xxxx.xxx')

    @mock.patch('src.listener.listener.logging')
    @mock.patch('src.listener.listener.requests')
    def test_push(self, mock_request, mock_logging):
        job = mock.Mock()
        job.dict.return_value = {'data': 'data'}
        mock_response = mock.Mock()
        mock_response.ok = True
        mock_request.post.return_value = mock_response
        listener = ExternalListener('xxxx.xxxx.xxx')

        listener.push(job)

        mock_request.post.assert_called_with('xxxx.xxxx.xxx', json={'data': 'data'})
        mock_logging.info('Notification Status: %s', 'Notification successfully')

    @mock.patch('src.listener.listener.logging')
    @mock.patch('src.listener.listener.requests')
    def test_push_fail(self, mock_request, mock_logging):
        job = mock.Mock()
        job.dict.return_value = {'data': 'data'}
        mock_response = mock.Mock()
        mock_response.ok = False
        mock_request.post.return_value = mock_response
        listener = ExternalListener('xxxx.xxxx.xxx')

        listener.push(job)

        mock_request.post.assert_called_with('xxxx.xxxx.xxx', json={'data': 'data'})
        mock_logging.info('Notification Status: %s', 'Message error')
