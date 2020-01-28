import logging
import re

import azure.functions as func
from __app__.shared_code import config, slack_utils


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    slack_message = {}
    message = ""
    send_approval_message = False
    try:
        event = req.get_json()
        event_type =  event.get("eventType")

        if event_type == "build.complete":
            resource = event.get("resource")
            status = resource.get("status")
            build_id = resource.get("id")
            reason = resource.get("reason")
            build_pipeline = resource.get("definition").get("name")
        elif event_type == "ms.vss-pipelines.run-state-changed-event":
            event_message = event.get("message").get("text")
            regex = r"buildId=([0-9]*)"
            build_id_search = re.search(regex, event.get("message").get("html"), re.IGNORECASE)

            if build_id_search:
                build_id = build_id_search.group(1)
            else:
                raise Exception("BuildId not found in event {event_type}".format(event_type=event_type))

            if "in progress" in event_message:
                status = "inprogress"
            elif "cancelled" in event_message:
                status = "cancelled"
            else:
                raise Exception("No other event to he handled with event type {event_type}".format(event_type=event_type))
        logging.info("Build Id:"+str(build_id))
        LOG = "<"+config.AZURE_PIPELINE_BUILD_RESULT_URL.format(build_id=build_id)+"| `Build Number: {build_id}`>".format(build_id=build_id)

        if status == "succeeded":
            color = config.SLACK_RES_COLORS["SUCCESS"]
            message = "Build `successfull` for {log_url}".format(log_url=LOG)
            if reason == "validateShelveset":
                message += " ready to merge."
            elif reason == "individualCI" and build_pipeline == config.STAGE_BUILD_PIPELINE:
                message += "\n Click <"+config.STAGE_ENV_URL+"| here> to go to staging environment"
                send_approval_message = True
            elif build_pipeline == config.PROD_BUILD_PIPELINE:
                message += "\n Click <"+config.PROD_ENV_URL+"| here> to go to production environment"
        elif status == "failed":
            color = config.SLACK_RES_COLORS["FAILURE"]
            message = "Build `failed` for {log_url}".format(log_url=LOG)
        elif status == "inprogress":
            color = config.SLACK_RES_COLORS["QUEUED"]
            message = "Build `in progress` for {log_url}".format(log_url=LOG)
        elif status == "cancelled":
            color = config.SLACK_RES_COLORS["CANCELLED"]
            message = "Build `cancelled` for {log_url}".format(log_url=LOG)

        slack_client = slack_utils.get_client(access_token = config.CICD_BOT_TOKEN)
        slack_message = get_message_attachment(text=message, color=color)

        slack_utils.send_message(client = slack_client, attachments = slack_message, channel = config.SLACK_CHANNEL)
        if send_approval_message:
            approval_message = get_approval_message(text="Do you want to deploy it to production?", color = config.SLACK_RES_COLORS["SUCCESS"])
            slack_utils.send_message(client = slack_client, attachments = approval_message, channel = config.SLACK_CHANNEL)
    except Exception as e:
        logging.error("Error occured due to exception: {error}".format(error=e))

    return func.HttpResponse(
            "Event successfully served!!",
            status_code=200
    )

def get_message_attachment(text, color):
    attachments = [{
        "fallback": text,
        "text":text,
        "color":color
    }]
    return attachments

def get_approval_message(text, color):
    attachments = [{
        "fallback": "You selected no!!",
        "callback_id":"deploy_prod_action_yes_no",
        "text":text,
        "color":color,
        "actions": [
                {
                    "name": "deploy_prod_action_yes",
                    "text": "Yes",
                    "type": "button",
                    "value": "yes",
                    "style":"primary"
                },
                {
                    "name": "deploy_prod_action_no",
                    "text": "No",
                    "type": "button",
                    "value": "no",
                    "style": "danger"
                }]
    }]
    return attachments