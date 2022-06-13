from abc import ABC, abstractmethod


class Filter(ABC):

    @abstractmethod
    def filter(self):
        pass


class GenericFilter(Filter):

    def __init__(self, field, value, compare_function):
        self.field = field
        self.value = value
        self.compare_function = compare_function

    def filter(self, jobs):
        return [job for job in jobs if self.compare_function(getattr(job, self.field, ''), self.value)]

    def __repr__(self):
        return f'[{self.__class__.__name__}] - Field: {self.field} - Value: {self.value}'


class GreaterThanFilter(GenericFilter):

    def __init__(self, field, value):
        super().__init__(field, value, lambda field_value, expected_value: field_value >= expected_value)


class LessThanFilter(GenericFilter):

    def __init__(self, field, value):
        super().__init__(field, value, lambda field_value, expected_value: field_value <= expected_value)


class EqualsThanFilter(GenericFilter):

    def __init__(self, field, value):
        super().__init__(field, value, lambda field_value, expected_value: field_value == expected_value)


class ContainsFilter(GenericFilter):

    def __init__(self, field, value):
        super().__init__(field, value, lambda field_value, expected_value: expected_value in field_value)


class MultiContainsFilter(GenericFilter):

    def __init__(self, field, value):
        filter_function = lambda field_values, expected_values: any([v for v in expected_values if v in field_values])

        super().__init__(field, value, filter_function)


def generate_filter(title, description, salary_min, salary_max, country, tags):
    filters = []
    if title:
        filters.append(ContainsFilter('title', title))
    if description:
        filters.append(ContainsFilter('description', description))
    if salary_min:
        filters.append(GreaterThanFilter('salary', salary_min))
    if salary_max:
        filters.append(LessThanFilter('salary', salary_max))
    if country:
        filters.append(EqualsThanFilter('country', country))
    if tags:
        filters.append(MultiContainsFilter('tags', tags))

    return filters
