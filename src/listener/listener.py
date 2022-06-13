import logging

import requests


class ExternalListener:

    def __init__(self, source_url):
        self.source_url = source_url

    def push(self, job_description):
        response = requests.post(self.source_url, json=job_description.dict())
        message = 'Notification successfully' if response.ok else 'Message error'

        logging.info('Notification Status: %s', message)
