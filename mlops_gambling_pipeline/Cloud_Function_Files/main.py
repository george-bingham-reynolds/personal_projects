import base64
import json
from google.cloud import aiplatform

# BASED ON GOOGLE CLOUD DOCUMENTATION HERE: https://cloud.google.com/vertex-ai/docs/pipelines/trigger-pubsub

# CHANGE FOR OWN PROJECT
PROJECT_ID = 'YOUR-PROJECT-ID' #CHANGE TO YOUR PROJECT ID                  
REGION = 'us-central1'                          
PIPELINE_ROOT = 'gs://nfl_spreads_model_output_gamma/pipeline_root/' 


def nfl_spreads_gamma_subscribe(event, context):
  """Triggered from google cloud storage repo update.
  Args:
        event (dict): Event payload.
        context (google.cloud.functions.Context): Metadata for the event.
  """
  # UPON MESSAGE FOR REPO UPDATE, RUN PIPELINE BUILD FUNCTION
  trigger_pipeline_run() 

def trigger_pipeline_run(): 
  """Triggers a pipeline run
  """

  # LOCATION OF PIPELINE SPECS MOVED TO GCS IN PIPELINE NOTEBOOK
  pipeline_spec_uri = "gs://nfl_spreads_model_output_gamma/nfl_spreads_model.json" 


  # Create a PipelineJob using the compiled pipeline from pipeline_spec_uri
  aiplatform.init(
      project=PROJECT_ID,
      location=REGION,
  )
  job = aiplatform.PipelineJob(
      display_name='nfl-spreads-pipeline',
      template_path=pipeline_spec_uri,
      pipeline_root=PIPELINE_ROOT,
      enable_caching=False
  )

  # Submit the PipelineJob
  job.submit()