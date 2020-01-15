import os
import requests
import json

# About: This script shows how to disable a schedule from Databricks jobs scheduler.
# Author: jiri.harazim@databricks.com

DOMAIN = os.environ['DATABRICKS_URL'] # Set your environment variables!
TOKEN = os.environ['DATABRICKS_TOKEN']

BASE_URL = '%s/api/2.0' % (DOMAIN)


def get_job(job_id):
    """Returns job given by job_id as a json from Databricks jobs REST API.
    You can use List operation to get all jobs too,
    see https://docs.microsoft.com/en-us/azure/databricks/dev-tools/api/latest/jobs#--list """
    url = BASE_URL + '/jobs/get?job_id={}'.format(job_id)
    response = requests.get(
      url,
      headers={"Authorization": "Bearer {}".format(TOKEN) }
    )
    return response.json()


def save_job(job):
    return "Implement saving of jobs so they can be restored later!"



def remove_schedule(job):
    """Remove json element 'schedule' and renames 'settings' to 'new_settings' as expected by API reset() operation."""
    data = job # json.loads(job)
    if 'schedule' in data["settings"]:
      del data["settings"]['schedule']
    data["new_settings"] = data.pop("settings")
    return json.dumps(data)


def update_job(job):
    """Updates jobs definition on Databricks server"""
    url = BASE_URL + '/jobs/reset'
    response = requests.post(
        url,
        headers={"Authorization": "Bearer {}".format(TOKEN)},
        data=job
    )
    return response.json()


# Test preparing updated schedule request:
# example_job_with_schedule = '{"job_id": 31462, "settings" : {"name" : "daily_load", "schedule" : "cron"}}'
# print("Before: " + example_job_with_schedule)
# print("After: " + remove_schedule(json.loads(example_job_with_schedule)))


# Test it on real job
#job = get_job(31462)
#print(job)
#new_settings = remove_schedule(job)
#print(new_settings)
#response = update_job(new_settings)
#print(response)


# Output:
# {"job_id": 31462, "settings" : { "name" : "daily_load", "schedule" : "cron" } }
# {"job_id": 31462, "settings": {"name": "daily_load"}}

# Real examples:
# Here are example of real JSON returned by Databricks jobs REST API operation get_job. Note without and with 'schedule'
# {'job_id': 31462, 'settings': {'name': 'jiri-schedulertest', 'existing_cluster_id': '1107-113xx-taste147', 'email_notifications': {}, 'timeout_seconds': 0, 'notebook_task': {'notebook_path': '/Users/xxx@databricks.com/test-repl', 'revision_timestamp': 0}, 'max_concurrent_runs': 1}, 'created_time': 1579017926360, 'creator_user_name': 'xxx@databricks.com'}
# {'job_id': 31462, 'settings': {'name': 'jiri-schedulertest', 'existing_cluster_id': '1107-113xx-taste147', 'email_notifications': {}, 'timeout_seconds': 0, 'schedule': {'quartz_cron_expression': '0 0 * * * ?', 'timezone_id': 'US/Pacific'}, 'notebook_task': {'notebook_path': '/Users/xxx@databricks.com/test-repl', 'revision_timestamp': 0}, 'max_concurrent_runs': 1}, 'created_time': 1579017926360, 'creator_user_name': 'xxx@databricks.com'}
