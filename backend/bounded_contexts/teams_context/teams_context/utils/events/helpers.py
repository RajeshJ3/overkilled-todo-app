from teams_context import config


def get_event_message_metadata() -> dict:
    return {"source_bc": config.BOUNDED_CONTEXT_NAME}
