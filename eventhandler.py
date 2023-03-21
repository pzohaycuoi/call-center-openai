import logging
import azure.eventgrid
import common


common.logger_config()
logger = logging.getLogger("file")


def event_handler(event: azure.eventgrid.EventGridEvent):
    logger.info(event.data)
    print(event.data)
    return event.data
