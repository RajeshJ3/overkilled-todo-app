from todos_context.utils.events.types import EventType

from todos_context.event_consumer_svc.event_handlers.users.user_registered import (
    handle_user_registered,
)

HANDLERS = {
    EventType.USER_REGISTERED.value: handle_user_registered,
}
