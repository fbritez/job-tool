

class NotificationService:

    def __init__(self, email_server):
        self.persistence_service = []
        self.email_server = email_server

    def _get_persistence_service(self):
        return self.persistence_service

    def get_all(self):
        return self.persistence_service

    def new_subscription(self, new_subscription):
        self.persistence_service.append(new_subscription)

    def notify_new_job(self, job_position):

        subscriptions = [subscription for subscription in self._get_persistence_service()
                         if subscription.match_with(job_position)]

        for subscription in subscriptions:
            self.email_server.send(subscription.email, job_position)


