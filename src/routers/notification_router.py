from typing import List, Union
from fastapi import APIRouter
import starlette.status as status
import logging

from starlette.responses import JSONResponse

from src.filter.filters import generate_filter
from src.model import JobPosition, Subscription, SubscriptionDTO
from src.services.notification_service import NotificationService

router = APIRouter()


class FakeEmailServer:

    def send(self, email, job):
        logging.info(email)
        logging.info(job)


service = NotificationService(FakeEmailServer())


@router.post("/subscription")
def new_subscribe(subscription: SubscriptionDTO):
    data = subscription.dict()
    logging.info('Subscrition request for: %s', data)

    filters = generate_filter(title=data.get('title', None),
                              description=data.get('description', None),
                              salary_min=data.get('salary_min', None),
                              salary_max=data.get('salary_max', None),
                              country=data.get('country', None),
                              tags=data.get('tags', None))

    subscription = Subscription(email=data['email'], filters=filters)

    service.new_subscription(subscription)

    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content={"message": f"Subscription successful"})


@router.get("/subscriptions", responses={status.HTTP_200_OK: {"jobs": List}})
def all_subscriptions():
    return service.get_all()


@router.post("/notify", responses={status.HTTP_200_OK: {"Status": str}})
def notify_new_job(job_position: JobPosition):
    logging.info(f'New Position received: %s', job_position)
    service.notify_new_job(job_position)
    return 'Sucess'
