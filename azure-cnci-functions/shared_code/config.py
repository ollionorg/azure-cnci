AZURE_PIPELINE_BUILD_RESULT_URL = "https://dev.azure.com/<<organization>>/<<devops_project>>/_build/results?buildId={build_id}&view=results"
AZURE_PERSONAL_ACCESS_TOKEN = "<<azure_personal_access_token>>"
ORGANIZATION_URL = "https://dev.azure.com/<<oragnization>>"
AZURE_DEVOPS_PROJECT_NAME = "<<devops_project>>"
BUILD_DEPLOY_PROD_PIPELINE = "<<prod_build_pipeline>>"
CICD_BOT_TOKEN = "<<slack_bot_token>>"
REPO_NAME = "<<git_repo_name>>"
GITHUB_ORG = "<<github_org>>"
GIT_PR_LINK = "https://github.com/{org}/{repo_name}/pull/{pull_number}"
GIT_PR_TEXT = "{repo_name}/pull/{pull_number}"
STAGE_BUILD_PIPELINE = "<<stage_build_pipeline>>"
PROD_BUILD_PIPELINE = "<<prod_build_pipeline>>"
STAGE_ENV_URL = "<<stage_env_url>>"
PROD_ENV_URL = "<<prod_env_url>>"
SLACK_CHANNEL = "<<devops_slack_channel>>"
BUILD_LOG_URL_TEXT = "<{build_log_url}| `Build Number: {build_id}`>"
SLACK_RES_COLORS = {
                        "SUCCESS": "#28c72a",
                        "FAILURE": "#eb0011",
                        "QUEUED": "#0083cc",
                        "WORKING": "#07b5ff",
                        "INTERNAL_ERROR": "#eb0011",
                        "TIMEOUT": "#f40072",
                        "CANCELLED": "#3a4247"
                    } 