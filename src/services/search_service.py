import itertools
import logging

import requests


class SearchService:

    def __init__(self, sources):
        self.sources = sources

    def search_jobs(self, title, description, salary_min, salary_max, country, tags):
        job_results = [source.search_jobs(title=title,
                                          description=description,
                                          salary_min=salary_min,
                                          salary_max=salary_max,
                                          country=country,
                                          tags=tags)
                       for source in self.sources]

        return list(itertools.chain(*job_results))


class ExternalSource:

    def __init__(self, source_url, search_field_mapping, field_to_object_function):
        self.source_url = source_url
        self.search_field_mapping = search_field_mapping
        self.field_to_object_function = field_to_object_function

    def search_jobs(self, **kwargs):
        query_string = ''
        for field, external_field in self.search_field_mapping.items():
            if field in kwargs and kwargs[field]:
                query_string = f'{query_string}&{external_field}={kwargs[field]}'
        full_url = f'{self.source_url}?{query_string}'

        logging.info('Query: %s', full_url)
        response = requests.get(full_url)
        logging.info('Query Response: %s', response.ok)

        jobs = []
        if response.ok:
            jobs = [self.field_to_object_function(value) for value in response.json()]

        return jobs



