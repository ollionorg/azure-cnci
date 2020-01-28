import logging
import json

import azure.functions as func
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from azure.devops.v6_0.pipelines import models
from __app__.shared_code import config, slack_utils

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    pipeline_id = None
    build_run_result_url = None
    pipeline_name = config.BUILD_DEPLOY_PROD_PIPELINE
    project_name = config.AZURE_DEVOPS_PROJECT_NAME
    payload = json.loads(req.form.get("payload"))
    
    if payload and payload.get("callback_id") == "deploy_prod_action_yes_no":
        
        action_value = payload.get("actions")[0].get("value")
        if action_value == "yes":
            response_url = payload.get("response_url")
            message = {"replace_original": 'true',
                        "text": "> Roger that, rolling out to production"}
            slack_utils.send_response(url=response_url,data=message)
        # Create a connection to the org
        credentials = BasicAuthentication('', config.AZURE_PERSONAL_ACCESS_TOKEN)
        connection = Connection(base_url=config.ORGANIZATION_URL, creds=credentials)
        try:
            # Create pipeline client for azure devops
            pipelines_client_v6_0 = connection.clients_v6_0.get_pipelines_client()

            # Find the pipeline id on the basis of given pipeline name
            pipelines = pipelines_client_v6_0.list_pipelines(project=project_name)
            for pipeline in pipelines:
                logging.info("Pipeline name:"+str(pipeline.name))
                if pipeline.name == pipeline_name:
                    pipeline_id = pipeline.id
            logging.info("Pipeline id:"+str(pipeline_id))

            # Creating empty run params
            run_parameters = models.RunPipelineParameters()

            # Inititate pipeline run
            build_run_result_url = pipelines_client_v6_0.run_pipeline(run_parameters=run_parameters,project=project_name,pipeline_id=pipeline_id)._links.additional_properties.get("web").get("href")
        except Exception as e:
            logging.error("Error due to exception: {error}".format(error=e))

    return func.HttpResponse(build_run_result_url)     

