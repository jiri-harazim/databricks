# Databricks notebook source
# MAGIC %md ### About
# MAGIC 
# MAGIC Welcome to the notebook that shows how to deploy a model as a webservice in AzureML. It uses a simple SciKit learn model based on well-known iris dataset and deploys the model as an online scoring service.
# MAGIC 
# MAGIC This notebook is based on the [MLflow Quick Start tutorial]([https://docs.azuredatabricks.net/_static/notebooks/mlflow/mlflow-quick-start-deployment-azure.html)

# COMMAND ----------

# MAGIC %md ### Setup your environment

# COMMAND ----------

# MAGIC %md
# MAGIC We start with installing the required python libraries into our notebook. Simply run the cell below.

# COMMAND ----------

dbutils.library.installPyPI("mlflow", extras="extras")
dbutils.library.installPyPI("azureml-sdk", extras="databricks")
dbutils.library.installPyPI("pandas")
dbutils.library.restartPython()

# COMMAND ----------

# MAGIC %md ### Provide your configuration

# COMMAND ----------

# MAGIC %md
# MAGIC This is a central configuration for this notebook. You shouldn't need to modify any other cell/code in this notebook other than this one, eg you will just run the remaining cells in this notebook. Please provide your configuration:

# COMMAND ----------

# MLflow configuration.
artifact_path = "sk-models" # This is the name of a folder created in mlflow. You can safely use the default.

# AzureML congiguration. You must provide all of them.
workspace_name = "<your_azureml_workspace_name>" # Display name for your AzureML Workspace, eg "Team XYZ Workspace Dev"
workspace_location="<azure_region>" # Azure region where the AzureML Workspace is created in. Eg. "eastus2"
resource_group = "<resource-group>" # Azure resource group that will host the AzureML Workspace. Eg "teamxyz-resource-group"
subscription_id = "<subscription_id>" # Azure subscription id where the AzureML Workspace will be created at 

# COMMAND ----------

# MAGIC %md ### Create and persist model

# COMMAND ----------

from sklearn.linear_model import LogisticRegression
from sklearn import datasets
import mlflow
import mlflow.sklearn

run_id = None # A unique id across all mlflow experiments. We use it for referencing our model.

with mlflow.start_run():
  
  # import some data to play with
  X, y = datasets.load_iris(return_X_y=True)

  # provide parameters for your model
  random_state = 0
  solver = 'lbfgs'
  multi_class = 'multinomial'
  max_iterations = 150
  # log parameters
  mlflow.log_param("random_state", random_state)
  mlflow.log_param("solver", solver)
  mlflow.log_param("multi_class", multi_class)
  mlflow.log_param("max_iterations", max_iterations)
  mlflow.set_tag("framework", "sklearn")
  # create a model
  model = LogisticRegression(random_state=random_state, solver=solver, multi_class=multi_class, max_iter=max_iterations)
  model = model.fit(X, y)
  # log metris and persiste model via mlflow.<flavour>.log_model
  score = model.score(X,y)
  mlflow.log_metric("score", model.score(X,y))
  mlflow.sklearn.log_model(model, artifact_path)
  # obtain run_id for next steps
  run_id = mlflow.active_run().info.run_id
  print("run_id: {}".format(run_id))
  print("Score: {}".format(model.score(X,y)))

# COMMAND ----------

# MAGIC %md ### Load model

# COMMAND ----------

# MAGIC %md
# MAGIC In this step we read the model from a persistent artifact storage we created in the previous step. This is to demonstrate the retrieval of created models using `run_id` as we will need in the next step when deploying to AzureML.

# COMMAND ----------

model_uri = "runs:/{}/{}".format(run_id, artifact_path)
model_loaded = mlflow.sklearn.load_model(model_uri)
print(model_uri)

# COMMAND ----------

# MAGIC %md
# MAGIC It is a good idea to test your model before we start working with webservices. Quickly test it here:

# COMMAND ----------

iris_setosa = [(5.1,3.5,1.4,0.2)] # 0
iris_virginica1 = [(6.8,3.2,5.9,2.3)] # 2
iris_versicolor = [(6.3,3.3,4.7,1.6)] # 1
iris_virginica2 = [(6.9,3.2,5.7,2.3)] # 2
for iris in [iris_setosa, iris_virginica1,  iris_versicolor, iris_virginica2]:
  print(model_loaded.predict(iris))

# COMMAND ----------

# MAGIC %md ### Create AzureML Workspace
# MAGIC 
# MAGIC This step requires an interactive authentication to your workspace (unless you modify the code to use a service principal).

# COMMAND ----------

import azureml
from azureml.core import Workspace

workspace = Workspace.create(name = workspace_name,
                             location = workspace_location,
                             resource_group = resource_group,
                             subscription_id = subscription_id,
                             exist_ok=True)

# COMMAND ----------

# MAGIC %md ### Create AzureML model image

# COMMAND ----------

import mlflow.azureml

# This command may run for several minutes. Use the next command to wait for the result.
model_image, azure_model = mlflow.azureml.build_image(model_uri=model_uri, 
                                                      workspace=workspace,
                                                      model_name="iris-model",
                                                      image_name="iris-model",
                                                      description="Sklearn LR image for predicting iris",
                                                      synchronous=False)

# COMMAND ----------

model_image.wait_for_creation(show_output=True)

# COMMAND ----------

# MAGIC %md ### Deploy AzureML model image as a webservice

# COMMAND ----------

from azureml.core.webservice import AciWebservice, Webservice

dev_webservice_name = "iris-model"
dev_webservice_deployment_config = AciWebservice.deploy_configuration()
dev_webservice = Webservice.deploy_from_image(name=dev_webservice_name, image=model_image, deployment_config=dev_webservice_deployment_config, workspace=workspace)

# COMMAND ----------

dev_webservice.wait_for_deployment()

# COMMAND ----------

# MAGIC %md ### Test: Query the deployed model

# COMMAND ----------

import requests
import json

def query_endpoint_example(scoring_uri, inputs, service_key=None):
  headers = {
    "Content-Type": "application/json",
  }
  if service_key is not None:
    headers["Authorization"] = "Bearer {service_key}".format(service_key=service_key)
    
  print("Sending batch prediction request with inputs: {}".format(inputs))
  # Note you can use also workspace.run(inputs)
  response = requests.post(scoring_uri, data=inputs, headers=headers)
  preds = json.loads(response.text)
  print("Received response: {}".format(preds))
  return preds

# COMMAND ----------

dev_webservice.scoring_uri

# COMMAND ----------

# Ensure that the input is a valid JSON-formatted Pandas DataFrame with the `split` orient produced using the `pandas.DataFrame.to_json(..., orient='split')` method.
# query_input = "{'columns': ['col1', 'col2', 'col3', 'col4'], 'data': [[(5.1,3.5,1.4,0.2)]]"
# dbutils.library.installPyPI("pandas")
from pandas import DataFrame

query_input = None

for iris in [iris_setosa, iris_virginica1,  iris_versicolor, iris_virginica2]: # labels are 0, 2, 1, 2
  query_input = DataFrame(data=iris, columns=['col1', 'col2', 'col3', 'col4']).to_json(orient='split')
  dev_prediction = query_endpoint_example(scoring_uri=dev_webservice.scoring_uri, inputs=query_input)

# COMMAND ----------

# MAGIC %md ### Clean-up
# MAGIC You finished this tutorial. Now it is time to clean-up the resources, namely the running scoring webservice and/or [delete the AzureML Workspace](https://docs.microsoft.com/en-us/python/api/azureml-core/azureml.core.workspace.workspace?view=azure-ml-py#delete-delete-dependent-resources-false--no-wait-false-) if you don't plan to re-use it.

# COMMAND ----------

dev_webservice.delete()

# COMMAND ----------

workspace.delete(delete_dependent_resources=True)

# COMMAND ----------

# MAGIC %md ### Congratulations! You have finished this notebook

# COMMAND ----------

# MAGIC %md
# MAGIC Let's summarize what we did in this notebook:
# MAGIC 
# MAGIC 
# MAGIC 1. We configured AzureML parameters (subscription_id etc)
# MAGIC 1. We installed required python libraries
# MAGIC 1. We created an SciKit learn model
# MAGIC 1. We created a new AzureML Workspace
# MAGIC 1. We build a model image in our AzureML Workspace
# MAGIC 1. We deployed the model image as webservice
# MAGIC 1. We tested the webservice works - so it can be used in another application.
# MAGIC 1. We shut down the running webservice.