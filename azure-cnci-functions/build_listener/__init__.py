import logging

import azure.functions as func
from __app__.shared_code import config, slack_utils, utils

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    slack_message = {}
    message = ""
    send_approval_message = False
    try:
        event = req.get_json()
        event_type =  event.get("eventType")

        logging.info("Event received is: {event}".format(event=event))

        result = utils.parse_event(event=event, event_type=event_type)

        status = result["status"]
        build_id = result["build_id"]

        logging.info("Build Id:"+str(build_id))
        log_url_text = config.BUILD_LOG_URL_TEXT.format(build_log_url=config.AZURE_PIPELINE_BUILD_RESULT_URL.format(build_id=build_id),
                                                        build_id=build_id)

        slack_message, send_approval_message = slack_utils.get_build_message(event_result=result, 
                                                                             log_url_text=log_url_text)

        slack_client = slack_utils.get_client(access_token = config.CICD_BOT_TOKEN)

        slack_utils.send_message(client = slack_client, 
                                 attachments = slack_message, 
                                 channel = config.SLACK_CHANNEL)

        if send_approval_message:
            approval_message = slack_utils.get_approval_message(text="Do you want to deploy it to production?", color = config.SLACK_RES_COLORS["SUCCESS"])
            slack_utils.send_message(client = slack_client, attachments = approval_message, channel = config.SLACK_CHANNEL)

    except Exception as e:
        logging.error("Error occured due to exception: {error}".format(error=e))
        return func.HttpResponse(
            body = "Something went wrong!!",
            status_code=500
        )

    return func.HttpResponse(
            body = "Event successfully served!!",
            status_code=200
    )