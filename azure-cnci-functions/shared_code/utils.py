import re
import logging

from __app__.shared_code.enum.event_type import EventType
from __app__.shared_code.enum.build_status import BuildStatus

def parse_event(event, event_type):
    result = {}
    logging.info("Event to be parsed: {event} of event type {event_type}".format(event=event,
                                                                                 event_type=event_type))

    if event_type == EventType.BUILD_COMPLETE_EVENT.value:
        resource = event.get("resource")
        result.update( {"resource" : resource} )
        result.update( {"status" : resource.get("status")} )
        result.update( {"build_id" : resource.get("id")} )
        result.update( {"reason" : resource.get("reason")} )
        result.update( {"build_pipeline" : resource.get("definition").get("name")} )
    elif event_type == EventType.BUILD_RUNSTATE_CHANGE_EVENT.value:
        event_message = event.get("message").get("text")
        regex = r"buildId=([0-9]*)"
        build_id_search = re.search(regex, event.get("message").get("html"), re.IGNORECASE)

        if build_id_search:
            result.update( {"build_id" : build_id_search.group(1)} )
        else:
            raise Exception("BuildId not found in event {event_type}".format(event_type=event_type))
            
        if any(status in event_message for status in BuildStatus.IN_PROGRESS.value):
            result.update( {"status" : "inprogress"} )
        elif any(status in event_message for status in BuildStatus.CANCELLED.value):
            result.update( {"status" : "cancelled"} )
        else:
            raise Exception("No other event to be handled with event type {event_type}".format(event_type=event_type))
    logging.info("Parsed event value is: {result}".format(result=result))
    return result