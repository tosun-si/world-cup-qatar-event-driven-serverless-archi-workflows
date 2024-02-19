resource "google_workflows_workflow" "workflow_world_cup_functions" {
  project         = var.project_id
  region          = var.location
  name            = var.workflow_name
  description     = "Workflow Event Driven and Serverless World Cup Cloud Functions"
  service_account = var.workflow_sa
  source_contents = local.world_cup_qatar_functions_workflow_yaml_as_string
}

resource "google_eventarc_trigger" "workflow_world_cup_functions_trigger" {
  depends_on = [
    google_workflows_workflow.workflow_world_cup_functions
  ]

  project         = var.project_id
  #  name            = "var.workflow_trigger.event_arc.name"
  name            = "workflow-world-cup-cloud-functions-trigger"
  location        = var.location
  service_account = var.workflow_sa

  matching_criteria {
    attribute = "type"
    value     = "google.cloud.storage.object.v1.finalized"
  }
  matching_criteria {
    attribute = "bucket"
    value     = "event-driven-functions-qatar-fifa-world-cup-stats-raw-wf"
  }

  destination {
    workflow = google_workflows_workflow.workflow_world_cup_functions.id
  }
}