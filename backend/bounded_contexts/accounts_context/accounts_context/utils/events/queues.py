# lib
from events_framework.utils.queues import Queue

# svc
from accounts_context import config


class Queue(Queue):
    USERS = config.RABBITMQ_USERS_QUEUE_NAME
