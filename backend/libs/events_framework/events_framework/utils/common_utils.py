# libs
from events_framework.utils.event_types import EventType


def event_message_builder(data: dict, event_type: EventType, meta: dict = None) -> dict:
    return {
        "action": event_type.value,
        "meta": meta,
        "payload": data,
    }
