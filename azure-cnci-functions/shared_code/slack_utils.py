from slack import WebClient
import ssl
import requests
import logging

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

def send_message(client, channel, message=None, attachments=None):
    client.chat_postMessage(channel=channel,
                            text=message,
                            attachments=attachments)

def send_response(url, data):
    logging.info(requests.post(url=url, json = data))