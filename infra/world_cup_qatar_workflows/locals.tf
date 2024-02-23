locals {
  world_cup_qatar_functions_workflow_config = jsondecode(file("${path.module}/resource/config/world_cup_qatar_functions_workflow_config.json"))
  world_cup_qatar_services_workflow_config  = jsondecode(file("${path.module}/resource/config/world_cup_qatar_services_workflow_config.json"))
}