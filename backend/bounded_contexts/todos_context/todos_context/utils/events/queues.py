# lib
from events_framework.utils.queues import Queue

# svc
from todos_context import config


class Queue(Queue):
    USERS = config.RABBITMQ_USERS_QUEUE_NAME
