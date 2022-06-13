import unittest
from src.filter.filters import generate_filter


class ModuleTests(unittest.TestCase):

    def test_generate_filters(self):
        filters = generate_filter(title='title', description='description', salary_min=100, salary_max=4000,
                                  country='Argentina', tags=['Example'])

        self.assertEquals(len(filters), 6)
