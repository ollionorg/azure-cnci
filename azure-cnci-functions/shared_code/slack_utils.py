import ssl
import requests
import logging

from slack import WebClient

from __app__.shared_code import config
from __app__.shared_code.enum.build_reason import BuildReason


def get_ssl_context():
        '''
        Returns default no-cert context
        '''
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        return ssl_context

def get_client(access_token):
    ''' Return slack client object oh the basis of access token
        if access is None or empty client without auth returned
    
    @param acces_token: str, optional 
    '''
    if access_token in ["", None]:
        access_token = None
    
    ssl_context = get_ssl_context()    
    client = WebClient(token=access_token,
                        ssl=ssl_context)
    
    return client

def get_build_message(event_result, log_url_text):
    status = event_result.get("status")
    send_approval_message = False

    if status == "succeeded":
        reason = event_result.get("reason")
        build_pipeline = event_result.get("build_pipeline")
        
        color = config.SLACK_RES_COLORS["SUCCESS"]
        message = "Build `successfull` for {log_url_text}".format(log_url_text=log_url_text)
        if reason == BuildReason.VALIDATE_SHELVE_SET.value:
            message += ", ready to merge."
        elif reason == BuildReason.INDIVIDUAL_CI.value and build_pipeline == config.STAGE_BUILD_PIPELINE:
            message += "\n Click <"+config.STAGE_ENV_URL+"| here> to go to staging environment"
            send_approval_message = True
        elif build_pipeline == config.PROD_BUILD_PIPELINE:
            message += "\n Click <"+config.PROD_ENV_URL+"| here> to go to production environment"
    elif status == "failed":
        color = config.SLACK_RES_COLORS["FAILURE"]
        message = "Build `failed` for {log_url}".format(log_url=log_url_text)
    elif status == "inprogress":
        color = config.SLACK_RES_COLORS["QUEUED"]
        message = "Build `in progress` for {log_url}".format(log_url=log_url_text)
    elif status == "cancelled":
        color = config.SLACK_RES_COLORS["CANCELLED"]
        message = "Build `cancelled` for {log_url}".format(log_url=log_url_text)
    else:
        raise Exception("Method not supported for status {status}".format(status=status))

    return get_message_attachment(text=message, color=color), send_approval_message

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

def send_message(client, channel, message=None, attachments=None):
    client.chat_postMessage(channel=channel,
                            text=message,
                            attachments=attachments)

def send_response(url, data):
    logging.info(requests.post(url=url, json = data))