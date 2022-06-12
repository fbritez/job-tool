from src.model import JobPosition
import uuid
import logging


class JobPositionService:

    def __init__(self):
        self.persistence_service = []

    def get_persistence_service(self):
        return self.persistence_service

    def get_all(self):
        return self.persistence_service

    def store(self, job_position: JobPosition):
        logging.info('Storing: %s', job_position)
        if not job_position.get_id():
            job_position.id = str(uuid.uuid4())
        self.persistence_service.append(job_position)

    def get_job_by_id(self, job_id):
        #jobs = [job for job in self.persistence_service if job.get_id() == job_id]
        jobs = []
        print(job_id)
        for job in self.persistence_service:
            print(job)
            if job.get_id() == job_id:
                jobs.append(job)

        return jobs[0] if len(jobs) >= 1 else None


