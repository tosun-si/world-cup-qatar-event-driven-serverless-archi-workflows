resource "google_workflows_workflow" "workflow_world_cup_services" {
  project         = var.project_id
  region          = var.location
  name            = local.world_cup_qatar_services_workflow_config["workflowName"]
  description     = "Workflow Event Driven and Serverless World Cup Cloud Run Services"
  service_account = var.workflow_sa
  source_contents = file("${path.module}/${local.world_cup_qatar_services_workflow_config["workflowFilePath"]}")
}

resource "google_eventarc_trigger" "workflow_world_cup_services_trigger" {
  depends_on = [
    google_workflows_workflow.workflow_world_cup_services
  ]

  project         = var.project_id
  name            = local.world_cup_qatar_services_workflow_config["workflowTriggerName"]
  location        = var.location
  service_account = var.workflow_sa

  matching_criteria {
    attribute = "type"
    value     = "google.cloud.storage.object.v1.finalized"
  }
  matching_criteria {
    attribute = "bucket"
    value     = local.world_cup_qatar_services_workflow_config["workflowTriggerBucket"]
  }

  destination {
    workflow = google_workflows_workflow.workflow_world_cup_services.id
  }
}