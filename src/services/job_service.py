from src.model import JobPosition
import uuid
import logging


class JobPositionService:

    def __init__(self, listeners=None):
        self.persistence_service = []
        self.listeners = listeners if listeners else []

    def get_persistence_service(self):
        return self.persistence_service

    def get_all(self):
        return self.persistence_service

    def store(self, job_position: JobPosition):
        logging.info('Storing: %s', job_position)
        if not job_position.get_id():
            job_position.id = str(uuid.uuid4())
        self.persistence_service.append(job_position)

        self.notify_listeners(job_position)

    def notify_listeners(self, job_position):
        for listener in self.listeners:
            listener.push(job_position)

    def get_jobs_by_id(self, job_id):
        jobs = [job for job in self.persistence_service if job.get_id() == job_id]

        return jobs[:1] if len(jobs) >= 1 else []

    def filter_jobs(self, filters):
        filtered_jobs = self.persistence_service
        for filter_object in filters:
            filtered_jobs = filter_object.filter(filtered_jobs)

        return filtered_jobs






